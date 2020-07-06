
echo "Starting Task Queue Redis Container"
docker start redis1

# gunicorn
gunicorn -w 3 run:app --daemon

# start worker node for task queue
echo "Starting Redis Queue Worker"
rq worker 

