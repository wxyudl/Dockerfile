#!/bin/bash

DATE=`date +%Y%m%d`

cd /scrapy/fang/
PATH=$PATH:/usr/local/bin
export PATH

scrapy crawl fang -o fang-$DATE.csv

mv /scrapy/fang/fang-$DATE.csv /scrapy/fang/playdata/Fang/data

# Push CSV file to github
cd /scrapy/fang/playdata
git add .
git commit -m 'new data'
git push
