# SentWordScraper

<p align="center">
  <img width="320" height="200" src="/app/static/images/logo.png">
</p>

# 1. Introduction

This is a little web application I built for fun.
The app is avalilable at [URL].

Main two functionalities are:
## WordScraper
Scrapes texts from the supplied URL and then counts words, visualizes the result, and generates a wordcloud image.
## SentScraper
Scrapes texts from the supplied URL, analyzes the sentiment of each sentence and then visualizes the result.


The project was made possible by:
- **Python Flask & gnicorn**: Backend Server
- **Python Beautiful Soup**: Webscraping
- **Chart.js**: Data Visualization
- **Redis**: Task Queue & Cache Database
- **Docker & docker-compose**: Deployment

<br>

# 2. Setup

First, make sure Docker is installed and configured.
For this app to work you need to spin up a single redis container. Build one with:
```bash
docker run -d -p 6379:6379 --name redis1 redis 
```

Then pip install the required modules
```bash
pip install -r requirements.txt
```
<br>

# 3. Usage
Once the setup is complete, run the shell script ```startup.sh```
*If you name your container something other than "redis1" please change the script to match the name.
```bash
echo "Starting Task Queue Redis Container"
docker start redis1

# gunicorn
gunicorn -w 3 run:app --daemon

# start worker node for task queue
echo "Starting Redis Queue Worker"
rq worker 
```

# 4. Sample Results

<p align="center">
  <img width="600" height="800" src="/app/static/images/ss1.png">
</p>

<p align="center">
  <img width="600" height="700" src="/app/static/images/ss2.png">
</p>

<p align="center">
  <img width="600" height="400" src="/app/static/images/ss3.png">
</p>