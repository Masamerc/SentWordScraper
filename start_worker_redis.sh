#!/bin/bash

# start task-queue redis in docker container
echo "Task Queue Redis container: redis1 started..."
docker start redis1

# start cache-database redis in docker container
echo "Cache-storage Redis container: redis0 started..."
docker start redis0
# start worker node for task queue
echo "Starting Redis Queue Worker..."
rq worker