-- Mutual Fund Analytics Platform
-- Database schema

CREATE TABLE IF NOT EXISTS dim_fund (
    scheme_code TEXT PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT,
    category TEXT,
    plan_type TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code TEXT NOT NULL,
    date TEXT NOT NULL,
    nav REAL NOT NULL,
    FOREIGN KEY (scheme_code)
        REFERENCES dim_fund(scheme_code),
    UNIQUE (scheme_code, date)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code TEXT NOT NULL,
    date TEXT NOT NULL,
    aum REAL,
    FOREIGN KEY (scheme_code)
        REFERENCES dim_fund(scheme_code)
);

CREATE TABLE IF NOT EXISTS fact_sip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code TEXT,
    month TEXT NOT NULL,
    sip_inflow REAL,
    sip_count INTEGER
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code TEXT,
    transaction_date TEXT,
    transaction_type TEXT,
    amount REAL,
    units REAL
);