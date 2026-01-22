import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "news_user"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "news_engine"),
    )
