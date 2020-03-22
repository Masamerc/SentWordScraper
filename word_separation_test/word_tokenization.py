from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize
from collections import Counter
from string import punctuation
import pickle

with open("test.txt", "r") as f:
    paragraphs = f.read()

addtional_special_chars = ['—', '“', '”']
stop_words = pickle.load(open("stopwords.pkl", "rb"))

for symbol in addtional_special_chars:
    punctuation += symbol

wt = wordpunct_tokenize(paragraphs)
wpt = word_tokenize(paragraphs)
sent = sent_tokenize(paragraphs)


wt = [word for word in wt if word not in punctuation and word not in stop_words]

count_wt = Counter(wt)

print(count_wt)