# SentWordScraper - with Docker 🐋
*for non-docker implementation please switch to no-docker branch
<center>

![logo](/app/static/images/logo.png)

</center>

# 1. Introduction

This is a little web application I built for fun.
The app is deployed at [URL].

Main two functionalities are:
## WordScraper
Description Here
## SentScraper
Description Here


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


# 3. Hello