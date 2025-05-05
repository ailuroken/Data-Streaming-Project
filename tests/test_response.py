from src.guardian_content import fetch_content
import unittest
from unittest.mock import patch, Mock
import requests
import boto3
from botocore.exceptions import ClientError


class TestContentFunction(unittest.TestCase):

    def setUp(self):
        self.sample_article = {
            "webPublicationDate": "2023-01-01T12:00:00Z",
            "webTitle": "Sample Title",
            "webUrl": "https://www.theguardian.com/sample-article",
            "fields": {"body": "Sample article body content..."},
        }

        self.formatted_article = {
            "webPublicationDate": "2023-01-01T12:00:00Z",
            "webTitle": "Sample Title",
            "webUrl": "https://www.theguardian.com/sample-article",
            "content_preview": "Sample article body content...",
        }

    def mock_secrets(self, mock_boto_client):
        mock_secret = {"SecretString": '{"API_KEY": "fake-key"}'}
        mock_boto_client.return_value.get_secret_value.return_value = mock_secret

    @patch("src.guardian_content.boto3.client")
    @patch("src.guardian_content.requests.get")
    def test_successful_response_single_article(self, mock_get, mock_boto_client):
        self.mock_secrets(mock_boto_client)
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"response": {"results": [self.sample_article]}},
        )
        mock_get.return_value.raise_for_status = Mock()

        result = fetch_content("machine learning", "2023-01-01")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.formatted_article)

    @patch("src.guardian_content.boto3.client")
    @patch("src.guardian_content.requests.get")
    def test_successful_response_multiple_articles(self, mock_get, mock_boto_client):
        self.mock_secrets(mock_boto_client)
        articles = [
            dict(
                self.sample_article, webTitle=f"Title {i}", fields={"body": f"body {i}"}
            )
            for i in range(5)
        ]
        mock_get.return_value = Mock(
            status_code=200, json=lambda: {"response": {"results": articles}}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = fetch_content("machine learning", "2023-01-01")
        self.assertEqual(len(result), 5)
        for i, article in enumerate(result):
            self.assertEqual(article["webTitle"], f"Title {i}")
            self.assertEqual(article["content_preview"], f"body {i}")

    @patch("src.guardian_content.boto3.client")
    @patch("src.guardian_content.requests.get")
    def test_no_results(self, mock_get, mock_boto_client):
        self.mock_secrets(mock_boto_client)
        mock_get.return_value = Mock(
            status_code=200, json=lambda: {"response": {"results": []}}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = fetch_content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch("src.guardian_content.boto3.client")
    @patch("src.guardian_content.requests.get")
    def test_http_error(self, mock_get, mock_boto_client):
        self.mock_secrets(mock_boto_client)
        mock_get.side_effect = requests.exceptions.RequestException("Failed request")
        result = fetch_content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch("src.guardian_content.boto3.client")
    @patch("src.guardian_content.requests.get")
    def test_invalid_json_structure(self, mock_get, mock_boto_client):
        self.mock_secrets(mock_boto_client)
        mock_get.return_value = Mock(
            status_code=200, json=lambda: {"bad_key": "no results here"}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = fetch_content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch("src.guardian_content.boto3.client")
    def test_missing_api_key(self, mock_boto_client):
        mock_boto_client.return_value.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": "SecretNotFound", "Message": "Secret not found"}},
            "GetSecretValue",
        )
        result = fetch_content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch("src.guardian_content.boto3.client")
    @patch("src.guardian_content.requests.get")
    def test_optional_parameters_are_none(self, mock_get, mock_boto_client):
        self.mock_secrets(mock_boto_client)
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"response": {"results": [self.sample_article]}},
        )
        mock_get.return_value.raise_for_status = Mock()

        result = fetch_content("machine learning")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.formatted_article)


if __name__ == "__main__":
    unittest.main()
