from app import app
from app import r
from app.tasks import count_words
from app import q 
from flask import render_template, request
from time import strftime 

@app.route('/')
def index():
    return "Hello You, go to '/add-task for demoing the app'"


### Scrapes Website & Count Words ###
@app.route('/add-task', methods=["GET", "POST"])
def add_task():
    # shows what jobs in queue
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

    return render_template('add_task.html', message=message, jobs=jobs)

