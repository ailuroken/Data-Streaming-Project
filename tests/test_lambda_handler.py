import unittest
from unittest.mock import patch, MagicMock
from src.guardian_content import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    @patch("src.guardian_content.fetch_content")
    def test_handler_with_defaults(self, mock_fetch):
        mock_fetch.return_value = [{"webTitle": "Test Article"}]
        event = {}

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Published 1 articles", response["body"])

    @patch("src.guardian_content.fetch_content")
    def test_handler_with_custom_input(self, mock_fetch):
        mock_fetch.return_value = [{"webTitle": "Another Article"}] * 5
        event = {
            "search_term": "climate change",
            "date_from": "2023-04-01",
            "date_to": "2023-04-02",
        }

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Published 5 articles", response["body"])

    @patch("src.guardian_content.fetch_content")
    def test_handler_with_no_results(self, mock_fetch):
        mock_fetch.return_value = []
        event = {"search_term": "somethingobscure"}

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Published 0 articles", response["body"])

    @patch("src.guardian_content.fetch_content", side_effect=Exception("API failure"))
    def test_handler_with_exception(self, mock_fetch):
        event = {"search_term": "news"}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("API failure", response["body"])
