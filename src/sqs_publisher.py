import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def publish_to_sqs(articles, broker_id="guardian_content"):
    """
    Publishes a list of articles to an Amazon SQS queue.

    Args:
        articles (list): A list of article dictionaries to publish.
        broker_id (str): The SQS queue name. Defaults to 'guardian_content'.

    Logs:
        Success messages for each article published.
        Error messages if sending to SQS fails.
    """
    try:
        sqs = boto3.client("sqs")
        queue_url = sqs.get_queue_url(QueueName=broker_id)["QueueUrl"]

        for article in articles:
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(article))
            print(f"Published to SQS: {article['webTitle']}")
    except (BotoCoreError, ClientError) as e:
        print(f"Error sending to SQS: {e}")
