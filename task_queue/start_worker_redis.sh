#!/bin/bash

# activate venv 
# source ../env/bin/activate

# start redis in docker container
docker start redis1

# start worker node for task queue
rq worker