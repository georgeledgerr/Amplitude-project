import logging
from function_unzip import unzip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # logs print in the terminal

result = unzip()   # uses the default data_dir = 'amplitude_data'
print(f'unzip returned: {result}')

#test 1 to see if it unzips, and moves file from zip/ to done/
# 2026-11-18 13:20:59,881 - INFO - Unzip started.
# Found 1 zip file(s) to unzip
# 2026-11-18 13:20:59,881 - INFO - Found 1 zip file(s): ['pull_20261111T12_20261111T12.zip']
# 2026-11-18 13:20:59,901 - INFO - pull_20261111T12_20261111T12.zip extracted to temp folder C:\Users\GEORGE~1\AppData\Local\Temp\tmp66dct5fy
# 2026-11-18 13:20:59,914 - INFO - Decompressed 100011471_2026-11-11_12#0.json.gz -> amplitude_data\json\100011471_2026-11-11_12#0.json
# Unzipped pull_20261111T12_20261111T12.zip 😁
# 2026-11-18 13:20:59,914 - INFO - Finished pull_20261111T12_20261111T12.zip
# 2026-11-18 13:20:59,918 - INFO - Moved pull_20261111T12_20261111T12.zip to amplitude_data\done
# 2026-11-18 13:20:59,918 - INFO - Temp folder deleted for pull_20261111T12_20261111T12.zip
# All files decompressed to amplitude_data\json
# 2026-11-18 13:20:59,918 - INFO - All files decompressed to amplitude_data\json
# unzip returned: amplitude_data\json

#test 2 - run with nothing inside zip/
# 2026-11-18 13:23:09,982 - INFO - Unzip started.
# No pull_*.zip files found in amplitude_data\zips. Run extract.py first.
# 2026-11-18 13:23:09,983 - WARNING - No pull_*.zip files found in amplitude_data\zips
# unzip returned: None

#test 3 - run with same file in zips
# 2026-11-18 13:24:12,132 - INFO - Unzip started.
# Found 1 zip file(s) to unzip
# 2026-11-18 13:24:12,132 - INFO - Found 1 zip file(s): ['pull_20261111T12_20261111T12.zip']
# pull_20261111T12_20261111T12.zip already unzipped previously (in amplitude_data\done). Skipping.
# 2026-11-18 13:24:12,132 - WARNING - pull_20261111T12_20261111T12.zip already in amplitude_data\done. Skipping.
# All files decompressed to amplitude_data\json
# 2026-11-18 13:24:12,132 - INFO - All files decompressed to amplitude_data\json
# unzip returned: amplitude_data\json

#test 4 - created fake zip to see if it gets ignored in processing and deletes it
# 2026-11-18 13:27:02,369 - INFO - Unzip started.
# Found 2 zip file(s) to unzip
# 2026-11-18 13:27:02,369 - INFO - Found 2 zip file(s): ['pull_20261111T12_20261111T12.zip', 'pull_zip.zip']
# pull_20261111T12_20261111T12.zip already unzipped previously (in amplitude_data\done). Skipping.
# 2026-11-18 13:27:02,369 - WARNING - pull_20261111T12_20261111T12.zip already in amplitude_data\done. Skipping.
# pull_zip.zip: failed to unzip - File is not a zip file
# 2026-11-18 13:27:02,369 - ERROR - pull_zip.zip: failed to unzip - File is not a zip file
# 2026-11-18 13:27:02,369 - INFO - Temp folder deleted for pull_zip.zip
# 1 zip file(s) failed. Check the log file
# 2026-11-18 13:27:02,369 - ERROR - 1 of 2 zip file(s) failed
