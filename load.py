import os
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

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

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

for file in file_location:
    if file.endswith('.json'): #only upload the json files and never anything else incase something accidentally gets saved inside
        to_upload = f'{data_dir}/{file}'
        try:
            s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #file location, bucket name, file name
            print(f'File {file} successfully uploaded')
            os.remove(to_upload)
        except Exception as e:
            print(f'Something went wrong. Error {e}')