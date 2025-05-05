'''

'''

import os
import requests
import json
import boto3
from botocore.exceptions import ClientError
from src.sqs_publisher import publish_to_sqs

def get_api_key():
    try:
        secret = boto3.client("secretsmanager").get_secret_value(SecretId="guardianApiKey")
        return json.loads(secret["SecretString"])["API_KEY"]
    except (ClientError, KeyError, json.JSONDecodeError) as e:
        print(f"Handled error retrieving API key: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


def fetch_content(search_term, date_from=None, date_to=None, broker_id="guardian_content"):
    """
    Fetch the latest content from the Guardian API and return formatted articles.
    """
    api_key = get_api_key()
    
    if not api_key:
        print("API_KEY not found")
        return []

    params = {
        "q": search_term,
        "from-date": date_from,
        "to-date": date_to,
        "order-by": "newest",
        "page-size": 10,
        "show-fields": "headline,body",
        "api-key": api_key
    }
    url = "https://content.guardianapis.com/search"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json()["response"]["results"]
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching articles: {e}")
        return []

    formatted_articles = []
    for article in articles:
        body = article.get("fields", {}).get("body", "")
        preview = body[:1000] if body else ""
        formatted = {
            "webPublicationDate": article["webPublicationDate"],
            "webTitle": article["webTitle"],
            "webUrl": article["webUrl"],
            "content_preview": preview
        }
        formatted_articles.append(formatted)
    
    # Publish articles to SQS after fetching
    publish_to_sqs(formatted_articles)  # Call the helper function

    return formatted_articles  

def lambda_handler(event, context):
    try:
        search_term = event.get('search_term', 'machine learning')
        date_from = event.get('date_from', '2023-01-01')
        date_to = event.get('date_to', '2023-01-02')

        articles = fetch_content(search_term, date_from=date_from, date_to=date_to)

        return {
            "statusCode": 200,
            "body": f"Published {len(articles)} articles to SQS"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }