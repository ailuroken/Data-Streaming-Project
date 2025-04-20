"""
This script retrieves the 10 latest articles that are relevent to the input from the Guardian API.
"""

from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

api_key = os.environ['API_KEY']

def content(input, date_from=None, date_to=None, broker_id="guardian_content"):
    """
    :param input: the desired search term
    :param date_from: optional date from which the articles are retrieved.
    :param date_from: optional date to which the articles are retrieved.
    :return: List of articles with their webPublicationDate, webTitle and webUrl in JSON format.
    """
    if not api_key:
        print("API_KEY not found")
        return []

    params = {
        "q": input,
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

print(content("machine learning"))
