import os
import sys # NEW: for sys.exit(1)
import boto3
import logging
#from datetime import datetime    # moved to main.py (only used for the log file name)
#from dotenv import load_dotenv   # moved to main.py: main reads the .env and passes the keys in

logger = logging.getLogger() #uses the logger set up in main.py

def load(data_dir:str, AWS_ACCESS_KEY:str, AWS_SECRET_ACCESS_KEY:str, AWS_BUCKET_NAME:str): # the whole script is now one function
    """Uploads every .json file in amplitude_data/json to the S3 bucket, deleting each local copy once uploaded

    Args:
        data_dir (str): folder where the data is stored, e.g. 'amplitude_data'
        AWS_ACCESS_KEY (str): AWS access key
        AWS_SECRET_ACCESS_KEY (str): AWS secret access key
        AWS_BUCKET_NAME (str): S3 bucket to upload to

    Returns:
        int: number of files uploaded, or None if there was nothing to upload
    """

    #timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')   # moved to main.py
    #log_dir = 'logs'
    #os.makedirs(log_dir, exist_ok=True)
    #logging.basicConfig(
    #    filename=f'{log_dir}/load_{timestamp}.log',
    #    format='%(asctime)s - %(levelname)s - %(message)s',
    #    level=logging.INFO
    #)
    #logger = logging.getLogger()   # now at the top of this file
    logger.info('Load started.') # was 'Load script started.'

    #load_dotenv()   # MOVED to main.py
    #AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')               # now an input
    #AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY') # now an input
    #AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')             # now an input

    # error handling - checks if aws keys or bucket name exists - validated ✅
    if not AWS_ACCESS_KEY:
        print('AWS_ACCESS_KEY missing from .env')
        logger.error('AWS_ACCESS_KEY missing from .env')
        sys.exit(1) # was exit(), which reports success to Kestra
    if not AWS_SECRET_ACCESS_KEY:
        logger.error('AWS_SECRET_ACCESS_KEY missing from .env')
        print('AWS_SECRET_ACCESS_KEY missing from .env')
        sys.exit(1) # was exit()
    if not AWS_BUCKET_NAME:
        logger.error('AWS_BUCKET_NAME missing from .env')
        print('AWS_BUCKET_NAME missing from .env')
        sys.exit(1) # was exit()

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

    #data_dir = 'amplitude_data/json'   # data_dir is now the input ('amplitude_data'), json folder built below
    json_dir = os.path.join(data_dir, 'json') # amplitude_data/json
    os.makedirs(json_dir, exist_ok=True)      # stops os.listdir crashing if the folder isn't there yet
    file_location = os.listdir(json_dir) # data_dir -> json_dir
    logger.info(f'{len(file_location)} file(s) found in {json_dir}') # data_dir -> json_dir

    if not any(file.endswith('.json') for file in file_location): # nothing to upload
        print(f'No .json files in {json_dir}. Nothing to upload.')
        logger.warning(f'No .json files in {json_dir}. Nothing to upload.')
        return None # ends load only, not an error

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
        sys.exit(1) # was exit(). Stops the script here, nothing gets uploaded or deleted

    uploaded = 0 # count successes
    failed = 0   # count failures, like unzip

    for file in file_location:
        if file.endswith('.json'): #only upload the json files and never anything else incase something accidentally gets saved inside
            to_upload = f'{json_dir}/{file}' # data_dir -> json_dir
            try:
                s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file) #file location, bucket name, file name
                print(f'File {file} successfully uploaded')
                logger.info(f'File {file} successfully uploaded')
                os.remove(to_upload)
                uploaded += 1 #counts number of files uploaded to s3 bucket
            except Exception as e:
                print(f'Something went wrong with {file}. Error {e}')
                logger.error(f'Something went wrong with {file}. Error {e}')
                failed += 1 #counts number of failures to s3 bucket

    if failed: # tell Kestra if any upload failed (the files stay in json/ to retry next run)
        print(f'{failed} file(s) failed to upload. Check the log file')
        logger.error(f'{failed} file(s) failed to upload, {uploaded} uploaded')
        sys.exit(1)

    logger.info(f'Load finished. {uploaded} file(s) uploaded.') # was 'Load script finished.'
    return uploaded # hands the count back to main.py