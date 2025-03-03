"""
Airflow DAG to download and process COVID-19 data from Johns Hopkins GitHub repository.
This pipeline handles both data ingestion and processing in a single workflow.

Created by: FaheemKhan0817
Last updated: 2025-03-03 08:01:20
"""
import os
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# DAG metadata
OWNER = "FaheemKhan0817"
PIPELINE_TIMESTAMP = "2025-03-03 08:01:20"

# Define default arguments for the DAG
default_args = {
    'owner': OWNER,
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'covid19_data_pipeline',
    default_args=default_args,
    description='Download and process COVID-19 data from JHU CSSE repository',
    schedule_interval='0 0 * * *',  # Run daily at midnight
    start_date=days_ago(1),
    tags=['covid19', 'data_pipeline', 'jhu_csse'],
)

# Define the data sources
urls = {
    "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
}

# Define file paths using Airflow's variables
def get_file_paths():
    """Generate file paths for raw and processed data directories."""
    airflow_home = os.environ.get('AIRFLOW_HOME', '/opt/airflow')
    raw_data_path = os.path.join(airflow_home, "data", "raw")
    processed_data_path = os.path.join(airflow_home, "data", "processed")
    
    # Create directories if they don't exist
    for path in [raw_data_path, processed_data_path]:
        os.makedirs(path, exist_ok=True)
    
    return raw_data_path, processed_data_path

def download_dataset(dataset_type, url, **kwargs):
    """Download a specific COVID-19 dataset and save as CSV."""
    raw_data_path, _ = get_file_paths()
    raw_file = os.path.join(raw_data_path, f"{dataset_type}.csv")
    
    logger.info(f"Downloading {dataset_type} data to {raw_file}...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(raw_file, "wb") as f:
            f.write(response.content)

        logger.info(f"✅ Successfully downloaded: {raw_file}")
        
        # Pass the file path to the next task via XCom
        kwargs['ti'].xcom_push(key=f'{dataset_type}_raw_file', value=raw_file)
        return True
    
    except requests.RequestException as e:
        logger.error(f"❌ Failed to download {dataset_type}: {e}")
        raise

def process_dataset(dataset_type, **kwargs):
    """Process a COVID-19 dataset."""
    raw_data_path, processed_data_path = get_file_paths()
    
    # Attempt to get the file path from XCom, fall back to constructing it
    ti = kwargs['ti']
    raw_file = ti.xcom_pull(task_ids=f'ingest_data.download_{dataset_type}_data', 
                           key=f'{dataset_type}_raw_file')
    
    if not raw_file:
        raw_file = os.path.join(raw_data_path, f"{dataset_type}.csv")
    
    processed_file = os.path.join(processed_data_path, f"{dataset_type}_processed.csv")
    
    try:
        logger.info(f"Processing {raw_file}...")
        
        # Check if raw file exists
        if not os.path.exists(raw_file):
            raise FileNotFoundError(f"Raw file not found: {raw_file}")
        
        # Read the CSV file
        df = pd.read_csv(raw_file)
        
        # Process data: Remove empty columns
        df.dropna(axis=1, how="all", inplace=True)
        
        # Save processed data
        df.to_csv(processed_file, index=False)
        logger.info(f"✅ Processed data saved: {processed_file}")
        
        # Update processing timestamp
        kwargs['ti'].xcom_push(key=f'{dataset_type}_processed_timestamp', 
                              value=PIPELINE_TIMESTAMP)
        return processed_file
        
    except Exception as e:
        logger.error(f"❌ Error processing {dataset_type}: {e}")
        raise

# Create a summary function for final reporting
def generate_pipeline_summary(**kwargs):
    """Generate a summary of the data pipeline execution."""
    ti = kwargs['ti']
    
    logger.info("==== COVID-19 Data Pipeline Summary ====")
    logger.info(f"Pipeline executed by: {OWNER}")
    logger.info(f"Execution timestamp: {PIPELINE_TIMESTAMP}")
    
    # Report on each dataset
    for dataset_type in urls.keys():
        processed_file = ti.xcom_pull(task_ids=f'process_data.process_{dataset_type}_data')
        if processed_file and os.path.exists(processed_file):
            file_size = os.path.getsize(processed_file) / 1024  # Size in KB
            logger.info(f"Dataset: {dataset_type} - Successfully processed ({file_size:.2f} KB)")
        else:
            logger.warning(f"Dataset: {dataset_type} - Processing may have failed")
    
    logger.info("====================================")
    return True

# Start of pipeline marker
start = DummyOperator(
    task_id='start_pipeline',
    dag=dag
)

# End of pipeline marker
end = DummyOperator(
    task_id='end_pipeline',
    dag=dag
)

# DATA INGESTION TASK GROUP
with TaskGroup(group_id='ingest_data', dag=dag) as ingest_group:
    # Create ingestion tasks for each dataset
    ingestion_tasks = []
    for data_type, url in urls.items():
        task = PythonOperator(
            task_id=f'download_{data_type}_data',
            python_callable=download_dataset,
            op_kwargs={'dataset_type': data_type, 'url': url},
            dag=dag,
        )
        ingestion_tasks.append(task)

# DATA PROCESSING TASK GROUP
with TaskGroup(group_id='process_data', dag=dag) as process_group:
    # Create processing tasks for each dataset
    processing_tasks = []
    for data_type in urls.keys():
        task = PythonOperator(
            task_id=f'process_{data_type}_data',
            python_callable=process_dataset,
            op_kwargs={'dataset_type': data_type},
            dag=dag,
        )
        processing_tasks.append(task)

# Add summary task
summary_task = PythonOperator(
    task_id='generate_summary',
    python_callable=generate_pipeline_summary,
    dag=dag
)

# Set up the task dependencies
start >> ingest_group >> process_group >> summary_task >> end

# Documentation
dag.doc_md = """
# COVID-19 Data Pipeline

This DAG performs a complete ETL process for COVID-19 data from Johns Hopkins University CSSE:

1. **Data Ingestion**: Downloads the latest COVID-19 datasets (confirmed cases, deaths, recovered)
2. **Data Processing**: Cleans and processes the raw data
3. **Summary Generation**: Creates a processing summary and logs the results

## Data Sources
- Confirmed cases: JHU CSSE GitHub repository
- Deaths: JHU CSSE GitHub repository
- Recovered cases: JHU CSSE GitHub repository

## Output
Processed files are saved to: `$AIRFLOW_HOME/data/processed/`

Created by: {owner}
Last updated: {timestamp}
""".format(owner=OWNER, timestamp=PIPELINE_TIMESTAMP)

if __name__ == "__main__":
    dag.cli()