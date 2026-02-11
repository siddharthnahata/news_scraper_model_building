import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def fetch_money_control():
    urls = [
        "https://www.moneycontrol.com/news/business/",
        "https://www.moneycontrol.com/news/business/stocks/",
        "https://www.moneycontrol.com/news/business/markets/",
        "https://www.moneycontrol.com/news/business/ipo/"
    ]

    articles = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            ul = soup.find("ul", id="cagetory")
            if not ul:
                continue

            # only real news items
            lis = ul.find_all("li", class_="clearfix")

            for li in lis:
                a_tag = li.find("a", href=True)
                h2 = li.find("h2")

                if not a_tag or not h2:
                    continue

                title = h2.get_text(strip=True)
                link = a_tag["href"]

                # avoid duplicates
                if not any(article["url"] == link for article in articles):
                    articles.append({
                        "title": title,
                        "url": link
                    })

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue

    return articles

def fetch_money_control_time_content(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    published_at, content = None, None

    schedule_div = soup.find("div", class_="article_schedule")
    if schedule_div:
        raw_text = schedule_div.get_text(" ", strip=True)
    
        date_match = re.search(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
            raw_text
        )

        time_match = re.search(r"\d{1,2}:\d{2}", raw_text)

        if date_match and time_match:
            dt_string = f"{date_match.group()} {time_match.group()}"
            published_at = datetime.strptime(dt_string, "%B %d, %Y %H:%M")

    paragraphs = []
    content_div = soup.find("div", id="contentdata")
    if content_div:
        for p in content_div.find_all("p"):
            txt = p.get_text(strip=True)
            if txt:
                paragraphs.append(txt)

        content = "\n".join(paragraphs)

        
    return published_at, content


def money_control_wrapper(seen_url: set):
    articles = fetch_money_control()
    final_data = []

    for article in articles:
        url = article["url"]
        
        if url in seen_url:
            continue

        pub_time, pub_content = fetch_money_control_time_content(url)
        if pub_content is None or pub_time is None:
            continue

        final_data.append({
            "title": article["title"],
            "content": pub_content,
            "pub_time": pub_time,
            "url": url
        })
    return final_data
