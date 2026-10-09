import sqlite3
from pathlib import Path

DB_PATH = Path("data/mutual_fund.db")

if not DB_PATH.exists():
    print("Database file nahi mili:", DB_PATH)
else:
    conn = sqlite3.connect(DB_PATH)

    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    print("Database:", DB_PATH)
    print("\nTables found:")

    for table in tables:
        print("-", table[0])

    result = conn.execute(
        "SELECT COUNT(*) FROM fact_nav"
    ).fetchone()

    print("\nTotal NAV records:", result[0])

    conn.close()