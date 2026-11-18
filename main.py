import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from function_extract import extract
from function_unzip import unzip
from function_load import load

#Logging: set up once and used everywhere
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # timestamp for the log file name
log_dir = 'logs/main'
os.makedirs(log_dir, exist_ok=True) # logging fails if the logs folder doesn't exist
log_filename = f'{log_dir}/main_{timestamp}.log'

logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8' # so emojis (💵 😁 💀) can be written to the log on Windows
)

logger = logging.getLogger()
logger.info('Logger was successfully initialised. Pipeline started.')

# read in api keys etc once and use anywhere
load_dotenv()

# Amplitude (extract)
url = 'https://analytics.eu.amplitude.com/api/2/export' # EU endpoint DONT USE STANDARD
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')

# AWS keys for load
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Shared between everyone for data_dir
data_dir = 'amplitude_data'
Test = False # True = pull 1 test hour

# Run the pipeline in order
zip_path = extract(url, api_key, secret_key, data_dir, Test)                      # API -> amplitude_data/zips/
json_path = unzip(data_dir)                                                        # zips/ -> json/, zip moved to done/
uploaded = load(data_dir, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME) # json/ -> S3, local JSON deleted

logger.info(f'Pipeline finished. Zip: {zip_path} | JSON folder: {json_path} | Files uploaded: {uploaded}')