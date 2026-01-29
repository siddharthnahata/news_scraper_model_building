from flask import Flask, jsonify
from scripts.db.mysql import get_connection as get_conn

app = Flask(__name__)



@app.route("/last-300")
def last_300():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM articles
            ORDER BY id DESC
            LIMIT 300
        """)
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
