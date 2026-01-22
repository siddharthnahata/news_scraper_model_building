import re
from utils.nse_master import load_nse_master, normalize

_nse = load_nse_master()

def extract_tickers(title: str, content: str):
    raw_text = f"{title} {content}".upper()
    norm_text = normalize(raw_text)

    matched = set()

    # phrase match (TATA CONSULTANCY SERVICES)
    for _, row in _nse.iterrows():
        phrase = row["NORM_NAME"]
        if re.search(rf"\b{re.escape(phrase)}\b", norm_text):
            matched.add(row["SYMBOL"])

    return list(matched) if matched else None
