# SentWordScraper - with Docker 🐋
*for non-docker implementation please switch to no-docker branch

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

# 2. Usage

First, make sure Docker & Docker Compose is installed and configured.
In the root directory of this project, run:
```bash
docker-compose build
```

Once all required containers are built, run the app by:
```bash
docker-compose up
```
Beware that by default nginx forwards all the requests to port ```80``` of the host machine.
It's likely another process is already using that port, in which case try killing that process or reconfigure ports in ```docker-compose.yaml```

<br>

# 3. Sample Results

<p align="center">
  <img width="320" height="200" src="/app/static/images/ss1.png">
</p>

<p align="center">
  <img width="320" height="200" src="/app/static/images/ss2.png">
</p>

<p align="center">
  <img width="320" height="200" src="/app/static/images/ss3.png">
</p>