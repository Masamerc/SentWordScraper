from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import requests
import time
import sqlite3
import datetime


HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'referer':'https://www.google.com/'}

conn = sqlite3.connect("word.db")
cur = conn.cursor()

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

cur.execute('''
CREATE TABLE IF NOT EXISTS words(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scraped_at timestamp,
    word TEXT NOT NULL,
    count INTEGER NOT NULL,
    source TEXT
)
''')


executor = ValueInserter(conn)

        
### SCRAPE WEB AND COUNT WORDS ###
def count_words(url):


    time.sleep(1)
    print(f"Counting words at {url}")

    start = time.time()
    resp = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(resp.content, 'html.parser')

    paragraphs = " ".join([p.text.lower() for p in soup.find_all('p')])

    # with Counter
    word_count = Counter(paragraphs.split())
    
    # with Defaultdict
    # word_count = defaultdict(int)
    # for i in paragraphs.split():
    #     word_count[i] += 1

    end = time.time()

    time_passsed = end - start

    print(f"Inserting Data to Database...")

    for word, count in word_count.items():
        word = word.strip().replace('.', '').replace('"', '').replace("'", "").replace(',', '')
        executor.insert((datetime.datetime.now(), word, count, url), "words")


    print(f'Total Words: {len(word_count)} Time Elapsed: {time_passsed}')

    executor.conn.close()

