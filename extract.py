import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #timestamp for our data and filename
#print(timestamp)

data_dir = 'amplitude_data' #naming folder where data is stored
#I almost didnt add this to the .gitignore🤡
os.makedirs(data_dir, exist_ok=True) #makes the file and exist_ok means that if it exists already then it doesnt break
filename = f'{data_dir}/{timestamp}.json' #filepath i.e. goto the directory for this repo and save this file i.e. amplitude_data/
#this ran fine

url='https://analytics.eu.amplitude.com/api/2/export' #EU endpoint DONT USE STANDARD
#Id like to put some error handling here incase the url changes for EU
#maybe a try and except?

load_dotenv()
api_key = os.getenv('AMP_API_KEY') #loads in api key (AMP_API_KEY has to match in here and .env(?))
secret_key = os.getenv('AMP_SECRET_KEY') #loads in secret key

#print(api_key)
#print(secret_key)
# API key printed successfully

start_end = {'start': '20261111T12', 'end': '20261111T12'}  # one hour
# example from docs 'GET 'https://amplitude.com/api/2/export?start=20220101T00&end=20220101T23'

response = requests.get(url, params=start_end, auth=(api_key, secret_key))

print(response.status_code)
#response code works as 200 - good to go