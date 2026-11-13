# Amplitude Project

Amplitude is my Data Engineering project during my training at TIL.

The project pulls website event data from the Amplitude API.

**Status (13 November 2026) -** the extraction phase has been complete.

## What it does

`extract.py` calls the Amplitude Export API (EU endpoint) and saves the response as a zip file in `amplitude_data/`.

- **Normal mode** pulls all of yesterday's data (UTC, `T00` to `T23`). The plan is to run it daily at 6am because Amplitude can take up to 2 hours to make data available, so yesterday is always ready by then.
- **Test mode** (`Test = True` in `extract.py`) pulls one hour.

The script also does/features:

- **Duplication Handling:** Skips the download if a file for that date range already exists
- **URL Errors:** Checks the URL to make sure we are using the connecting to the correct endpoint
- **Soft errors:** Treats `404` (no data for the range yet) as a warning, not a failure
- **Hard errors:** Stops on `400`, `401` or `403`, which mean the request or keys need fixing
- **Retry logic:** Retries up to 3 times on `429` (rate limit) or server errors
- **File Validtaion:** Checks the saved file is a valid zip, and deletes it if not so the next run tries again

Still needs doing:

NA

Files are named by date range, e.g. `amplitude_data/pull_20261111T00_20261111T23.zip`.

## Setup

1. Clone the repo and open the folder in a terminal.
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the packages:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your Amplitude keys. It's git-ignored, so it never goes to GitHub:
   ```
   AMP_API_KEY=your_api_key
   AMP_SECRET_KEY=your_secret_key
   ```

## Running it

```
python extract.py
```

Set `Test = True` or `False` at the top of the date section in `extract.py` to choose between test mode and normal mode.

| Path | What it is |
|---|---|
| `extract.py` | The extraction script |
| `amplitude_data/` | Where downloaded zips are saved. Its contents are git-ignored; the folder ships with the repo |
| `requirements.txt` | Python packages needed |
| `Test_Files_and_Scripts/` | Scripts and dummy files used to test parts of the code |
| `Test_Files_and_Scripts/test_dates.py` | Tests the "yesterday in UTC" date logic |
| `Test_Files_and_Scripts/test_zip.py` | Tests the zip check against `valid.zip` and `invalid.zip` |
| `Test_Files_and_Scripts/testing_dupe.py` | Tests the "already pulled" check that skips duplicate downloads |
| `Test_Files_and_Scripts/valid.zip`, `invalid.zip` | Dummy zips (complete and cut off) for `test_zip.py` |