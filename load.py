import os
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# testing if it prints from .env file
# print(AWS_ACCESS_KEY)
# print(AWS_SECRET_ACCESS_KEY)
# print(AWS_BUCKET_NAME)