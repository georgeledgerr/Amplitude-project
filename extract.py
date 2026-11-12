import os
import requests
import json
from datetime import datetime, timedelta, timezone # didnt know you could import several packages and name them one thing 
from dotenv import load_dotenv
import sys
import zipfile
import time

#timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #timestamp for our data and filename ----> no longer used
#print(timestamp)

data_dir = 'amplitude_data' #naming folder where data is stored
#I almost didnt add this to the .gitignore🤡
#os.makedirs(data_dir, exist_ok=True) #makes the file and exist_ok means that if it exists already then it doesnt break ------> Removed this because I am not trying to recreate the folder each time
#filename = f'{data_dir}/{timestamp}.zip' ----> Removed and moved down to loop
#this ran fine
#going to remove because i have added new gitignore

url='https://analytics.eu.amplitude.com/api/2/export' #EU endpoint DONT USE STANDARD
#Id like to put some error handling here incase the url changes for EU
#maybe a try and except?

load_dotenv()
api_key = os.getenv('AMP_API_KEY') #loads in api key (AMP_API_KEY has to match in here and .env(?))
secret_key = os.getenv('AMP_SECRET_KEY') #loads in secret key

#print(api_key)
#print(secret_key)
# API key printed successfully

#start_end = {'start': '20261111T12', 'end': '20261111T12'}  # one hour                                            rows 29-35 have been moved to a more dynamic testing place
# example from docs 'GET 'https://amplitude.com/api/2/export?start=20220101T00&end=20220101T23'

#response = requests.get(url, params=start_end, auth=(api_key, secret_key))

#print(response.status_code)
#response code works as 200 - good to go


#error handling if no API key present in .env
if not api_key or not secret_key: #this checks if the rows exist in the .env file
    print('Keys not found, check .env file :/💀')
    sys.exit(1) #abnormal error from my understanding, but it stops the run if no keys are found

Test = False  #for testing 1h vs on a schedule dynamically
 
if Test:
    start_time = '20261111T12'
    end_time = '20261111T12'
    #just pulls 1h of data as a test
else:
    yesterday_utc = datetime.now(timezone.utc) - timedelta(days=1)
    start_time = yesterday_utc.strftime('%Y%m%dT00')
    end_time = yesterday_utc.strftime('%Y%m%dT23')
    #testing done in test_dates.py and worked as expected

start_end = {'start': start_time, 'end': end_time}  # now dynamic and can either be in test or normal mode
# example from docs 'GET 'https://amplitude.com/api/2/export?start=20220101T00&end=20220101T23'

filename = f'{data_dir}/pull_{start_time}_{end_time}.zip' #how file name is being stored with no duplicates
print(f'Requesting {start_time} to {end_time}') #showing what is being requested

if os.path.exists(filename): #checks if file already exists and skips if it does (consideration)
    print(f'File {filename} already exists. Skipping download.')
    sys.exit()

attempt = 1
max_attempts = 3
delay_to_retry_seconds = 30

while attempt <= max_attempts:
    response = requests.get(url, params=start_end, auth=(api_key, secret_key), timeout=300) #timeout of 5 minutes added to avoid trying for too long
    status_code = response.status_code
 
    if status_code == 200:
            print("Huge w, data received 💵")
            break  # success so script can leave the loop and save
    if status_code == 404:
            print('404: no data for this range yet 💀')
            sys.exit(0)
    if status_code in (400, 401, 403): # 400 = wrong parameter format. 401 = wrong key. 403 = wrong key or wrong region 
            print(f'{status_code} - fix the request or check keys.')
            print(f'{response.text}')
            sys.exit(1)
        # left out codes 429 because its a rate limit and 5xx are due to the server end and can be retried
 
    if attempt < max_attempts:
        print(f'Retrying in {delay_to_retry_seconds}s')
        time.sleep(delay_to_retry_seconds)

    attempt+=1