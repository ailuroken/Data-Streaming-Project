# Data Streaming Project

A serverless data pipeline that fetches articles from the Guardian API, processes them, and publishes to an SQS queue using AWS Lambda and Terraform. Only the free tier API key provided by the Guardian is needed. The application is written in python and the articles are published in JSon format. 

[The Guardian documentation](https://open-platform.theguardian.com/documentation/)
---
## 📚 Table of Contents

- [Setup Instructions](#️-setup-instructions)
  - [Clone the Repository](#1-clone-the-repository)
  - [Set up Virtual Environment](#2-set-up-virtual-environment)
  - [Configure AWS Credentials](#3-configure-aws-credentials)
  - [Store API key in SecretsManager](#4-create-secret-api-key)
  - [Build Requests Layer](#5-make-requests-layer-zip)
  - [Create Backend bucket](#6-create-backend)
- [Deployment](#️-deployment)
  - [Provision Infrastructure](#1-provision-infrastructure-with-terraform)
  - [CI/CD Pipeline](#2-cicd)
  - [SQS Queues](#-sqs-queues)
- [Example Event Payload](#-secrets)
- [Example Outputted SQS Message](#-tests)
- [Author](#️-author)

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ailuroken/Data-Streaming-Project.git
cd data-streaming-project
```
### 2. Set up Virtual Environment
```bash
make create-environment
source venv/bin/activate
make requirements
```
### 3. Configure AWS Credentials
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=eu-west-2
```
### 4. Store API key in SecretsManager
```bash
aws secretsmanager create-secret \
  --name guardianApiKey \
  --secret-string '{"API_KEY":"your-api-key"}'
```
### 5. Build Requests Layer
```bash
make build-requests-layer
```
### 6. Create Backend Bucket
```bash
aws s3api create-bucket \
  --bucket guardian-api-data-streaming \
  --region eu-west-2 \
  --create-bucket-configuration LocationConstraint=eu-west-2
```
## Deployment
### 1 Provision Infrastructure with Terraform
```bash
cd infrastructure/terraform
terraform init
terraform apply -auto-approve
```
### 2 CI/CD
GitHub Actions will automatically when pushed on main:

Run tests

Package the Lambda layer

Deploy infrastructure

All defined in .github/workflows/deploy.yml

## 📬 SQS Queues
guardian_content: Main queue for articles

guardian_content_dlq: Dead letter queue

## Example Event Payload
```bash
{
  "search_term": "climate change",
  "date_from": "2023-01-01",
  "date_to": "2023-12-31",
  "broker_id": "guardian_content"
}
```
## Example Outputted SQS Message
```bash
{
'webPublicationDate': '2024-01-05T22:38:21Z', 
'webTitle': 'Biden accuses Trump of ‘assault on democracy’ and says ‘it’s what he’s promising for the future’ - as it happened', 
'webUrl': 'https://www.theguardian.com/us-news/live/2024/jan/05/donald-trump-election-warning-nikki-haley-joe-biden-latest-news', 'content_preview': 'Biden delivered an impassioned speech ahead of the third anniversary of January 6</strong>. Speaking at Montgomery County Community College in Blue Bell, Pennsylvania, near Valley Forge, Biden asked the question, “is democracy still America’s sacred cause?”, underscoring his 2024 campaign’s theme of the importance of preserving democracy.</p> <p>In his speech, Biden also condemned all forms of political violence, recounting not just the 6 Jan insurrection, when the US capitol was attacked by an angry mob ahead of Biden’s inauguration, but other incidents such as the 2022 <a href="https://www.theguardian.com/us-news/2022/oct/30/democrats-warn-political-violence-after'
}
```
# ✍️ Author
Yuyao Ai – aiyuyao2000@gmail.com