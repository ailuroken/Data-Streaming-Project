import os
import requests
import json


# Create your create_conn function to return a database connection object    #


api_key = os.environ['API_KEY']
def content(input, date_from):
    endpoint = input
    url = f"http://content.guardianapis.com/search?q={endpoint}&api-key={api_key}"
    response = requests.get(url)
    data = response.json()

def get_content():