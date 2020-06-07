import pickle
import time
import os

from app import app
from app import q
from app.tasks import count_words, handle_sentiment
from flask import render_template, request, redirect, url_for, after_this_request
from redis import Redis
from time import strftime


cache_redis = Redis(port=6379)


@app.route('/')
def index():
    """Route to landing page"""
    return render_template('index.html')


@app.route('/add-task', methods=["GET", "POST"])
def add_task():
    """
    Route to a page where usrs send word-scraping requests.\n
    RQ queues up a task defined in tasks.py
    """
    jobs = q.jobs
    message = None

    if request.args:
        if request.args.get('url'):
            url = request.args.get('url')
            task = q.enqueue(count_words, url)
            jobs = q.jobs
            q_length = len(q)
            message = f"Task queued at {task.enqueued_at.strftime('%a %d %b %Y %H:%M')}. {q_length} Jobs Queued"

            # redirects to "/result" route and pass on "url"
            return redirect(url_for(".show_result", url=url))

    return render_template('add_task.html', message=message, jobs=jobs)


@app.route('/result', methods=["GET", "POST"])
def show_result():
    """
    Route loaded after word-scraper task\n
    Sends data from word-scraper to result.html
    """
    url = request.args["url"]

    # retrieve scraped words from redis
    while cache_redis.get("ws" + url) is None:
        time.sleep(0.5)
        if cache_redis.get("ws" + url):
            break

    scraper_result_data = pickle.loads(cache_redis.get("ws" + url))

    scraped_words = []
    for data in scraper_result_data:
        ts, word, count, source = data
        scraped_words.append((word, count))
        time_stamp = ts
    scraped_words.sort(key=lambda x: x[1], reverse=True)

    # retrieve wordcloud file_id from redis 
    while cache_redis.get("ws" + url + "filename") is None:
        time.sleep(0.5)
        if cache_redis.get("ws" + url + "filename"):
            break
    wordcloud_image_name = cache_redis.get("ws" + url + "filename")
    wordcloud_image_name = wordcloud_image_name.decode("utf-8")


    return render_template('result.html', url=url, scraped_words=scraped_words, time_stamp=time_stamp, image_name=wordcloud_image_name)


@app.route('/add-sent-task', methods=["GET", "POST"])
def add_sent_task():
    """
    Route to a page where usrs send sentiment-scraping requests.\n
    RQ queues up a task defined in tasks.py
    """
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
            return redirect(url_for(".show_sent_result", url=url))

    return render_template('add_sent_task.html', message=message, jobs=jobs)


@app.route('/sent-result', methods=["GET", "POST"])
def show_sent_result():
    """
    Route to page loaded right after sent-scraper runs\n
    Loads data from sentiment-scraper and sends it to sent_result.html
    """
    url = request.args['url']

    while cache_redis.get("ss" + url) is None:
        time.sleep(0.5)
        if cache_redis.get("ss" + url):
            break

    sentiment_list_data = pickle.loads(cache_redis.get("ss" + url))

    scraped_sents = []

    for data in sentiment_list_data:
        sent, pos, neu, neg, compound, source, ts = data
        scraped_sents.append((sent, compound))
        time_stamp = ts

    scraped_sents.sort(key=lambda x: x[1], reverse=True)
    scraped_sents = [sent_tuple for sent_tuple in scraped_sents if sent_tuple[1] != 0]

    total_compound = sum((row[1] for row in scraped_sents))
    total_records = len(scraped_sents)
    average_compound = round(total_compound / total_records, 4)
    total_pos = [row[1] for row in scraped_sents if row[1] >= 0]
    total_neg = [row[1] for row in scraped_sents if row[1] < 0]

    top_10_sents = scraped_sents[:10]
    worst_10_sents = scraped_sents[-10:][::-1]

    return render_template('sent_result.html', url=url, scraped_sents=scraped_sents,
                           time_stamp=time_stamp, average_compound=average_compound,
                           top_10_sents=top_10_sents, worst_10_sents=worst_10_sents, total_records=total_records,
                           pos_length=len(total_pos), neg_length=len(total_neg))
