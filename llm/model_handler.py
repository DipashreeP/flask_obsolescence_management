import requests
import boto3

def query_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "codellama", "prompt": prompt}
    )
    return response.json()["response"]

def query_bedrock(prompt):
    bedrock = boto3.client('bedrock-runtime', region_name="us-east-1")
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        body=f'{{"prompt":"{prompt}","max_tokens_to_sample":300}}'
    )
    return response['body'].read().decode()
