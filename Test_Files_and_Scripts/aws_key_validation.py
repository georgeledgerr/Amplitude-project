import os
import boto3
import logging
from datetime import datetime 
from dotenv import load_dotenv

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=f'{log_dir}/load_{timestamp}.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()
logger.info('Load script started.')

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# error handling - checks if aws keys or bucket name exists - validated
if not AWS_ACCESS_KEY:
    print('AWS_ACCESS_KEY missing from .env')
    logger.error('AWS_ACCESS_KEY missing from .env')
if not AWS_SECRET_ACCESS_KEY:
    logger.error('AWS_SECRET_ACCESS_KEY missing from .env')
    print('AWS_SECRET_ACCESS_KEY missing from .env')
if not AWS_BUCKET_NAME:
    logger.error('AWS_BUCKET_NAME missing from .env')
    print('AWS_BUCKET_NAME missing from .env')


    # check the keys and bucket work before uploading anything
try:
    s3_client.head_bucket(Bucket=AWS_BUCKET_NAME) #asks AWS "can I access this bucket?"
    print('AWS keys and bucket OK')
    logger.info('AWS keys and bucket OK')
except Exception as e:
    print(f'Cannot access the bucket, KILLING SCRIPT. Error {e}')
    logger.critical(f'Cannot access the bucket, KILLING SCRIPT. Error {e}')
    exit() # stops the script here, nothing gets uploaded or deleted