from app import app
from app import r
from app.tasks import count_words, handle_sentiment
from app import q 
from flask import render_template, request, redirect, url_for
from time import strftime 
from redis import Redis
import time
import pickle

cache_redis = Redis(port=6378)

@app.route('/')
def index():
    return render_template('index.html')

############ Scrapes Website & Count Words ############

@app.route('/add-task', methods=["GET", "POST"])
def add_task():
    # shows queued jobs
    jobs = q.jobs
    message = None

    if request.args:
        # in html the name attr is "url"
        if request.args.get('url'):
            url = request.args.get('url')
            task = q.enqueue(count_words, url)
            jobs = q.jobs
            q_length = len(q)
            message = f"Task queued at {task.enqueued_at.strftime('%a %d %b %Y %H:%M')}. {q_length} Jobs Queued"

            # redirects to "/result" route and pass on "url"
            time.sleep(1)
            return redirect(url_for(".show_result", url=url))

    return render_template('add_task.html', message=message, jobs=jobs)


@app.route('/result', methods=["GET", "POST"])
def show_result():
    time.sleep(3)

    url = request.args["url"]

    # (datetime.datetime(2020, 5, 13, 22, 57, 26, 151155), 'mouth', 1, 'https://www.ign.com/articles/the-invisible-man-review')
    scraper_result_data = pickle.loads(cache_redis.get("word_count"))

    top_50_words = []
    for data in scraper_result_data:
        ts, word, count, source = data
        top_50_words.append((word, count))
        time_stamp = ts
    top_50_words.sort(key=lambda x: x[1], reverse=True)

    return render_template('result.html', url=url, top_50_words=top_50_words, len_top_50_words=len(top_50_words), time_stamp=time_stamp)



############ Sentiment Analysis ############


@app.route('/add-sent-task', methods=["GET", "POST"])
def add_sent_task():
    # shows queued jobs
    jobs = q.jobs
    message = None

    if request.args:
        # in html the name attr is "url"
        if request.args.get('url'):
            url = request.args.get('url')
            task = q.enqueue(handle_sentiment, url)
            jobs = q.jobs
            q_length = len(q)
            message = f"Task queued at {task.enqueued_at.strftime('%a %d %b %Y %H:%M')}. {q_length} Jobs Queued"

            # redirects to "/result" route and pass on "url" 
            time.sleep(2)
            return redirect(url_for(".show_sent_result", url=url))

    return render_template('add_sent_task.html', message=message, jobs=jobs)



############ Route for Testing ############

@app.route('/sent-result', methods=["GET", "POST"])
def show_sent_result():
    # url = request.args['url']
    url = 'https://www.politico.com/news/2020/03/20/trump-hypes-unproven-coronavirus-drugs-139525'

    time.sleep(2) # change to 3 

    sentiment_list_data = pickle.loads(cache_redis.get("sentiment_count"))
    print(sentiment_list_data)

    top_100_sents = []

    for data in sentiment_list_data:
        sent, pos, neu, neg, compound, source, ts = data
        top_100_sents.append((sent, compound))
        time_stamp = ts

    top_100_sents.sort(key=lambda x: x[1], reverse=True)
    top_100_sents = [sent_tuple for sent_tuple in top_100_sents if sent_tuple[1] != 0]

    total_compound = sum((row[1] for row in top_100_sents))
    total_records = len(top_100_sents)
    average_compound = round(total_compound / total_records, 4)
    total_pos = [row[1] for row in top_100_sents if row[1] >= 0]
    total_neg = [row[1] for row in top_100_sents if row[1] < 0]

    top_10_sents = top_100_sents[:10]
    worst_10_sents = top_100_sents[-10:][::-1]

    return render_template('sent_result.html', url=url, top_100_sents=top_100_sents,\
                        time_stamp=time_stamp, average_compound=average_compound,\
                        top_10_sents=top_10_sents, worst_10_sents=worst_10_sents, total_records=total_records,\
                        pos_length=len(total_pos), neg_length=len(total_neg))