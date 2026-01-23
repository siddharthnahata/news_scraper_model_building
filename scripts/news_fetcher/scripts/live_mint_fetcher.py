import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_livemint():
    BASE_URL = "https://www.livemint.com/market/stock-market-news"
    articles = []
    max_pages=10

    for page in range(1, max_pages + 1):
        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}/page-{page}"

        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")

        page_articles = 0

        for h2 in soup.find_all("h2", class_="headline"):
            a = h2.find("a", href=True)
            if not a:
                continue

            link = a["href"]
            if link.startswith("/"):
                link = "https://www.livemint.com" + link

            articles.append({
                "title": a.get_text(strip=True),
                "url": link
            })

            page_articles += 1

        # 🔑 stop if page is empty
        if page_articles == 0:
            break

    return articles

def fetch_livemint_time_content(url: str):
    """
    Fetch published time + article content from Livemint article page
    """
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # ---- TIME ----
    pub_time = None
    time_span = soup.find("span", string=re.compile("IST"))
    if time_span:
        try:
            pub_time = datetime.strptime(
                time_span.get_text(strip=True),
                "%d %b %Y, %I:%M %p IST"
            )
        except Exception:
            pub_time = None

    # ---- CONTENT ----
    paragraphs = soup.select("div.storyParagraph p")
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    if not content:
        return None

    return {
        "content": content,
        "pub_time": pub_time
    }

def live_mint_wrapper(seen_url: set):
    articles = fetch_livemint()
    final_data = []

    for article in articles:
        url = article["url"]
        
        if url in seen_url:
            continue

        pub_time, pub_content = fetch_livemint_time_content(url)
        if pub_content is None or pub_time is None:
            continue

        final_data.append({
            "title": article["title"],
            "content": pub_content,
            "pub_time": pub_time,
            "url": url
        })
    return final_data