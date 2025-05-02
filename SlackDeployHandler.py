import json
import boto3
import urllib.parse

codepipeline = boto3.client('codepipeline')

def lambda_handler(event, context):
    print("Event:", event)

    # Parse Slack form-encoded body (important!)
    body = urllib.parse.parse_qs(event.get('body', ''))
    print("Parsed Body:", body)

    try:
        # Start the pipeline
        response = codepipeline.start_pipeline_execution(
            name='PythonAppPipeline'  # <-- Replace with your pipeline name
        )
        print("Pipeline Triggered:", response)

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({ "text": "🚀 Deploy command received! Your pipeline is starting..." })
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({ "text": f"❌ Failed to trigger pipeline: {str(e)}" })
        }

