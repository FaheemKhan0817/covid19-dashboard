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

COVID-19 Analytics Platform
├── 🔄 Data Processing Layer (Airflow)
│   ├── Data Ingestion DAG
│   │   └── Fetches raw data from JHU CSSE GitHub
│   └── Data Processing DAG
│       └── Cleans, transforms, and stores processed data
└── 📊 Visualization Layer (Streamlit)
├── Dashboard Application
│   ├── Global statistics
│   ├── Country-specific analysis
│   └── Interactive visualizations
└── User Interface
├── Filters and controls
├── Multi-tab visualizations
└── Export functionality
text

---

## 📥 Installation

### Prerequisites
- 🐍 Python 3.9+
- 🌬️ Apache Airflow 2.0+
- 📦 Git

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/FaheemKhan0817/covid19-dashboard.git
   cd covid19-dashboard

    Create a Virtual Environment
    bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies
bash
pip install -r requirements.txt
Create Required Directories
bash
mkdir -p data/raw data/processed
Project Structure
text

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

🔄 Running the Pipeline
Setting Up Airflow

    Set AIRFLOW_HOME Environment Variable
    bash

export AIRFLOW_HOME=$(pwd)/airflow  # On Windows: set AIRFLOW_HOME=%cd%\airflow
Initialize Airflow Database
bash
airflow db init
Create an Admin User
bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
Copy DAG Files
bash

    cp covid_data_pipeline_dag.py $AIRFLOW_HOME/dags/

Starting Airflow Services

    Start the Scheduler
    bash

airflow scheduler
Start the Webserver (in a new terminal)
bash

    export AIRFLOW_HOME=$(pwd)/airflow
    airflow webserver --port 8080
    Access the Airflow UI
        Open http://localhost:8080
        Log in with your admin credentials
    Run the DAG
        Enable and trigger the covid19_data_pipeline DAG in the UI
        Monitor execution progress

Understanding the DAG

    Data Ingestion Group: Downloads and validates raw data, stores it as CSV.
    Data Processing Group: Cleans, transforms, and prepares data for the dashboard.

📊 Using the Dashboard
Running the Streamlit Dashboard
bash
streamlit run dashboard.py

    Access at: http://localhost:8501

Dashboard Navigation

    Cases Over Time: Line/bar charts of cumulative stats
    Daily New Cases: Trends in new infections
    Case Distribution: Pie charts for case proportions
    Regional Data: Detailed provincial/state breakdowns

Dashboard Features

    🌍 Country selection dropdown
    📅 Custom date range filtering
    🎨 Toggleable chart types and logarithmic scaling
    📤 Data export to CSV
    📋 Summary stats at a glance

📈 Data Sources

Sourced from the Johns Hopkins University CSSE COVID-19 Dataset, aggregating data from:

    🌐 World Health Organization (WHO)
    🇺🇸 US CDC
    🇪🇺 European CDC
    Various national health departments

Includes: Confirmed cases, deaths, recoveries, and geographic data, updated daily.
🚀 Deployment
Deploying on Streamlit Cloud

    Push to GitHub
    bash

    git add .
    git commit -m "Prepare for Streamlit Cloud deployment"
    git push
    Deploy via Streamlit Cloud
        Log in with GitHub
        Select repository and branch
        Set dashboard.py as the main file
        Click "Deploy"

Deploying Airflow on a Server

    Use Docker Compose, Amazon MWAA, Google Cloud Composer, or Kubernetes.

🤝 Contributing

We welcome contributions! Follow these steps:

    Fork the repo
    Create a feature branch (git checkout -b feature/amazing-feature)
    Commit changes (git commit -m 'Add some amazing feature')
    Push to the branch (git push origin feature/amazing-feature)
    Open a Pull Request

📄 License

Licensed under the MIT License. See the LICENSE file for details.
🙏 Acknowledgements

    Johns Hopkins CSSE: For the COVID-19 dataset
    Streamlit: For an amazing visualization framework
    Apache Airflow: For workflow orchestration
    Plotly: For interactive charts

<p align="center"> <i>Developed with ❤️ by <a href="https://github.com/FaheemKhan0817">FaheemKhan0817</a></i><br> <i>Last updated: 2025-03-03 09:15:47 UTC</i> </p> ```