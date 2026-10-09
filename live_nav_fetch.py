import requests
import pandas as pd
from pathlib import Path

# Create the raw data folder
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# HDFC Top 100 Direct
SCHEME_CODE = "125497"
url = f"https://api.mfapi.in/mf/{SCHEME_CODE}"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    print("Actual scheme:", data["meta"]["scheme_name"])
    nav_df = pd.DataFrame(data["data"])
    nav_df["date"] = pd.to_datetime(
        nav_df["date"], format="%d-%m-%Y", errors="coerce"
    )
    nav_df["nav"] = pd.to_numeric(nav_df["nav"], errors="coerce")
    nav_df = nav_df.dropna(subset=["date", "nav"])
    nav_df = nav_df.sort_values("date")

    raw_file = RAW_DIR / "hdfc_top100_raw.json"
    csv_file = RAW_DIR / "hdfc_top100_nav.csv"

    raw_file.write_text(response.text, encoding="utf-8")
    nav_df.to_csv(csv_file, index=False)

    print("NAV data successfully fetched!")
    print("Scheme:", data.get("meta", {}).get("scheme_name", "Unknown"))
    print("Total records:", len(nav_df))
    print(nav_df.head())
    print("Saved to:", csv_file)

except requests.RequestException as error:
    print("API se data fetch nahi hua:", error)
except (ValueError, KeyError, TypeError) as error:
    print("Data process karte waqt error aaya:", error)