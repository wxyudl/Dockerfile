FROM debian:stretch

RUN apt-get update && apt-get upgrade && apt-get install build-essential --assume-yes
RUN apt-get install wget --assume-yes
RUN apt-get install python --assume-yes

WORKDIR /opt
RUN wget https://nodejs.org/dist/v4.4.7/node-v4.4.7.tar.gz
RUN tar -xvf node-v4.4.7.tar.gz
WORKDIR ./node-v4.4.7
RUN ./configure && make install
WORKDIR /opt
RUN npm install forever -g && npm install elasticsearch

RUN wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.2/elasticsearch-2.3.2.deb
RUN pkg -i elasticsearch.*

RUN wget https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v1.9.2/elasticsearch-analysis-ik-1.9.2.zip
