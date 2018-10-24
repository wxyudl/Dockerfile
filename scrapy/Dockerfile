FROM python:3.6

RUN apt-get update && pip install scrapy
RUN apt-get install cron vim --assume-yes

RUN mkdir -p /scrapy/shell && mkdir -p /gitlab.com/
WORKDIR /scrapy

RUN scrapy startproject xlj && mkdir -p /scrapy/xlj/data/

RUN pip3 install jieba && pip3 install langdetect && pip3 install furl