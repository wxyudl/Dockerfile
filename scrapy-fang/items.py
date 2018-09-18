# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 每日房价
class FangItem(scrapy.Item):
    province     = scrapy.Field()
    city         = scrapy.Field()
    district     = scrapy.Field()
    name         = scrapy.Field() # 小区名称
    address      = scrapy.Field()
    type         = scrapy.Field() # 类型：新盘、二手房
    lng          = scrapy.Field() # 经度
    lat          = scrapy.Field() # 纬度
    year         = scrapy.Field() # 建筑年代（年）
    tv           = scrapy.Field() # 成交量（Trading Volume）
    osv          = scrapy.Field() # 在售量（On Sale Volume）
    property_fee = scrapy.Field() # 物业费
    price        = scrapy.Field() # 平均单价
    property     = scrapy.Field() # 物业
    developer    = scrapy.Field() # 开发商
    index_date   = scrapy.Field()