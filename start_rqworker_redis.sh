#!/bin/bash

# create crontab
crontab -l > mycron
echo "0 */12 * * * rm -rf /home/masa/Projects/SentWordScraper/app/static/images/wordcloud_images/*" >> mycron

# install crontab
crontab mycron
rm mycron

# start task-queue redis in docker container
echo "Task Queue Redis container: redis1 started..."
docker start redis1

# start cache-database redis in docker container
echo "Cache-storage Redis container: redis0 started..."
docker start redis0
# start worker node for task queue
echo "Starting Redis Queue Worker..."
rq worker

