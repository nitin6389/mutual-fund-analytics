import requests

url = "https://api.mfapi.in/mf"
offset = 0
limit = 1000
matches = []

try:
    while True:
        response = requests.get(
            url,
            params={"limit": limit, "offset": offset},
            timeout=30
        )
        response.raise_for_status()
        funds = response.json()

        if not isinstance(funds, list) or not funds:
            break

        for fund in funds:
            name = fund.get("schemeName", "")
            if "HDFC" in name.upper() and "TOP 100" in name.upper():
                matches.append(fund)

        offset += len(funds)
        print("Schemes checked:", offset)

        if len(funds) < limit:
            break

    print("\nMatching funds:")
    for fund in matches:
        print(fund.get("schemeCode"), "-", fund.get("schemeName"))

    if not matches:
        print("HDFC Top 100 nahi mila. Search result verify karna hoga.")

except Exception as error:
    print("Error:", error)