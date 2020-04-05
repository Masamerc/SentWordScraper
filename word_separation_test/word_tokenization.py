from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize
from collections import Counter
from string import punctuation
import pickle
from pprint import pprint as pp

with open("sw_episodeVI.txt", "r") as f:
    paragraphs = f.read()

addtional_special_chars = ['—', '“', '”']
stop_words = pickle.load(open("stopwords.pkl", "rb"))

for symbol in addtional_special_chars:
    punctuation += symbol

wpt = wordpunct_tokenize(paragraphs)
wt = word_tokenize(paragraphs)
sent = sent_tokenize(paragraphs)

split_words = paragraphs.split()

words_tokenized_cleaned = [word for word in wpt if (word.lower() not in punctuation) and (word.lower() not in stop_words) and (len(word) > 1)]
# words_tokenized_cleaned = [word for word in wpt if (word.lower() not in stop_words) and (len(word) > 1)]
words_split_cleaned = [word for word in split_words if word.lower() not in punctuation and word.lower() not in stop_words]
count_wt = Counter(words_tokenized_cleaned)
count_split = Counter(words_split_cleaned)

pp(count_wt)