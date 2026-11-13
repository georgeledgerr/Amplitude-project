import os
import requests
import json
from datetime import datetime, timedelta, timezone # didnt know you could import several packages and name them one thing 
from dotenv import load_dotenv
import sys

Test = False  #for testing 1h vs on a schedule dynamically
 
if Test:
    start_time = '20261111T12'
    end_time = '20261111T12'
    #just pulls 1h of data as a test
else:
    yesterday_utc = datetime.now(timezone.utc) - timedelta(days=1)
    print(yesterday_utc)
    
    start_time = yesterday_utc.strftime('%Y%m%dT00')
    print(start_time)
    end_time = yesterday_utc.strftime('%Y%m%dT23')
    print(end_time)