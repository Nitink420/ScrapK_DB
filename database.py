import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_cursor():
    conn = get_connection()
    if conn:
        return conn.cursor()
    return None

def execute_query(query, params=None):
    cursor = get_cursor()
    if cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
    return None

def execute_query_one(query, params=None):
    cursor = get_cursor()
    if cursor:
        cursor.execute(query, params)
        return cursor.fetchone()
    return None

def execute_query_none(query, params=None):
    cursor = get_cursor()
    if cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
    return None