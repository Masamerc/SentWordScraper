from app import app
from app import r
from app.tasks import count_words
from app import q 
from flask import render_template, request, redirect, url_for
from time import strftime 
from util import SqliteWrapper


@app.route('/')
def index():
    return "Hello You, go to '/add-task for demoing the app'"


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
            return redirect(url_for(".show_result", url=url))

    return render_template('add_task.html', message=message, jobs=jobs)


############ Route Result Screen ############

@app.route('/result')
def show_result():

        url = 'https://www.npr.org/2020/03/24/820271472/tom-nook-take-me-away-animal-crossing-new-horizons-is-a-perfect-escape'
        # url = request.args['url']
        
        # SQL query to get top 30 recorded  words  
        with SqliteWrapper('word.db') as db:
            query = db.execute(f'''select * from words where source = ?
                                    order by count desc LIMIT 30;''', (url,))
            top_30_words = []

            for data in query.fetchall():
                ind, ts, word, count, source = data
                top_30_words.append((word, count))
                time_stamp = ts

        return render_template('result.html', url=url, top_30_words=top_30_words, time_stamp=time_stamp)


############ All Results ############

@app.route('/all-results', methods=['GET', 'POST'])
def show_all_results():

    if request.args:
        print("Arg received")

        keyword = request.args['keyword']

        with SqliteWrapper('word.db') as db:
            word_query = db.execute('''select * from words where source LIKE ? 
                                    order by count desc LIMIT 100;''', ("%"+ keyword + "%",))

            

            all_words = []
            sources = []

            for data in word_query.fetchall():
                ind, ts, word, count, source = data
                all_words.append((word, count))

            source_query = db.execute('select source, max(scraped_at) from words where source LIKE ? group by source;', ("%"+ keyword + "%",))

            for data in source_query.fetchall():
                source, ts = data
                sources.append((source, ts))

        message = f"Showing results that matched the keyword: {keyword}"
        print(sources)

        return render_template('all_results.html', all_words=all_words, message=message, sources=sources)


    with SqliteWrapper('word.db') as db:
            query = db.execute(f'''select * from words 
                                    order by count desc LIMIT 100;''')
            all_words = []

            for data in query.fetchall():
                ind, ts, word, count, source = data
                all_words.append((word, count))

            message = "Showing All Results: No keyword supplied or keyword did not match any source"

    return render_template('all_results.html', all_words=all_words, message=message)


############ Route for Testing ############

@app.route('/test')
def test():
    with SqliteWrapper('word.db') as db:
        q = db.execute("select * from words LIMIT 5;")
        result = q.fetchall()

    if result:
        print(result)

    return "hi"