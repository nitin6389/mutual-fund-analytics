import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

with sqlite3.connect("data/mutual_fund.db") as conn:
    df = pd.read_sql_query(
        """
        SELECT date, nav
        FROM fact_nav
        WHERE scheme_code = '125497'
        ORDER BY date
        """,
        conn
    )

df["date"] = pd.to_datetime(df["date"])
df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
df = df.dropna(subset=["date", "nav"])

print("Total records:", len(df))
print("\nNAV summary:")
print(df["nav"].describe())

plt.figure(figsize=(12, 6))
plt.plot(df["date"], df["nav"])
plt.title("SBI Small Cap Fund - NAV History")
plt.xlabel("Date")
plt.ylabel("NAV (₹)")
plt.grid(True)
plt.tight_layout()
plt.savefig("reports/sbi_small_cap_nav.png")
plt.show()

print("\nChart saved: reports/sbi_small_cap_nav.png")