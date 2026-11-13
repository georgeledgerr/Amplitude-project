# =====================================================================
# unzip.py: turn the zips from extract.py into readable JSON files
#
# What an Amplitude zip looks like inside (like a set of nesting boxes):
#   pull_20261111T12_20261111T12.zip      <- box 1: the zip
#     └── 100011471/                      <- box 2: a folder named with a number (the project ID)
#           ├── ..._2026-11-11_12#0.json.gz   <- box 3: compressed files
#           └── ..._2026-11-11_12#1.json.gz
#
# This script opens every box and saves the JSON files inside to amplitude_data/json/
# =====================================================================

import os         # work with folders and file paths
import sys        # sys.exit() to stop the script with an exit code
import zipfile    # open .zip files (box 1)
import gzip       # open .gz files (box 3)
import shutil     # copy file contents, and delete whole folders
import tempfile   # make a throwaway folder to unzip into
import logging    # write a log file, like extract.py
from datetime import datetime


# ---------- STEP 0: logging (same pattern as extract.py) ----------
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # e.g. '2026-11-13 11-55-00', used in the log file name

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)  # make the logs folder if it isn't there (logging crashes without it)
log_filename = f'{log_dir}/unzip_{timestamp}.log'  # 'unzip_' so you can tell these logs apart from extract.py's

logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',  # each log line: time - level - message
    level=logging.INFO                                   # record INFO and anything more serious
)

logger = logging.getLogger()
logger.info('Logger was successfully initialised.')


# ---------- STEP 1: set up the folders ----------
data_dir = 'amplitude_data'                # where extract.py saved the zips
json_dir = os.path.join(data_dir, 'json')  # where the JSON files will go: 'amplitude_data/json'
                                           # (os.path.join glues folder names together with the right slash)
os.makedirs(json_dir, exist_ok=True)       # make the json folder if it isn't there


# ---------- STEP 2: find the zips to unzip ----------
# Look at every name in amplitude_data/ and keep only the ones that
# start with 'pull_' AND end with '.zip', then sort them (oldest date first).
# Long-hand version:
#   zip_files = []
#   for f in os.listdir(data_dir):
#       if f.startswith('pull_') and f.endswith('.zip'):
#           zip_files.append(f)
#   zip_files.sort()
zip_files = sorted(f for f in os.listdir(data_dir) if f.startswith('pull_') and f.endswith('.zip'))

# No zips found = nothing to do. Not an error, so exit code 0.
if not zip_files:
    print(f'No pull_*.zip files found in {data_dir}. Run extract.py first.')
    logger.warning(f'No pull_*.zip files found in {data_dir}')
    sys.exit(0)

print(f'Found {len(zip_files)} zip file(s) to unzip')  # len() = how many items are in the list
logger.info(f'Found {len(zip_files)} zip file(s): {zip_files}')

failed = 0  # a counter: goes up by 1 every time a zip fails, so we know at the end if anything went wrong


# ---------- STEP 3: unzip each zip, one at a time ----------
for zip_name in zip_files:                       # e.g. zip_name = 'pull_20261111T12_20261111T12.zip'
    zip_path = os.path.join(data_dir, zip_name)  # full path: 'amplitude_data/pull_..._.zip'
    temp_dir = tempfile.mkdtemp()                # make a brand-new empty throwaway folder for this zip

    try:  # try all of this; if anything goes wrong, jump to the matching 'except' below

        # --- 3a. Open box 1: unzip everything into the throwaway folder ---
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:  # 'r' = read. 'with' closes the zip when done
            zip_ref.extractall(temp_dir)                 # extract every file inside into temp_dir
        logger.info(f'{zip_name} extracted to temp folder {temp_dir}')

        # --- 3b. Find box 2: the folder whose name is all digits (the project ID) ---
        # Same pattern as STEP 2, but next() takes just the FIRST match instead of building a list.
        # If there's no match at all, next() raises StopIteration (handled below).
        id_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())  # .isdigit() = "is this text all numbers?"
        id_path = os.path.join(temp_dir, id_folder)                        # full path to that folder

        # --- 3c. Open box 3: decompress every .gz file ---
        # os.walk goes through a folder AND all folders inside it.
        # Each time round it gives: root  = the folder it's currently in
        #                           _     = the sub-folders (not needed, so named _ meaning "ignore this")
        #                           files = the list of files in that folder
        for root, _, files in os.walk(id_path):
            for file in files:
                if file.endswith('.gz'):                           # only the compressed files
                    gz_path = os.path.join(root, file)             # where the .gz file is
                    json_filename = file[:-3]                      # chop the last 3 characters ('.gz') off the name
                    output_path = os.path.join(json_dir, json_filename)  # where the JSON file will be saved

                    # Open the .gz for reading and a new file for writing, both as bytes ('rb'/'wb'),
                    # then copy everything across. gzip.open un-compresses as it reads.
                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                        shutil.copyfileobj(gz_file, out_file)

                    logger.info(f'Decompressed {file} -> {output_path}')

        print(f'Unzipped {zip_name} 😁')
        logger.info(f'Finished {zip_name}')

    except StopIteration:
        # 3b found no all-digits folder inside the zip
        failed += 1
        print(f'{zip_name}: no numbered folder found inside the zip')
        logger.error(f'{zip_name}: no numbered folder found inside the zip')

    except Exception as e:
        # anything else went wrong (e.g. the zip is broken). Log it and carry on with the next zip
        failed += 1
        print(f'{zip_name}: failed to unzip - {e}')
        logger.error(f'{zip_name}: failed to unzip - {e}')

    finally:
        # 'finally' ALWAYS runs, whether the try worked or failed:
        # delete the throwaway folder so they don't pile up
        shutil.rmtree(temp_dir, ignore_errors=True)  # rmtree = delete a folder and everything in it
        logger.info(f'Temp folder deleted for {zip_name}')


# ---------- STEP 4: finish with the right exit code ----------
if failed:  # failed is more than 0, so at least one zip went wrong
    print(f'{failed} zip file(s) failed. Check {log_filename}')
    logger.error(f'{failed} of {len(zip_files)} zip file(s) failed')
    sys.exit(1)  # 1 = something needs looking at

print(f'All files decompressed to {json_dir}')
logger.info(f'All files decompressed to {json_dir}')
# reaching the end normally = exit code 0 (success)