import sqlite3

def create_connection():
    conn = sqlite3.connect("data.db")
    return conn