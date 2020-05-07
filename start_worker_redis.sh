#!/bin/bash

# start redis in docker container
echo "Redis container: redis1 started..."
docker start redis1

# start worker node for task queue
echo "Starting Redis Queue Worker..."
rq worker