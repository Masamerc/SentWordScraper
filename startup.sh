#!/bin/bash
# echo "0 */12 * * * rm -rf /home/masa/Projects/SentWordScraper/app/static/images/wordcloud_images/*" >> mycron


# start task-queue redis in docker container
echo "Task Queue Redis container: redis1 started..."
docker start redis1

# gunicorn
gunicorn -w 3 run:app --daemon

# start worker node for task queue
echo "Starting Redis Queue Worker..."
rq worker && gunicorn -w 3 run:app
