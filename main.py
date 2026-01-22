import time
import logging
from datetime import datetime

from scripts.news_fetcher.wrapper import generic_news_wrapper
from scripts.data_processor.ticker_extractor import extract_tickers
from scripts.data_processor.tag_extractor import extract_tags
from scripts.db.article_repo import insert_article

from scripts.news_fetcher.scripts.money_control_fetcher import (
    fetch_money_control,
    fetch_money_control_time_content
)
from scripts.news_fetcher.scripts.business_standard_fetcher import (
    fetch_business_standard,
    fetch_business_standard_time_content
)

# ---------------- CONFIG ----------------
SLEEP_SECONDS = 5 * 60

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ---------------- CORE INGESTION ----------------
def ingest_articles(source_name, fetch_listing, fetch_detail):
    seen_url = set()  # cycle-level dedup only

    articles = generic_news_wrapper(
        seen_url,
        fetch_listing,
        fetch_detail
    )

    for art in articles:
        try:
            art["tickers"] = extract_tickers(art["title"], art["content"])
            art["tags"] = extract_tags(art["title"], art["content"])
            art["source"] = source_name

            insert_article({
                "source": art["source"],
                "title": art["title"],
                "url": art["url"],
                "content": art["content"],
                "published_at": art["pub_time"],
                "tickers": art["tickers"],
                "tags": art["tags"]
            })

            logging.info(f"[{source_name}] Inserted: {art['title'][:80]}")

        except Exception as e:
            logging.error(f"[{source_name}] Failed for URL {art.get('url')} | {e}")

# ---------------- MAIN LOOP ----------------
def run_forever():
    logging.info("News ingestion service started")

    while True:
        start_time = datetime.now()

        try:
            # ---- MONEYCONTROL ----
            ingest_articles(
                source_name="moneycontrol",
                fetch_listing=fetch_money_control,
                fetch_detail=fetch_money_control_time_content
            )

            # ---- BUSINESS STANDARD ----
            ingest_articles(
                source_name="business_standard",
                fetch_listing=fetch_business_standard,
                fetch_detail=fetch_business_standard_time_content
            )

        except Exception as e:
            logging.critical(f"Cycle failed | {e}")

        elapsed = (datetime.now() - start_time).total_seconds()
        sleep_for = max(0, SLEEP_SECONDS - elapsed)

        logging.info(f"Cycle done. Sleeping {sleep_for:.0f} seconds...\n")
        time.sleep(sleep_for)

# ---------------- ENTRY ----------------
if __name__ == "__main__":
    run_forever()
