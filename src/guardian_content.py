import os
import requests
import json
import boto3
from botocore.exceptions import ClientError

def get_api_key():
    try:
        secret = boto3.client("secretsmanager").get_secret_value(SecretId="guardianApiKey")
        return json.loads(secret["SecretString"])["API_KEY"]
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        return None
    except KeyError as e:
        print(f"API key missing in secret: {e}")
        return None

def fetch_content(search_term, date_from=None, date_to=None, broker_id="guardian_content"):
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
    
    return formatted_articles
