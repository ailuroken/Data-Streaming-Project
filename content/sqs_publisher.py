import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from content.app import content

def publish_to_sqs(articles, broker_id="guardian_content"):
    try:
        sqs = boto3.client('sqs')
        queue_url = sqs.get_queue_url(QueueName=broker_id)['QueueUrl']

        for article in articles:
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(article)
            )
            print(f"Published to SQS: {article['webTitle']}")
    except (BotoCoreError, ClientError) as e:
        print(f"Error sending to SQS: {e}")

if __name__ == "__main__":
    search_term = "machine learning"
    date_from = "2023-01-01"
    articles = content(search_term, date_from=date_from)
    publish_to_sqs(articles)