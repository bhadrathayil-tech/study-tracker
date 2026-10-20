import sqlite3
from datetime import datetime

DB_NAME = "study_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            duration INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS freezes (
            date TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def add_session(subject, duration, date_str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (subject, duration, date) VALUES (?, ?, ?)', 
                   (subject, duration, date_str))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, subject, duration, date FROM sessions ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_session(session_id, subject, duration, date_str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE sessions SET subject = ?, duration = ?, date = ? WHERE id = ?', 
                   (subject, duration, date_str, session_id))
    conn.commit()
    conn.close()

def delete_session(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()