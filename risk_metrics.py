import sqlite3
import pandas as pd
import numpy as np
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
df = df.dropna(subset=["date", "nav"]).sort_values("date")

# Daily percentage returns
df["daily_return"] = df["nav"].pct_change()
returns = df["daily_return"].dropna()

# Approximate annualized metrics using 252 trading days
annual_return = (1 + returns.mean()) ** 252 - 1
annual_volatility = returns.std() * np.sqrt(252)

# Sharpe ratio using 6% assumed annual risk-free rate
risk_free_rate = 0.06
sharpe = (
    (annual_return - risk_free_rate) / annual_volatility
    if annual_volatility != 0 else np.nan
)

# Maximum drawdown
df["running_peak"] = df["nav"].cummax()
df["drawdown"] = df["nav"] / df["running_peak"] - 1
max_drawdown = df["drawdown"].min()

print("Fund: SBI Small Cap Fund")
print(f"Annualized return estimate: {annual_return:.2%}")
print(f"Annualized volatility: {annual_volatility:.2%}")
print(f"Sharpe ratio estimate: {sharpe:.3f}")
print(f"Maximum drawdown: {max_drawdown:.2%}")

df.to_csv("reports/sbi_small_cap_returns.csv", index=False)

print("\nReturns data saved to reports/sbi_small_cap_returns.csv")