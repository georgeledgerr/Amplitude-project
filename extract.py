import os
import requests
import json
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #timestamp for our data and filename
#print(timestamp)

data_dir = 'amplitude_data' #naming folder where data is stored
os.makedirs(data_dir, exist_ok=True) #makes the file and exist_ok means that if it exists already then it doesnt break
filename = f'{data_dir}/{timestamp}.json' #filepath i.e. goto the directory for this repo and save this file i.e. amplitude_data/...
#this ran fine