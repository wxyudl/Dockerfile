# _*_encoding:utf-8_*_
import scrapy
import time
import datetime
from fang.items import FangItem
from fang.spiders.utils import Utils
from scrapy.http import Request
from urllib import parse
import re

utils = Utils()
class Spider(scrapy.Spider):
    # Set limit page: -1 (scrapy all page)
    limitPage = 100
    currentPage = 1
    name = "fang"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        # "https://dl.fang.lianjia.com/loupan/",
        "https://dl.lianjia.com/xiaoqu/cro11/",
    ]

    def parse(self, response):
        currentUrl = response.url

        if currentUrl.find('loupan') > 0 and response.css('.no-result-wrapper.hide'):
            for sel in response.css(".resblock-list-wrapper > li"):
                url = response.urljoin(sel.css('.resblock-name a::attr("href")').extract()[0].strip())
                name = sel.css('.resblock-name a::text').extract_first(default = '').strip()
                price = sel.css('.main-price span.number::text').extract_first(default = '').strip()
                district = sel.css('.resblock-location span:first-child::text').extract_first(default = '').strip()

                yield Request(url, callback = self.parseLoupanDetail, meta = {
                    'name': name,
                    'price': price,
                    'district': district
                })
        else:
            if response.css('.listContent > li'):
                for sel in response.css(".listContent > li"):
                    url = response.urljoin(sel.css('.title a::attr("href")').extract()[0].strip())
                    name = sel.css('.title a::text').extract_first(default = '').strip()
                    price = sel.css('.totalPrice span::text').extract_first(default = '').strip()
                    district = sel.css('.positionInfo .district::text').extract_first(default = '').strip()
                    tv = 0
                    osv = 0

                    if sel.css('.houseInfo a[href*="chengjiao"]'):
                        tv = sel.css('.houseInfo a[href*="chengjiao"]::text').extract_first(default = '').strip()
                        if len(re.findall('\d+套', tv)) > 0:
                            tv = int(re.findall('\d+套', tv)[0][:-1])
                        else:
                            tv = 0
                    if sel.css('.xiaoquListItemSellCount a span'):
                        osv = sel.css('.xiaoquListItemSellCount a span::text').extract_first(default = '').strip()
                        if len(re.findall('\d+', osv)) > 0:
                            osv = int(re.findall('\d+', osv)[0])
                        else:
                            osv = 0
                    

                    yield Request(url, callback = self.parseErshouDetail, meta = {
                        'name': name,
                        'price': price,
                        'district': district,
                        'tv': tv,
                        'osv': osv
                    })

        if self.currentPage < self.limitPage:
            self.currentPage += 1
            if currentUrl.find('loupan') > 0:
                yield scrapy.Request(url='https://dl.fang.lianjia.com/loupan/pg'+ str(self.currentPage) +'/')
            else:
                yield scrapy.Request(url='https://dl.lianjia.com/xiaoqu/pg'+ str(self.currentPage) +'cro11//')

    def parseLoupanDetail(self, response):
        item = FangItem()
        address = response.css('.where span::attr("title")').extract_first(default = '').strip()
        location = utils.getLocat(parse.quote(address))
        developer = '-'
        property = '-'
        property_fee = '-'
        price = response.meta['price']

        if len(re.findall('\d+\.?\d?', price)) > 0:
            price = int(re.findall('\d+\.?\d?', price)[0])

            if float(price) > 1500:
                for info in response.css('#house-details .box-loupan p'):
                    if info.css('span.label::text').extract_first(default = '').strip() == '开发商：':
                        developer = info.css('span.label-val::text').extract_first(default = '').strip()

                    if info.css('span.label::text').extract_first(default = '').strip() == '物业公司：':
                        property = info.css('span.label-val::text').extract_first(default = '').strip()
                    
                    if info.css('span.label::text').extract_first(default = '').strip() == '物业费用：':
                        property_fee = info.css('span.label-val::text').extract_first(default = '').strip()
                        if len(re.findall('\d+\.?\d?', property_fee)) > 0:
                            property_fee = re.findall('\d+\.?\d?', property_fee)[0]
                        else:
                            property_fee = '-'


                item["province"] = '辽宁'
                item["city"] = '大连'
                item["district"] = response.meta['district']
                item["name"] = response.meta['name']
                item["address"] = address
                item["type"] = "新房"
                item["lng"] = location['lng']
                item["lat"] = location['lat']
                item["year"] = datetime.datetime.now().year
                item["tv"] = '-'
                item["osv"] = '-'
                item["property_fee"] = property_fee
                item["price"] = price
                item["property"] = property
                item["developer"] = developer
                item["index_date"] = time.strftime("%Y%m%d", time.localtime(int(time.time())))

                yield item
            else:
                pass
        else:
            pass

    def parseErshouDetail(self, response):
        item = FangItem()
        developer = '-'
        property = '-'
        property_fee = '-'
        year = '-'
        address = response.meta['name']
        price = response.meta['price']
        tv = response.meta['tv']
        osv = response.meta['osv']

        if len(re.findall('\d+\.?\d?', price)) > 0:
            price = int(re.findall('\d+\.?\d?', price)[0])

            if float(price) > 1500:
                if tv == 0 and osv == 0:
                    pass
                else:
                    for info in response.css('.xiaoquInfo .xiaoquInfoItem'):
                        if info.css('.xiaoquInfoLabel::text').extract_first(default = '').strip() == '开发商':
                            developer = info.css('.xiaoquInfoContent::text').extract_first(default = '').strip()

                        if info.css('.xiaoquInfoLabel::text').extract_first(default = '').strip() == '物业公司':
                            property = info.css('.xiaoquInfoContent::text').extract_first(default = '').strip()
                        
                        if info.css('.xiaoquInfoLabel::text').extract_first(default = '').strip() == '物业费用':
                            property_fee = info.css('.xiaoquInfoContent::text').extract_first(default = '').strip()
                            if len(re.findall('\d+\.?\d?', property_fee)) > 0:
                                property_fee =  re.findall('\d+\.?\d?', property_fee)[0]
                            else:
                                property_fee = '-'

                        if info.css('.xiaoquInfoLabel::text').extract_first(default = '').strip() == '附近门店':
                            address = info.css('.xiaoquInfoContent::text').extract_first(default = '').strip()[1:]

                        if info.css('.xiaoquInfoLabel::text').extract_first(default = '').strip() == '建筑年代':
                            if len(re.findall('\d{4}', info.css('.xiaoquInfoContent::text').extract_first(default = '').strip())) > 0:
                                year = re.findall('\d{4}', info.css('.xiaoquInfoContent::text').extract_first(default = '').strip())[0]

                    location = utils.getLocat(parse.quote(address))

                    item["province"] = '辽宁'
                    item["city"] = '大连'
                    item["district"] = response.meta['district']
                    item["name"] = response.meta['name']
                    item["address"] = address
                    item["type"] = "二手房"
                    item["lng"] = location['lng']
                    item["lat"] = location['lat']
                    item["year"] = year
                    item["tv"] = tv
                    item["osv"] = osv
                    item["property_fee"] = property_fee
                    item["price"] = price
                    item["property"] = property
                    item["developer"] = developer
                    item["index_date"] = time.strftime("%Y%m%d", time.localtime(int(time.time())))

                    yield item
            else:
                pass
        else:
            pass

