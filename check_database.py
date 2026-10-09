import sqlite3

db_path = "data/mutual_fund.db"

with sqlite3.connect(db_path) as conn:
    funds = conn.execute(
        "SELECT * FROM dim_fund"
    ).fetchall()

    print("FUNDS IN DATABASE:")
    for fund in funds:
        print(fund)

    print("\nFIRST 10 NAV RECORDS:")
    records = conn.execute("""
        SELECT scheme_code, date, nav
        FROM fact_nav
        ORDER BY date ASC
        LIMIT 10
    """).fetchall()

    for record in records:
        print(record)

    total = conn.execute(
        "SELECT COUNT(*) FROM fact_nav"
    ).fetchone()[0]

    print("\nTotal NAV records:", total)