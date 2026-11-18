import os
import sys
import zipfile
import gzip
import shutil
import tempfile
import logging
#from datetime import datetime   # MOVED to main.py (only used for the log file name)

logger = logging.getLogger() # NEW: uses the logger set up in main.py

def unzip(data_dir:str = 'amplitude_data'): # NEW: the whole script is now one function
    """Unzips every pull_*.zip in amplitude_data/zips, decompresses the .gz files into amplitude_data/json,
    then moves each finished zip into amplitude_data/done

    Args:
        data_dir (str): folder where the data is stored. Defaults to 'amplitude_data'

    Returns:
        str: path of the json folder, or None if there were no zips to unzip
    """

    #timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # timestamp for logging   # moved to main.py
     
    # Logging: same setup as extract.py, with 'unzip_' in front so the two scripts'   # moved to main.py
    #logger = logging.getLogger()   # moved -> now at the top of this file
    logger.info('Unzip started.') # was 'Logger was successfully initialised.' (main.py logs that now)
     
    #data_dir = 'amplitude_data'               # where extract.py saves the zips   # now an input (default 'amplitude_data')
    zips_dir = os.path.join(data_dir, 'zips') # the zips are now in amplitude_data/zips
    os.makedirs(zips_dir, exist_ok=True)      # stops os.listdir crashing if the folder isn't there yet
    done_dir = os.path.join(data_dir, 'done') # unzipped zips get moved here
    os.makedirs(done_dir, exist_ok=True)      # this script creates done/ (extract.py only reads it)
    json_dir = os.path.join(data_dir, 'json') # where the decompressed JSON files go
    os.makedirs(json_dir, exist_ok=True)
     
    # Find every zip extract.py has saved
    zip_files = sorted(f for f in os.listdir(zips_dir) if f.startswith('pull_') and f.endswith('.zip')) #lists each file name in the directory and checks it starts with pull and ends with .zip   # CHANGED: data_dir -> zips_dir, finished the comment
     
    if not zip_files:
        print(f'No pull_*.zip files found in {zips_dir}. Run extract.py first.') # data_dir -> zips_dir --> error handling if no zips are ready to be unzipped
        logger.warning(f'No pull_*.zip files found in {zips_dir}')               # data_dir -> zips_dir
        return None # was sys.exit(0). Ends unzip only, so load can still upload any leftover JSON
     
    print(f'Found {len(zip_files)} zip file(s) to unzip') # --> prints number of zipped files
    logger.info(f'Found {len(zip_files)} zip file(s): {zip_files}')
     
    failed = 0 # count failures so the exit code can say whether everything worked
     
    for zip_name in zip_files:
        zip_path = os.path.join(zips_dir, zip_name) # data_dir -> zips_dir --> loops through all the files for unzipping

        # skip this zip if it's already in done/ (it was unzipped on a previous run)
        if os.path.exists(os.path.join(done_dir, zip_name)):
            print(f'{zip_name} already unzipped previously (in {done_dir}). Skipping.')
            logger.warning(f'{zip_name} already in {done_dir}. Skipping.')
            continue # jump straight to the next zip in the loop

        temp_dir = tempfile.mkdtemp() # a fresh temporary folder for each zip
     
        try:
            # 1. Unzip into the temporary folder
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            logger.info(f'{zip_name} extracted to temp folder {temp_dir}')
     
            # 2. Find the numbered folder (Amplitude's project ID)
            id_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
            id_path = os.path.join(temp_dir, id_folder)
     
            # 3. Decompress every .gz file into amplitude_data/json/
            for root, _, files in os.walk(id_path):
                for file in files:
                    if file.endswith('.gz'):
                        gz_path = os.path.join(root, file)
                        json_filename = file[:-3] # remove the .gz extension
                        output_path = os.path.join(json_dir, json_filename)
     
                        with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                            shutil.copyfileobj(gz_file, out_file)
     
                        logger.info(f'Decompressed {file} -> {output_path}')
     
            print(f'Unzipped {zip_name} 😁')
            logger.info(f'Finished {zip_name}')

            # 4. move the zip into done/ so it isn't unzipped again (and is kept as a backup)
            shutil.move(zip_path, os.path.join(done_dir, zip_name)) # only reached if steps 1-3 worked, so a failed zip stays in zips/ to retry
            logger.info(f'Moved {zip_name} to {done_dir}')
     
        except StopIteration:
            # next() found no numbered folder inside the zip
            failed += 1
            print(f'{zip_name}: no numbered folder found inside the zip')
            logger.error(f'{zip_name}: no numbered folder found inside the zip')
        except Exception as e:
            # anything else (e.g. a corrupt zip): log it and move on to the next zip
            failed += 1
            print(f'{zip_name}: failed to unzip - {e}')
            logger.error(f'{zip_name}: failed to unzip - {e}')
        finally:
            # always delete the temporary folder, whether it worked or not
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f'Temp folder deleted for {zip_name}')
     
    if failed:
        print(f'{failed} zip file(s) failed. Check the log file') # log_filename now lives in main.py
        logger.error(f'{failed} of {len(zip_files)} zip file(s) failed')
        sys.exit(1)
     
    print(f'All files decompressed to {json_dir}')
    logger.info(f'All files decompressed to {json_dir}')
    return json_dir # hands the json folder back to main.py