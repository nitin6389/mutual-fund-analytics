Mutual Fund Analytics

A Python-based data analytics project focused on collecting, processing, storing, and analyzing mutual fund Net Asset Value (NAV) data.

Project Overview

This project demonstrates a data analytics workflow for mutual fund data, including data ingestion, database storage, exploratory data analysis, and risk-return analysis.

Features

- Fetch mutual fund NAV data using an API
- Process and clean NAV records using Pandas
- Store fund data in an SQLite database
- Perform exploratory data analysis (EDA)
- Calculate risk and return metrics
- Generate charts and CSV reports

Technologies Used

- Python
- Pandas
- Requests
- SQLite
- SQL
- Matplotlib

Project Structure

Mutual-Fund-Analytics/
├── dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── reports/
├── sql/
├── check_database.py
├── data_ingestion.py
├── eda_analysis.py
├── find_fund.py
├── live_nav_fetch.py
├── load_to_sqlite.py
├── risk_metrics.py
├── update_fund_metadata.py
└── requirements.txt

Getting Started

1. Clone this repository.

2. Install the required dependencies:
   
   pip install -r requirements.txt

3. Run the data ingestion script:
   
   python data_ingestion.py

4. Follow the project scripts to load the data, perform analysis, and generate reports.

Current Dataset

The current database contains NAV history for SBI Small Cap Fund - Direct Plan - Growth. Dataset details may change as additional mutual fund schemes are added.

Author

Nitin Kumar

GitHub: "@nitin6389" (https://github.com/nitin6389)
