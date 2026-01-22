import pandas as pd
import requests
import io
import re

STOPWORDS = {
    "LIMITED", "LTD", "PRIVATE", "PVT",
    "CORPORATION", "CORP", "CO", "COMPANY"
}

def normalize(text: str) -> str:
    text = text.upper()
    text = re.sub(r"[^A-Z\s]", " ", text)
    words = [w for w in text.split() if w not in STOPWORDS]
    return " ".join(words)

def load_nse_master():
    url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/csv"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    df = pd.read_csv(io.StringIO(r.text))
    df["SYMBOL"] = df["SYMBOL"].str.upper()
    df["NORM_NAME"] = df["NAME OF COMPANY"].apply(normalize)

    # critical false-positive control
    df = df[df["NORM_NAME"].str.len() >= 10]

    return df
