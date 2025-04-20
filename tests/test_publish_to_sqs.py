import unittest
from unittest.mock import patch, MagicMock
import json
from botocore.exceptions import BotoCoreError, ClientError
from content.sqs_publisher import publish_to_sqs


class TestPublishToSQS(unittest.TestCase):

    def setUp(self):
        self.sample_articles = [
            {
                "webPublicationDate": "2025-04-18T09:00:05Z",
                "webTitle": "Sample Title",
                "webUrl": "https://example.com/article",
                "content_preview": "Preview preview preview"
            }
        ]

    @patch("content.sqs_publisher.boto3.client")
    def test_publish_successfully(self, mock_boto_client):
        mock_sqs = MagicMock()
        mock_boto_client.return_value = mock_sqs
        mock_sqs.get_queue_url.return_value = {'QueueUrl': 'https://dummy-queue-url'}

        publish_to_sqs(self.sample_articles, broker_id="guardian_content")

        mock_sqs.get_queue_url.assert_called_once_with(QueueName="guardian_content")
        mock_sqs.send_message.assert_called_once()
        args, kwargs = mock_sqs.send_message.call_args
        self.assertEqual(kwargs['QueueUrl'], 'https://dummy-queue-url')
        self.assertEqual(json.loads(kwargs['MessageBody']), self.sample_articles[0])

    @patch("content.sqs_publisher.boto3.client")
    def test_publish_with_empty_article_list(self, mock_boto_client):
        publish_to_sqs([], broker_id="guardian_content")
        mock_boto_client.assert_called_once()

    @patch("content.sqs_publisher.boto3.client", side_effect=BotoCoreError())
    def test_boto_client_failure(self, mock_boto_client):
        try:
            publish_to_sqs(self.sample_articles)
        except Exception as e:
            self.fail(f"Function raised an unexpected exception: {e}")

    @patch("content.sqs_publisher.boto3.client")
    def test_queue_url_failure(self, mock_boto_client):
        mock_sqs = MagicMock()
        mock_sqs.get_queue_url.side_effect = ClientError(
            error_response={'Error': {'Code': 'AWS.SimpleQueueService.NonExistentQueue'}},
            operation_name='GetQueueUrl'
        )
        mock_boto_client.return_value = mock_sqs

        try:
            publish_to_sqs(self.sample_articles, broker_id="nonexistent_queue")
        except Exception as e:
            self.fail(f"Function raised an unexpected exception: {e}")

    @patch("content.sqs_publisher.boto3.client")
    def test_send_message_failure(self, mock_boto_client):
        mock_sqs = MagicMock()
        mock_sqs.get_queue_url.return_value = {'QueueUrl': 'https://dummy-queue-url'}
        mock_sqs.send_message.side_effect = ClientError(
            error_response={'Error': {'Code': 'InternalError', 'Message': 'Something broke'}},
            operation_name='SendMessage'
        )
        mock_boto_client.return_value = mock_sqs

        try:
            publish_to_sqs(self.sample_articles)
        except Exception as e:
            self.fail(f"Function raised an unexpected exception: {e}")


if __name__ == "__main__":
    unittest.main()