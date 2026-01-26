import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_economic_times():
    url = "https://economictimes.indiatimes.com/markets/stocks/news"
    articles = []

    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    # 🔑 Anchor on stable class
    articles_divs = soup.find_all("div", class_="eachStory")

    for div in articles_divs:
        a = div.find("a", href=True)
        if not a:
            continue

        link = a["href"]

        # handle relative URLs
        if link.startswith("/"):
            link = "https://economictimes.indiatimes.com" + link

        articles.append({
            "title": a.get_text(strip=True),
            "url": link
        })

    return articles


def fetch_economic_times_time_content(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    published_at, content = None, None

    meta_div = soup.find("div", class_="article_block")
    if meta_div:
        raw_date = meta_div.get("data-artidate")

        if raw_date:
            try:
                clean_date = raw_date.replace(" IST", "")
                published_at = datetime.strptime(
                    clean_date, "%b %d, %Y, %I:%M:%S %p"
                )
            except Exception:
                published_at = None

    paragraphs = []
    article_div = soup.find("div", class_="artText")
    if article_div:
        # remove unwanted elements
        for tag in article_div.find_all(
            ["style", "script", "noscript", "div"],
            recursive=True
        ):
            tag.decompose()

        for elem in article_div.stripped_strings:
            if len(elem) > 30:  # filter noise
                paragraphs.append(elem)

    content = "\n".join(paragraphs) if paragraphs else None

    return published_at, content


def economic_times_wrapper(seen_url: set):
    articles = fetch_economic_times()
    final_data = []

    for article in articles:
        url = article["url"]
        
        if url in seen_url:
            continue

        pub_time, pub_content = fetch_economic_times_time_content(url)
        if pub_content is None or pub_time is None:
            continue

        final_data.append({
            "title": article["title"],
            "content": pub_content,
            "pub_time": pub_time,
            "url": url
        })
    return final_data


