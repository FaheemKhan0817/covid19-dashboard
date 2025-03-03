import os
import pandas as pd
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define file paths
BASE_DIR = os.getcwd()
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed")

# Ensure directories exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

# URLs for downloading COVID-19 datasets
urls = {
    "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
}

# Function to download data if missing
def download_data():
    for key, url in urls.items():
        raw_file = os.path.join(RAW_DATA_PATH, f"{key}.csv")
        
        if not os.path.exists(raw_file):  # Download only if file is missing
            logging.info(f"Downloading {key} data...")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(raw_file, "wb") as f:
                    f.write(response.content)
                logging.info(f"✅ Successfully downloaded {key}.csv")
            except requests.RequestException as e:
                logging.error(f"❌ Failed to download {key}: {e}")

# Function to process data
def process_data():
    download_data()  # Ensure data is available

    for key in urls.keys():
        raw_file = os.path.join(RAW_DATA_PATH, f"{key}.csv")
        processed_file = os.path.join(PROCESSED_DATA_PATH, f"{key}_processed.csv")

        try:
            logging.info(f"Processing {raw_file}...")
            df = pd.read_csv(raw_file)
            
            # Example cleaning: Removing empty columns
            df.dropna(axis=1, how="all", inplace=True)

            # Save processed data
            df.to_csv(processed_file, index=False)
            logging.info(f"✅ Processed data saved: {processed_file}")

        except Exception as e:
            logging.error(f"❌ Error in data processing: {e}")

if __name__ == "__main__":
    process_data()

    logging.info("✅ Data processing complete.")