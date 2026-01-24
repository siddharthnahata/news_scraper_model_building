import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("NEWS_DB_HOST"),
        user=os.getenv("NEWS_DB_USER"),
        password=os.getenv("NEWS_DB_PASSWORD"),
        database=os.getenv("NEWS_DB_NAME")
    )