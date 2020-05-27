FROM python:3-slim
RUN mkdir usr/src/app
WORKDIR usr/src/app
COPY . .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt

