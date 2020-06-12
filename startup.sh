#!/bin/bash

# create crontab
# crontab -l > mycron
# echo "0 */12 * * * rm -rf /home/masa/Projects/SentWordScraper/app/static/images/wordcloud_images/*" >> mycron

# install crontab
# crontab mycron
# rm mycron

# run & create redis docker 
# docker run -d -p 6379:6379 --name redis1 redis

# start task-queue redis in docker container
echo "Task Queue Redis container: redis1 started..."
docker start redis1

# start worker node for task queue
echo "Starting Redis Queue Worker..."
rq worker