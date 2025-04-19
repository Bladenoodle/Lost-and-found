import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    try:
        cursor = con.execute(sql, params)
        con.commit()
        return cursor
    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
        return None
    finally:
        con.close()

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result