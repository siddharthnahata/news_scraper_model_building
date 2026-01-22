import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_business_standard():
    url = "https://www.business-standard.com/markets"
    articles = []

    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    # 🔑 Anchor on stable class
    articles_divs = soup.find_all("div", class_="cardlist")

    for div in articles_divs:
        a = div.find("a", href=True)
        if not a:
            continue

        link = a["href"]

        # handle relative URLs
        if link.startswith("/"):
            link = "https://www.business-standard.com" + link

        articles.append({
            "title": a.get_text(strip=True),
            "url": link
        })

    return articles

def fetch_business_standard_time_content(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    published_at, content = None, None

    meta_div = soup.find("div", class_="meta-info")
    if meta_div:
        raw_text = meta_div.get_text(" ", strip=True)

        date_match = re.search(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}",
            raw_text
        )
        time_match = re.search(r"\d{1,2}:\d{2}\s+(AM|PM)", raw_text)

        if date_match and time_match:
            dt_string = f"{date_match.group()} {time_match.group()}"
            published_at = datetime.strptime(
                dt_string, "%b %d %Y %I:%M %p"
            )

    paragraphs = []

    parent_div = soup.find("div", id="parent_top_div")
    if parent_div:
        for div in parent_div.find_all("div", recursive=True):
            text = div.get_text(strip=True)
            if text:
                paragraphs.append(text)

    content = "\n".join(paragraphs)

    return published_at, content


def business_standard_wrapper(seen_url: set):
    articles = fetch_business_standard()
    final_data = []

    for article in articles:
        url = article["url"]
        
        if url in seen_url:
            continue

        pub_time, pub_content = fetch_business_standard_time_content(url)
        if pub_content is None or pub_time is None:
            continue

        final_data.append({
            "title": article["title"],
            "content": pub_content,
            "pub_time": pub_time,
            "url": url
        })
    return final_data


