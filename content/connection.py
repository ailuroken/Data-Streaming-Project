import os
import requests
import json


# Create your create_conn function to return a database connection object    #


api_key = os.environ['API_KEY']
def content(input, date_from):
    from_date = date_from
    url = f"http://content.guardianapis.com/search?q={input}/{input}&from-date={from_date}&api-key={api_key}"
    response = requests.get(url)
    data = response.json()

def get_content():