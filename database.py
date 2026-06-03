import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", os.getenv("DB_HOST")),
        port=int(os.getenv("MYSQLPORT", 3306)),
        user=os.getenv("MYSQLUSER", os.getenv("DB_USER")),
        password=os.getenv("MYSQLPASSWORD", os.getenv("DB_PASSWORD")),
        database=os.getenv("MYSQLDATABASE", os.getenv("DB_NAME"))
    )