import time
import sqlite3
import datetime


conn = sqlite3.connect("word.db")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS words(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scraped_at timestamp,
    word TEXT NOT NULL,
    count INTEGER NOT NULL,
    source TEXT
)
''')

class ValueInserter:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
        
    def insert(self, tuple, table_name):
        length = len(tuple)
        placeholders = "(" + "null," + "?, " * (length -1) + "?)"

        self.cur.execute(f'''
        INSERT INTO {table_name}
        VALUES{placeholders}
        ''', tuple)

        self.conn.commit()


executor = ValueInserter(conn)


executor.conn.close()