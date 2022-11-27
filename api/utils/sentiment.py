import requests
from dotenv import load_dotenv
import os

load_dotenv()

def sentiment_analysis(text: str):
    """ Sentiment analysis from Azure Text Analytics API """
    # Azure API key
    subscription_key = os.getenv('AZURE_API_KEY')
    # Azure API endpoint
    endpoint = os.getenv("AZURE_ENDPOINT")
    # Azure API path
    path = os.getenv("AZURE_PATH")
    headers = {
		# Already added when you pass json=
		# 'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}
    params = {
		'api-version': '2022-05-01',
	}
    json_data = {
		'kind': 'SentimentAnalysis',
		'analysisInput': {
			'documents': [
				{
					'id': 'documentId',
					'text': text,
					'language': 'es',
				},
			],
		},
		'parameters': {
			'opinionMining': True,
		},
	}
    response = requests.post(f"{endpoint}{path}", headers=headers, params=params, json=json_data)
    return response.json()['results']['documents'][0]['sentiment']