import requests
import pandas as pd
from pathlib import Path

# Project data folder
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Currently tested scheme code
SCHEME_CODES = ["125497"]

def fetch_fund_data(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        scheme_name = data.get("meta", {}).get(
            "scheme_name", "Unknown Fund"
        )

        records = data.get("data", [])
        if not records:
            print("No NAV records found:", scheme_name)
            return

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(
            df["date"], format="%d-%m-%Y", errors="coerce"
        )
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        df = df.dropna(subset=["date", "nav"])
        df = df.sort_values("date")

        # Save using the actual scheme code
        json_file = RAW_DIR / f"scheme_{scheme_code}_raw.json"
        csv_file = RAW_DIR / f"scheme_{scheme_code}_nav.csv"

        json_file.write_text(response.text, encoding="utf-8")
        df.to_csv(csv_file, index=False)

        print("\nFund:", scheme_name)
        print("Scheme code:", scheme_code)
        print("NAV records:", len(df))
        print("CSV saved:", csv_file)

    except (requests.RequestException, ValueError, TypeError) as error:
        print(f"Error fetching scheme {scheme_code}: {error}")


if __name__ == "__main__":
    for code in SCHEME_CODES:
        fetch_fund_data(code)