import os
import requests
import json
from datetime import datetime, timedelta, timezone, time # didnt know you could import several packages and name them one thing 
from dotenv import load_dotenv
import sys
import zipfile

data_dir = 'amplitude_data'

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

if os.path.exists(filename): #
    print(f'File {filename} already exists. Skipping download.')
else:
    print("ALL GOOD")

    #THIS WORKS