from bs4 import BeautifulSoup
from collections import Counter
import requests
import time
import sqlite3
import datetime
from nltk import wordpunct_tokenize, sent_tokenize
from string import punctuation
import pickle


HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'referer':'https://www.google.com/'}


addtional_special_chars = ['—', '“', '”']
stop_words = pickle.load(open("stopwords.pkl", "rb"))

for symbol in addtional_special_chars:
    punctuation += symbol

######################-Database Initialization-######################

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

        
######################-Tasks-######################

def count_words(url):

    print(f"Counting words at {url}")

    start = time.time()
    resp = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(resp.content, 'html.parser')

    paragraphs = " ".join([p.text.lower() for p in soup.find_all('p')])

    # with tokenizer
    word_tokenized = wordpunct_tokenize(paragraphs)
    word_tokenized_cleaned = [word for word in word_tokenized if (word.lower() not in punctuation) and (word.lower() not in stop_words) and (len(word) > 1)]
    word_count = Counter(word_tokenized_cleaned)

    end = time.time()

    time_passsed = end - start

    print(f"Inserting Data to Database...")

    for word, count in word_count.items():
        executor.insert((datetime.datetime.now(), word, count, url), "words")


    print(f'Total Words: {len(word_count)} Time Elapsed: {time_passsed}')

    executor.conn.close()

