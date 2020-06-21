FROM python:3.7
RUN mkdir usr/src/app
WORKDIR usr/src/app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install cron
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt

