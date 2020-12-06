import redis
from flask import Flask
from rq import Queue

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379, password='Masa1014')
q = Queue(connection=r)

from app import tasks
from app import views
