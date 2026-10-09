import sqlite3
from pathlib import Path

db_path = Path("data/mutual_fund.db")

with sqlite3.connect(db_path) as conn:
    columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(dim_fund)")
    }

    new_columns = {
        "fund_house": "TEXT",
        "category": "TEXT",
        "plan_type": "TEXT",
    }

    for column, data_type in new_columns.items():
        if column not in columns:
            conn.execute(
                f"ALTER TABLE dim_fund ADD COLUMN {column} {data_type}"
            )
            print("Added column:", column)

    conn.execute("""
        UPDATE dim_fund
        SET fund_house = ?,
            category = ?,
            plan_type = ?
        WHERE scheme_code = ?
    """, (
        "SBI Mutual Fund",
        "Small Cap",
        "Direct Plan - Growth",
        "125497"
    ))

    result = conn.execute("""
        SELECT scheme_code, scheme_name, fund_house, category, plan_type
        FROM dim_fund
    """).fetchall()

    print("\nUpdated fund details:")
    for row in result:
        print(row)

print("\nDatabase metadata update complete!")