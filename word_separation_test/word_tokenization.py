from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize

with open("test.txt", "r") as f:
    paragraphs = f.read()

wt = wordpunct_tokenize(paragraphs)
wpt = word_tokenize(paragraphs)
sent = sent_tokenize(paragraphs)

