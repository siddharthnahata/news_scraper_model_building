from flask import Flask, jsonify
from scripts.db.mysql import get_connection as get_conn
import psycopg2.extras

app = Flask(__name__)



@app.route("/last-300")
def last_300():
    conn = get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT title, content, source, published_at
            FROM articles
            ORDER BY id DESC
            LIMIT 300
        """)
        rows = cur.fetchall()

    conn.close()

    return jsonify({
        "count": len(rows),
        "data": rows
    })
