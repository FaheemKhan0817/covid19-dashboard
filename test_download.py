import os
import requests

RAW_DATA_PATH = os.path.join(os.getcwd(), "data", "raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

urls = {
    "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
}

def download_data():
    for key, url in urls.items():
        raw_file = os.path.join(RAW_DATA_PATH, f"{key}.csv")
        print(f"Downloading {key} data to {raw_file}...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(raw_file, "wb") as f:
                f.write(response.content)

            print(f"✅ Successfully downloaded: {raw_file}")

        except requests.RequestException as e:
            print(f"❌ Failed to download {key}: {e}")

if __name__ == "__main__":
    download_data()
