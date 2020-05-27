
import pickle
import requests
import datetime

from bs4 import BeautifulSoup
from collections import Counter
from nltk import wordpunct_tokenize, sent_tokenize
from redis import Redis
from string import punctuation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


cache_redis = Redis(host="redis0", port=6378)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'referer': 'https://www.google.com/'
    }

stop_words = pickle.load(open("data/stopwords.pkl", "rb"))
analyzer = SentimentIntensityAnalyzer()

# add additonal frequently used symbols to punctuations
addtional_special_chars = ['—', '“', '”']

for symbol in addtional_special_chars:
    punctuation += symbol


def count_words(url: str) -> None:
    """scrape p tags from url and then count and store each word  """
    print(f"Counting words at {url}")

    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    paragraphs = " ".join([p.text.lower() for p in soup.find_all('p')])

    word_tokenized = wordpunct_tokenize(paragraphs)

    word_tokenized_cleaned = [word for word in word_tokenized
                              if (word.lower() not in punctuation) and (word.lower() not in stop_words) and (len(word) > 1)]

    word_count = Counter(word_tokenized_cleaned)

    word_count_list = [(datetime.datetime.now(), word, count, url)
                       for word, count in word_count.items()]
    cache_redis.setex("ws" + url, 60, pickle.dumps(word_count_list))

    print(f'Total Words: {len(word_count)}')


def score_sentiment(sentence: str, url: str) -> None:
    """Helper function that analyze sentiment and return a tuple of analyzed data"""
    score = analyzer.polarity_scores(sentence)
    return (sentence, score["pos"], score["neu"], score["neg"],
            score['compound'], url, datetime.datetime.now())


def handle_sentiment(url: str) -> None:
    """
    Scrapes sentences from the url and stores them in a list\n
    Sends the list to redis with TTL of 60 seconds
    """
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    paragraphs = " ".join([p.text for p in soup.find_all('p')])

    sentiment_data_list = [score_sentiment(sent, url)
                           for sent in sent_tokenize(paragraphs)]

    cache_redis.setex("ss" + url, 60, pickle.dumps(sentiment_data_list))
