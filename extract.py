import os
import requests
import json
from datetime import datetime, timedelta, timezone # didnt know you could import several packages and name them one thing 
from dotenv import load_dotenv
import sys
import zipfile
import time
import logging

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') #timestamp for logging
#print(timestamp)

data_dir = 'amplitude_data' #naming folder where data is stored
#I almost didnt add this to the .gitignore🤡
#os.makedirs(data_dir, exist_ok=True) #makes the file and exist_ok means that if it exists already then it doesnt break ------> Removed this because I am not trying to recreate the folder each time
#filename = f'{data_dir}/{timestamp}.zip' ----> Removed and moved down to loop
#this ran fine
#going to remove because i have added new gitignore

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True) # logging fails if the logs folder doesn't exist
log_filename = f'{log_dir}/{timestamp}.log'
 
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
 
logger = logging.getLogger()
logger.info('Logger was successfully initialised.')

url='https://analytics.eu.amplitude.com/api/2/export' #EU endpoint DONT USE STANDARD
#Id like to put some error handling here incase the url changes for EU
#maybe a try and except?

if 'analytics.eu.amplitude.com' not in url: # URL check because our API key does not work for NA
    print(f'URL is not for the EU endpoint - {url}')
    logger.error(f'URL is not for the EU endpoint - {url}')
    sys.exit(1)

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
    logger.error('Keys not found, check .env file :/💀') # logging
    sys.exit(1) #abnormal error from my understanding, but it stops the run if no keys are found

Test = True  #for testing 1h vs on a schedule dynamically
 
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
logger.info(f'Requesting {start_time} to {end_time}. Test mode - {Test}')

if os.path.exists(filename): #checks if file already exists and skips if it does (consideration)
    print(f'File {filename} already exists. Skipping download.')
    logger.info(f'File {filename} already exists. Skipping download.')
    sys.exit(0)

attempt = 1
max_attempts = 3
delay_to_retry_seconds = 30

while attempt <= max_attempts:
    response = requests.get(url, params=start_end, auth=(api_key, secret_key), timeout=300) #timeout of 5 minutes added to avoid trying for too long
    status_code = response.status_code
    logger.info(f'Attempt {attempt}. Status code = {status_code}')
 
    if status_code == 200:
            print('This could change everything, data received 💵')
            logger.info('This could change everything, data received 💵') 
            break  # success so script can leave the loop and save
    if status_code == 404:
            print('404: no data for this range yet - make sure you are not requesting data sooner than 2 hours ago💀')
            logger.warning('404: no data for this range yet 💀')
            sys.exit(0)
    if status_code in (400, 401, 403): # 400 = wrong parameter format. 401 = wrong key. 403 = wrong key or wrong region 
            print(f'{status_code} - fix the request or check keys.')
            print(f'{response.text}')
            logger.error(f'{status_code} - fix the request or check keys.')
            logger.error(f'{response.text}')
            sys.exit(1)
        # left out codes 429 because its a rate limit and 5xx are due to the server end and can be retried
 
    if attempt < max_attempts:
        print(f'Retrying in {delay_to_retry_seconds}s')
        time.sleep(delay_to_retry_seconds)
        logger.warning(f'Attempt {attempt} failed, status code {status_code}. Retrying API call in {delay_to_retry_seconds}s')

    if attempt == max_attempts:
        print('Max attempts reached, please investigate 🗿')
        logger.error(f'Max attempts reached. Status code {status_code}. Please investigate 🗿')
        sys.exit(1)

    attempt+=1

# else:
#     print('Max attempts reached, please investigate 🗿') #only reaches here if the while loop isnt broken
#     sys.exit(1)
#     #why doesnt this fail?
#     #this needs to be happening inside the loop
 
with open(filename, 'wb') as file: #write file to the filename path and write bytes because its a zip file, JSON DIDNT WORK
    #with allows the file to be closed automatically after it is done, so no need to close it manually
    file.write(response.content)
 
if zipfile.is_zipfile(filename): #a quick check to see if the zip file was truncated and would appear as incomplete
    #apparently  a zips index is at the end of the file and a partial file would fail this check 
    print(f'Saved successfully 😁: {filename}')
    logger.info(f'Saved successfully 😁: {filename}')
else:
    print(f'{filename} is not a valid zip')
    logger.error(f'{filename} is not a valid zip. Deleting to retry API call for complete file')
    os.remove(filename) #removes the file if its not a valid zip - also, in case of a partial download, this will remove the file so that it can be retried next time
    sys.exit(1)