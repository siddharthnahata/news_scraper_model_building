import json
from scripts.db.mysql import get_connection

def insert_article(article: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO articles (
            source, title, url, content,
            published_at, tickers, tags
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE url = url
        """,
        (
            article["source"],
            article["title"],
            article["url"],
            article["content"],
            article["published_at"],
            json.dumps(article["tickers"]),
            json.dumps(article["tags"])
        )
    )

    conn.commit()
    cur.close()
    conn.close()
