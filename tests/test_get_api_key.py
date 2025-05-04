import unittest
from unittest.mock import patch, Mock
from botocore.exceptions import ClientError
import json
from src.guardian_content import get_api_key

class TestGetApiKey(unittest.TestCase):

    @patch("src.guardian_content.boto3.client")
    def test_successful_retrieval(self, mock_boto_client):
        # Simulate Secrets Manager returning the correct secret
        mock_boto_client.return_value.get_secret_value.return_value = {
            "SecretString": json.dumps({"API_KEY": "test-api-key"})
        }

        result = get_api_key()
        self.assertEqual(result, "test-api-key")

    @patch("src.guardian_content.boto3.client")
    def test_secret_not_found(self, mock_boto_client):
        # Simulate ClientError for missing secret
        mock_boto_client.return_value.get_secret_value.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "ResourceNotFoundException",
                    "Message": "Secret not found"
                }
            },
            operation_name="GetSecretValue"
        )

        result = get_api_key()
        self.assertIsNone(result)

    @patch("src.guardian_content.boto3.client")
    def test_secret_string_not_json(self, mock_boto_client):
        # Simulate secret string being invalid JSON
        mock_boto_client.return_value.get_secret_value.return_value = {
            "SecretString": "not-a-json"
        }

        result = get_api_key()
        self.assertIsNone(result)

    @patch("src.guardian_content.boto3.client")
    def test_secret_missing_api_key(self, mock_boto_client):
        # Simulate JSON that doesn't include API_KEY
        mock_boto_client.return_value.get_secret_value.return_value = {
            "SecretString": json.dumps({"not_the_key": "value"})
        }

        result = get_api_key()
        self.assertIsNone(result)

    @patch("src.guardian_content.boto3.client")
    def test_secret_string_missing(self, mock_boto_client):
        # Simulate get_secret_value returning no SecretString at all
        mock_boto_client.return_value.get_secret_value.return_value = {}

        result = get_api_key()
        self.assertIsNone(result)

    @patch("src.guardian_content.boto3.client")
    def test_unexpected_exception(self, mock_boto_client):
        # Simulate any other unexpected exception
        mock_boto_client.return_value.get_secret_value.side_effect = Exception("Boom")

        result = get_api_key()
        self.assertIsNone(result)

