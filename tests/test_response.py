"""
Tests for the app.py
"""

from content.app import content
import unittest
from unittest.mock import patch, Mock
import os
import requests

class TestContentFunction(unittest.TestCase):

    def setUp(self):
        self.sample_article = {
            "webPublicationDate": "2023-01-01T12:00:00Z",
            "webTitle": "Sample Title",
            "webUrl": "https://www.theguardian.com/sample-article",
            "content_preview": ""
        }

    @patch.dict(os.environ, {'API_KEY': 'fake-key'})
    @patch('content.app.requests.get')
    def test_successful_response_single_article(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                "response": {
                    "results": [self.sample_article]
                }
            }
        )
        mock_get.return_value.raise_for_status = Mock()

        result = content("machine learning", "2023-01-01")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.sample_article)

    @patch.dict(os.environ, {'API_KEY': 'fake-key'})
    @patch('content.app.requests.get')
    def test_successful_response_multiple_articles(self, mock_get):
        articles = [dict(self.sample_article, webTitle=f"Title {i}") for i in range(5)]
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"response": {"results": articles}}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = content("machine learning", "2023-01-01")

        self.assertEqual(len(result), 5)
        for i, article in enumerate(result):
            self.assertEqual(article["webTitle"], f"Title {i}")

    @patch.dict(os.environ, {'API_KEY': 'fake-key'})
    @patch('content.app.requests.get')
    def test_no_results(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"response": {"results": []}}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch.dict(os.environ, {'API_KEY': 'fake-key'})
    @patch('content.app.requests.get')
    def test_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Failed request")
        result = content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch.dict(os.environ, {'API_KEY': 'fake-key'})
    @patch('content.app.requests.get')
    def test_invalid_json_structure(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"bad_key": "no results here"}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch('content.app.os.environ', side_effect=KeyError("API_KEY not found"))
    def test_missing_api_key(self, mock_environ):
        result = content("machine learning", "2023-01-01")
        self.assertEqual(result, [])

    @patch.dict(os.environ, {'API_KEY': 'fake-key'})
    @patch('content.app.requests.get')
    def test_optional_parameters_are_none(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"response": {"results": [self.sample_article]}}
        )
        mock_get.return_value.raise_for_status = Mock()

        result = content("machine learning")
        self.assertEqual(len(result), 1)
