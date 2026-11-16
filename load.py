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

# error handling - checks if aws keys or bucket name exists - validated ✅
if not AWS_ACCESS_KEY:
    print('AWS_ACCESS_KEY missing from .env')
    logger.error('AWS_ACCESS_KEY missing from .env')
    exit()
if not AWS_SECRET_ACCESS_KEY:
    logger.error('AWS_SECRET_ACCESS_KEY missing from .env')
    print('AWS_SECRET_ACCESS_KEY missing from .env')
    exit()
if not AWS_BUCKET_NAME:
    logger.error('AWS_BUCKET_NAME missing from .env')
    print('AWS_BUCKET_NAME missing from .env')
    exit()

# testing if it prints from .env file - it works ✅
# print(AWS_ACCESS_KEY)
# print(AWS_SECRET_ACCESS_KEY)
# print(AWS_BUCKET_NAME)

# testing if I can upload a hard-coded json file to aws bucket - it works ✅
# data_dir = 'amplitude_data/json'
# test_file = '100011471_2026-11-11_12#0.json'
# file_location = os.listdir(data_dir)

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )

# s3_client.upload_file(f'{data_dir}/{test_file}', AWS_BUCKET_NAME, test_file) #file location, bucket name, file name
# print(f'File {test_file} successfully uploaded')

data_dir = 'amplitude_data/json'
file_location = os.listdir(data_dir)
logger.info(f'{len(file_location)} file(s) found in {data_dir}')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# check the keys and bucket work before uploading anything - validated ✅
try:
    s3_client.head_bucket(Bucket=AWS_BUCKET_NAME) #checks whether python can access the AWS bucket and if it exists --> https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/head_bucket.html
    print('AWS keys and bucket are okay 👍')
    logger.info('AWS keys and bucket are okay')
except Exception as e:
    print(f'Cannot access the bucket, KILLING SCRIPT. Error {e}')
    logger.critical(f'Cannot access the bucket, KILLING SCRIPT. Error {e}')
    exit() # stops the script here, nothing gets uploaded or deleted

for file in file_location:
    if file.endswith('.json'): #only upload the json files and never anything else incase something accidentally gets saved inside
        to_upload = f'{data_dir}/{file}'
        try:
            s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #file location, bucket name, file name
            print(f'File {file} successfully uploaded')
            logger.info(f'File {file} successfully uploaded')
            os.remove(to_upload)
        except Exception as e:
            print(f'Something went wrong with {file}. Error {e}')
            logger.error(f'Something went wrong with {file}. Error {e}')

logger.info('Load script finished.')