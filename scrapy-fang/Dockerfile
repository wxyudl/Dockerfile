FROM python:3.6

RUN apt-get update && pip install scrapy
RUN apt-get install cron vim --assume-yes

RUN mkdir /scrapy
WORKDIR /scrapy
RUN scrapy startproject fang

COPY utils.py fang_spider.py /scrapy/fang/fang/spiders/
COPY items.py settings.py /scrapy/fang/fang/
COPY run_spider.sh /scrapy/fang/
ADD crontab /etc/cron.d/scrapy-cron

WORKDIR /scrapy/fang