from app import app
from app import r
from app.tasks import count_words, print_sentiment
from app import q 
from flask import render_template, request, redirect, url_for
from time import strftime 
from util import SqliteWrapper
import time


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
    
    # url = 'https://www.npr.org/2020/03/24/820271472/tom-nook-take-me-away-animal-crossing-new-horizons-is-a-perfect-escape'
    url = request.args['url']
    # SQL query to get top 30 recorded  words  
    with SqliteWrapper('word.db') as db:

        query = db.execute(f'''select * from words where source = ?
                                order by count desc LIMIT 50;''', (url,))
        top_50_words = []

        for data in query.fetchall():
            ind, ts, word, count, source = data
            top_50_words.append((word, count))
            time_stamp = ts

    return render_template('result.html', url=url, top_50_words=top_50_words, len_top_50_words=len(top_50_words), time_stamp=time_stamp)


############ All Results ############

@app.route('/all-results', methods=['GET', 'POST'])
def show_all_results():

    if request.args:
        keyword = request.args['keyword']

        with SqliteWrapper('word.db') as db:
            # gets word & count from db
            word_query = db.execute('''select * from words where source LIKE ? 
                                    order by count desc LIMIT 100;''', ("%"+ keyword + "%",))

            all_words = []
            sources = []

            for data in word_query.fetchall():
                ind, ts, word, count, source = data
                all_words.append((word, count))

            # get matched sources from db
            source_query = db.execute('select source, max(scraped_at) from words where source LIKE ? group by source;', ("%"+ keyword + "%",))

            for data in source_query.fetchall():
                source, ts = data
                sources.append((source, ts))

        message = f"Showing results that matched the keyword: {keyword}"

        return render_template('all_results.html', all_words=all_words, message=message, sources=sources)


    with SqliteWrapper('word.db') as db:
            query = db.execute(f'''select * from words 
                                    order by count desc LIMIT 100;''')
            all_words = []
            sources = []

            for data in query.fetchall():
                ind, ts, word, count, source = data
                all_words.append((word, count))

            source_query = db.execute('select source, max(scraped_at) from words group by source;')

            for data in source_query.fetchall():
                source, ts = data
                sources.append((source, ts))

            message = "Showing All Results: No keyword supplied or keyword did not match any source"

    return render_template('all_results.html', all_words=all_words, message=message, sources=sources)


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
            task = q.enqueue(print_sentiment, url)
            jobs = q.jobs
            q_length = len(q)
            message = f"Task queued at {task.enqueued_at.strftime('%a %d %b %Y %H:%M')}. {q_length} Jobs Queued"

            # redirects to "/result" route and pass on "url" 
            time.sleep(1.5)
            return redirect(url_for(".show_sent_result", url=url))

    return render_template('add_sent_task.html', message=message, jobs=jobs)


@app.route('/sent-result', methods=["GET", "POST"])
def show_sent_result():
    url = 'https://www.politico.com/news/2020/03/20/trump-hypes-unproven-coronavirus-drugs-139525'    
    # url = request.args['url']

    # SQL query to get top 30 recorded  words
    time.sleep(1)  
    with SqliteWrapper('word.db') as db:

        query = db.execute(f'''select * from sents where source = ? AND compound != 0
                                order by compound desc LIMIT 100;''', (url,))
        top_100_sents = []

        for data in query.fetchall():
            ind, sent, pos, neu, neg, compound, source, ts = data
            top_100_sents.append((sent, compound))
            time_stamp = ts

        total_compound = sum((row[1] for row in top_100_sents))
        total_records = len(top_100_sents)
        average_compound = round(total_compound / total_records, 4)

        top_10_sents = top_100_sents[:10]
        worst_10_sents = top_100_sents[-10:][::-1]

    return render_template('sent_result.html', url=url, top_100_sents=top_100_sents,\
                           time_stamp=time_stamp, average_compound=average_compound,\
                            top_10_sents=top_10_sents, worst_10_sents=worst_10_sents)


############ Route for Testing ############

@app.route('/test')
def test():
    with SqliteWrapper('word.db') as db:
        q = db.execute("select * from words LIMIT 5;")
        result = q.fetchall()

    if result:
        print(result)

    return "hi"