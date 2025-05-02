import json
import boto3
import urllib.request

bedrock = boto3.client('bedrock-runtime')

def fetch_latest_codebuild_logs(log_group_name):
    logs_client = boto3.client('logs')
    
    # Step 1: Get latest log stream
    response = logs_client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True,
        limit=1
    )
    
    log_stream_name = response['logStreams'][0]['logStreamName']

    # Step 2: Get log events
    events_response = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startFromHead=True
    )

    logs_text = "\n".join([event['message'] for event in events_response['events']])
    return logs_text

def filter_logs(logs):
    lines = logs.splitlines()
    # Focus on errors, warnings, or failure-related logs
    relevant_lines = [line for line in lines if "ERROR" in line or "WARNING" in line or "FAIL" in line]
    return "\n".join(relevant_lines)


def summarize_logs_with_mistral(log_text):
    filtered_log_text = filter_logs(log_text)
    
    prompt = f"""
    You are a DevOps assistant. Summarize the following CI/CD logs in a clear and structured format.

    Include the following sections:
    ✅ Deployment Status: Show if build/deploy succeeded or failed.
    📦 Build Phase: List phases completed, number of files deployed, and key commands executed.
    ⚠️ Warnings: Summarize important warnings with counts if repeated.
    🧠 Recommendations: Suggest possible fixes for issues/warnings.
    🕒 Duration: Include total build time and memory usage.

    Respond in this markdown format:

    ✅ Deployment Status: ...

    📦 Build Phase:
    - ...
    - ...
    - ...

    ⚠️ Warnings:
    - ... — repeated X times

    🧠 Recommendations:
    - ...
    - ...

    🕒 Duration: ... | Max Memory Used: ...

    Logs:
    {filtered_log_text}
    """

    body = {
        "prompt": prompt,
        "max_tokens": 800
    }

    response = bedrock.invoke_model(
        modelId="mistral.mistral-large-2402-v1:0",  # replace with your actual model ID
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    result = json.loads(response['body'].read())
    generated_text = result.get("generation") or result.get("outputs", [{}])[0].get("text")
    print("Bedrock raw output:", result)
    return generated_text or "No summary generated."


def send_summary_to_slack(summary):
    slack_webhook_url = "https://hooks.slack.com/services/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"
    payload = {
        "text": f"📦 *Deployment Summary:*\n\n{summary}"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(slack_webhook_url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        response.read()

def lambda_handler(event, context):
    log_group = "/aws/codebuild/python-app-flask"

    logs_text = fetch_latest_codebuild_logs(log_group)
    summary = summarize_logs_with_mistral(logs_text)
    send_summary_to_slack(summary)

    return {
        "statusCode": 200,
        "body": json.dumps("Summary sent to Slack!")
    }
