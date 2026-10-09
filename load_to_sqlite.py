import sqlite3
import pandas as pd
from pathlib import Path

# Project paths
CSV_FILE = Path("data/raw/scheme_125497_nav.csv")
DB_FILE = Path("data/mutual_fund.db")

# Create database folder if needed
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

if not CSV_FILE.exists():
    print("CSV file nahi mili:", CSV_FILE)
else:
    df = pd.read_csv(CSV_FILE, parse_dates=["date"])

    with sqlite3.connect(DB_FILE) as conn:
        # Fund master table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_fund (
                scheme_code TEXT PRIMARY KEY,
                scheme_name TEXT NOT NULL
            )
        """)

        # NAV history table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_nav (
                scheme_code TEXT NOT NULL,
                date TEXT NOT NULL,
                nav REAL NOT NULL,
                PRIMARY KEY (scheme_code, date),
                FOREIGN KEY (scheme_code)
                    REFERENCES dim_fund(scheme_code)
            )
        """)

        conn.execute(
            """
            INSERT OR REPLACE INTO dim_fund
            (scheme_code, scheme_name)
            VALUES (?, ?)
            """,
            ("125497", "SBI SMALL CAP FUND - Direct Plan - Growth")
        )

        # Replace existing NAV rows for this scheme
        conn.execute(
            "DELETE FROM fact_nav WHERE scheme_code = ?",
            ("125497",)
        )

        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        rows = [
            ("125497", row.date, float(row.nav))
            for row in df.itertuples(index=False)
        ]

        conn.executemany(
            """
            INSERT INTO fact_nav (scheme_code, date, nav)
            VALUES (?, ?, ?)
            """,
            rows
        )

        total = conn.execute(
            "SELECT COUNT(*) FROM fact_nav WHERE scheme_code = ?",
            ("125497",)
        ).fetchone()[0]

    print("Database successfully created!")
    print("Database:", DB_FILE)
    print("NAV records loaded:", total)