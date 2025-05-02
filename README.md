# **AI DevOps Assistant Bot (AWS + GenAI + Slack)** 

### The AI DevOps Assistant Bot is designed to:
- Automate CI/CD pipeline triggers.
- Summarize CI/CD logs for quick insights.
- Detect anomalies and provide optimization recommendations.

> 🚨 **Important Note:** We welcome your ideas to enhance this bot! Feel free to contribute by creating issues or submitting pull requests.

---

## Table of Contents
1. [Achievements](#achievements)
2. [Tools/Tech Stack](#tools-tech-stack)
3. [Steps to Create This Bot](#steps-to-create-this-bot)
    - [Step 1: Set up a Slack App](#step-1-set-up-a-slack-app)
    - [Step 2: Set Up Permissions](#step-2-set-up-permissions)
    - [Step 3: Create AWS Lambda Function](#step-3-create-aws-lambda-function)
    - [Step 4: Create API Gateway for Lambda](#step-4-create-api-gateway-for-lambda)
    - [Step 5: Update Slack Command URL](#step-5-update-slack-command-url)
    - [Step 6: Test It!](#step-6-test-it)

## **Achievements**

- **Enhanced Productivity:** Reduced manual effort in triggering CI/CD processes by over 50% through automation.
- **Log Analysis:** Collects and analyzes CI/CD logs to detect anomalies, provide optimization recommendations, and summarize logs effectively.

## Steps to create this Bot

## **🛠️ Tools/Tech Stack:**

| Part                   | Tech                                      |
| :--------------------- | :---------------------------------------- |
| Backend Logic          | AWS Lambda (Node.js or Python)            |
| API Endpoint           | AWS API Gateway                           |
| Slack Bot              | Slack App + Slack Events API              |
| GenAI                  | AWS Bedrock or OpenAI or any AI you prefer) |


## **Step 1: Set up a Slack App**
- Go to [Slack API](https://api.slack.com/) Console.
- Create a new App.
- Enable Slash Commands like /deploy, /summarize
- Set the Request URL to your AWS API Gateway URL (we’ll create it soon).


## **Step 2: Set Up Permissions**
- Go to OAuth & Permissions
- Under Scopes → Bot Token Scopes, add:
    - commands
    - chat:write
- Click Install to Workspace
- You’ll now get a Bot User OAuth Token (like xoxb-xxxx...).


## **Step 3: Create AWS Lambda Function**
- Go to your [AWS Console](https://aws.amazon.com/) and search Lambda Functions
- Create Function Named `SlackDeployHandler` `(Python RunTime 3.12)`
- Add this code in your function
 ```
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
            name='###'  # <-- Replace with your pipeline name
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


 ```
 - add OAuth Token as Env Varibale
 - Similarlly create function named `SummerizePipelineLogs`
 - add `SummerizePipelineLogs.py` code


 ## **Step 4: Create API Gateway for Lambda**

- Go to API Gateway → Create API
- Name it: `SlackBotAPI` Create a Resource: `/slack` Add a `POST` method:
- Deploy the API: new Stage: `prod`
- Copy url `https://xxxxxx.execute-api.us-east-1.amazonaws.com/prod/slack`


## **Step 5: Update Slack Command URL**
- Go back to your Slack App dashboard → Slash Commands → `/deploy`
- Paste your new API Gateway URL.
- Do same for `/summarize` command

## **Step 6: Test It!**
- Go to Slack
- Type `/deploy` your CICD will be Triggered
- Type '/summarize' you will get summarized logs

## **Some Images of output**



## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.
