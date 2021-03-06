# [SentWordScraper](https://www.sentwordscraper.com) - with Docker 🐋
*for non-docker implementation please switch to no-docker branch

<p align="center">
  <img width="250" height="auto" src="/app/static/images/logo.png">
</p>

# 1. Introduction

This is a little web application I built for fun.
The app is avalilable https://www.sentwordscraper.com

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
```bashli1872-187.members.linode.com/
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
  <img width="600" height="auto" src="/app/static/images/demo_imgs/sent_header_piechart.png">
</p>

<p align="center">
  <img  width="600" height="auto" src="/app/static/images/demo_imgs/sent_top_10.png">
</p>
<p align="center">
  <img width="600" height="auto" src="/app/static/images/demo_imgs/sent_worst_10.png">
</p>

<p align="center">
  <img width="600" height="auto" src="/app/static/images/demo_imgs/wc_example.png">
</p>
