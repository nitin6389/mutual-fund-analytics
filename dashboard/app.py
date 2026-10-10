import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "mutual_fund.db"

st.set_page_config(
    page_title="Mutual Fund Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Mutual Fund Analytics Dashboard")
st.caption("BlueStock FinTech Internship Project")

# Load NAV data
@st.cache_data
def load_data():
   with sqlite3.connect(DB_PATH) as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table'",
            conn
        )

        if "fact_nav" not in tables["name"].values:
            raise ValueError(
                "Database mein fact_nav table nahi mili. "
                "Database file ya table setup check karein."
            )

        df = pd.read_sql_query(
            """
            SELECT date, nav
            FROM fact_nav
            WHERE scheme_code = '125497'
            ORDER BY date
            """,
            conn
        )

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        df = df.dropna(subset=["date", "nav"])
        return df

try:
    df = load_data()

    if df.empty:
        st.error("NAV data nahi mila. Database aur scheme code check karein.")
        st.stop()

    df["daily_return"] = df["nav"].pct_change()
    returns = df["daily_return"].dropna()

    annual_return = (
        (1 + returns.mean()) ** 252 - 1
        if not returns.empty else 0
    )
    volatility = (
        returns.std() * (252 ** 0.5)
        if len(returns) > 1 else 0
    )

    sharpe = (
        (annual_return - 0.06) / volatility
        if volatility != 0 else 0
    )

    running_peak = df["nav"].cummax()
    drawdown = df["nav"] / running_peak - 1
    max_drawdown = drawdown.min()

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latest NAV", f"₹{df['nav'].iloc[-1]:.2f}")
    col2.metric("Annualized Return*", f"{annual_return:.2%}")
    col3.metric("Annualized Volatility", f"{volatility:.2%}")
    col4.metric("Maximum Drawdown", f"{max_drawdown:.2%}")

    st.subheader("NAV History")
    st.line_chart(df.set_index("date")["nav"])

    st.subheader("Daily Returns")
    st.line_chart(df.set_index("date")["daily_return"])

    st.subheader("Fund Data")
    st.write(f"**Fund:** SBI Small Cap Fund - Direct Plan - Growth")
    st.write(f"**Total NAV records:** {len(df):,}")
    st.write(f"**Sharpe Ratio estimate:** {sharpe:.3f}")

    st.dataframe(df.tail(10), use_container_width=True)

    st.caption(
        "*Annualized return is an estimate based on average daily returns. "
        "Historical performance does not guarantee future returns."
    )

except Exception as error:
    st.error(f"Dashboard load karte waqt error aaya: {error}")