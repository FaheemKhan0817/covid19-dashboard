# 🌍 COVID-19 Analytics Platform

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Last Updated](https://img.shields.io/badge/last%20updated-March%202025-blueviolet)

> An end-to-end data pipeline and interactive dashboard for COVID-19 global analytics, combining Airflow for automated data processing and Streamlit for visualization.

![COVID-19 Dashboard Preview](https://github.com/FaheemKhan0817/covid19-dashboard/raw/main/screenshots/dashboard_preview.png)

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Running the Pipeline](#-running-the-pipeline)
- [Using the Dashboard](#-using-the-dashboard)
- [Data Sources](#-data-sources)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

## 🔍 Overview

This project provides a comprehensive solution for COVID-19 data analysis through:

1. **Automated Data Pipeline**: Airflow DAGs that fetch, process, and clean COVID-19 data from authoritative sources
2. **Interactive Dashboard**: A Streamlit web application for visualizing trends, comparing regions, and exploring patterns

Built with data engineering best practices, the platform provides up-to-date analytics with minimal maintenance.

## ✨ Features

### Data Pipeline Features
- Automated daily data ingestion from Johns Hopkins CSSE repository
- Robust error handling and retry mechanisms
- Data validation and cleaning steps
- Processed data storage with version tracking
- Email notifications on pipeline failures (configurable)

### Dashboard Features
- Global and country-specific COVID-19 statistics
- Multiple visualization types (line, bar, pie charts)
- Time series analysis of cases, deaths, and recoveries
- Regional and provincial breakdown
- Data exploration and filtering tools
- CSV/Excel export functionality
- Mobile-responsive design

## 🏗️ Architecture
COVID-19 Analytics Platform │ ├── 🔄 Data Processing Layer (Airflow) │ ├── Data Ingestion DAG │ │ └── Downloads raw COVID-19 data from JHU CSSE GitHub │ │ │ └── Data Processing DAG │ └── Cleans, transforms and stores processed data │ └── 📊 Visualization Layer (Streamlit) ├── Dashboard Application │ ├── Global statistics │ ├── Country-specific analysis │ └── Interactive visualizations │ └── User Interface ├── Filters and controls ├── Multiple visualization tabs └── Export functionality


## 📥 Installation

### Prerequisites
- Python 3.9+
- Apache Airflow 2.0+
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/FaheemKhan0817/covid19-dashboard.git
cd covid19-dashboard

2. **Create a new environment**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

# If you're using Google Cloud SDK, install the necessary components


4. **Create required directories**
mkdir -p data/raw data/processed

5. **Project Structure**

covid19-dashboard/
├── airflow/
│   └── dags/
│       ├── covid_data_pipeline_dag.py
│       └── data_quality_checks.py
├── data/
│   ├── processed/
│   └── raw/
├── dashboard.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── README.md
└── screenshots/
    ├── dashboard_preview.png
    └── airflow_dag_view.png


6. **🔄 Running the Pipeline**

** Setting Up Airflow **

    Set AIRFLOW_HOME environment variable

bash

export AIRFLOW_HOME=$(pwd)/airflow  # On Windows: set AIRFLOW_HOME=%cd%\airflow

    Initialize the Airflow database

bash

airflow db init

    Create an admin user

bash

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

    Copy DAG files to Airflow DAGs directory

bash

cp covid_data_pipeline_dag.py $AIRFLOW_HOME/dags/

Starting Airflow Services

    Start the Airflow scheduler

bash

airflow scheduler

    In another terminal, start the Airflow webserver

bash

export AIRFLOW_HOME=$(pwd)/airflow  # Set environment again in new terminal
airflow webserver --port 8080

    Access the Airflow UI
        Open your browser and navigate to http://localhost:8080
        Login with the admin credentials you created

    Run the DAG
        From the Airflow UI, enable and trigger the covid19_data_pipeline DAG
        Monitor execution in the Airflow UI

Understanding the DAG

The main DAG has two primary task groups:

    Data Ingestion Group
        Downloads COVID-19 time series data from JHU CSSE GitHub repository
        Performs data validation
        Stores raw data in CSV format

    Data Processing Group
        Cleans and transforms the raw data
        Calculates additional metrics
        Exports processed data to the dashboard-accessible location

📊 Using the Dashboard
Running the Streamlit Dashboard
bash

streamlit run dashboard.py

The dashboard will be available at http://localhost:8501
Dashboard Navigation

The COVID-19 dashboard is organized into several tabs:

    Cases Over Time: Cumulative statistics with line or bar chart options
    Daily New Cases: Day-by-day analysis of new infections and trends
    Case Distribution: Pie charts showing proportions of active, recovered, and death cases
    Regional Data: Provincial/state level breakdown where available

Dashboard Features

    Country Selection: Choose any country from the dropdown menu
    Date Range Selection: Filter data by custom date ranges
    Visualization Options: Toggle between chart types and use logarithmic scaling
    Data Export: Download data as CSV for offline analysis
    Summary Statistics: View key metrics and indicators at a glance

📊 Data Sources

This project uses data from the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) COVID-19 dataset, which compiles data from:

    World Health Organization (WHO)
    US Centers for Disease Control and Prevention (CDC)
    European Centre for Disease Prevention and Control (ECDC)
    Various national and regional health departments

The data is updated daily and includes:

    Confirmed cases
    Deaths
    Recovered cases (where available)
    Geographic information (coordinates)

🚀 Deployment
Deploying on Streamlit Cloud

    Push your code to GitHub

bash

git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push

    Deploy on Streamlit Cloud
        Go to Streamlit Cloud
        Sign in with your GitHub account
        Select your repository and branch
        Set the main file path to dashboard.py
        Click "Deploy"

Deploying Airflow on a Server

For production environments, consider using:

    Docker Compose for Airflow deployment
    Managed Airflow services like Amazon MWAA or Google Cloud Composer
    Kubernetes for container orchestration

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

    Fork the repository
    Create your feature branch (git checkout -b feature/amazing-feature)
    Commit your changes (git commit -m 'Add some amazing feature')
    Push to the branch (git push origin feature/amazing-feature)
    Open a Pull Request

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
🙏 Acknowledgements

    Johns Hopkins CSSE for maintaining the COVID-19 dataset
    Streamlit for their amazing framework
    Apache Airflow for the workflow management platform
    Plotly for interactive visualizations

<p align="center"> <i>Developed with ❤️ by <a href="https://github.com/FaheemKhan0817">FaheemKhan0817</a></i><br> <i>Last updated: 2025-03-03 09:15:47 UTC</i> </p> ```

