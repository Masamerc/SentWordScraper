from nltk import sent_tokenize
from bs4 import BeautifulSoup
import requests
import sqlite3
import pprint
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import datetime

# https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'referer':'https://www.google.com/'}

conn = sqlite3.connect("sent.db")
cur = conn.cursor()
analyzer = SentimentIntensityAnalyzer()

cur.execute('''
CREATE TABLE IF NOT EXISTS sents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sentence TEXT NOT NULL,
    positive REAL,
    neutral REAL,
    negative REAL,
    source TEXT,
    scraped_at timestamp
)
''')


def store_data(sentence, score, url):
    params = (None, sentence, score["pos"], score["neu"], score["neg"], url, datetime.datetime.now())
    cur.execute("""INSERT INTO sents VALUES(?, ?, ?, ?, ?, ?, ?)""", params)


def sentiment_analyzer_scores(sentence, url):
    score = analyzer.polarity_scores(sentence)
    print(f"Sentence '{sentence[:10]}' stored in database")
    print(f'Score:{str(score)}')
    params = (None, sentence, score["pos"], score["neu"], score["neg"], url, datetime.datetime.now())
    cur.execute("""INSERT INTO sents VALUES(?, ?, ?, ?, ?, ?, ?)""", params)


##### utility #####

def make_paragraphs(url):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    paragraphs = " ".join([p.text for p in soup.find_all('p')])
    with open("test.txt", 'w') as f:
        f.write(paragraphs)
    
def load_file():
    with open("test.txt", 'r') as f:
        paragraphs = f.read()
    return sent_tokenize(paragraphs)


# make_paragraphs('https://www.gamespot.com/reviews/final-fantasy-7-remake-review-first-class/1900-6417445/')

url = 'https://www.gamespot.com/reviews/final-fantasy-7-remake-review-first-class/1900-6417445/'
sentences = load_file()

for sent in sentences:
    sentiment_analyzer_scores(sent, url)

conn.commit()
conn.close()