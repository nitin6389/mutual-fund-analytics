import sqlite3
from pathlib import Path

DB_PATH = Path("data/mutual_fund.db")
SCHEMA_PATH = Path("sql/schema.sql")

if not SCHEMA_PATH.exists():
    print("Error: schema.sql file nahi mili!")
else:
    conn = sqlite3.connect(DB_PATH)

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema)
        conn.commit()
        print("Database schema successfully created!")

        tables = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """).fetchall()

        print("\nTables found:")
        for table in tables:
            print("-", table[0])

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        conn.close()