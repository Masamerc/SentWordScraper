from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
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


        
        
### SCRAPE WEB AND COUNT WORDS ###
def count_words(url):

    time.sleep(1)
    print(f"Counting words at {url}")

    start = time.time()
    resp = requests.get(url)

    soup = BeautifulSoup(resp.content, 'html.parser')

    paragraphs = " ".join([p.text for p in soup.find_all('p')])
    
    # with Counter
    word_count = Counter(paragraphs.split())
    
    # with Defaultdict
    # word_count = defaultdict(int)
    # for i in paragraphs.split():
    #     word_count[i] += 1

    end = time.time()

    time_passsed = end - start

    print(word_count.most_common(10))
    print(f'Total Words: {len(word_count)} Time Elapsed: {time_passsed}')


executor.conn.close()