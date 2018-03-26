#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from sytrack.items import SytrackItem
from sytrack.spiders.OrderNo import Orderno
from sytrack.settings import USER_AGENTS
import random
import json
import datetime


class SytrackSpider(scrapy.Spider):
    """
    顺友国际订单
    """
    name = 'sytrack'
    allow_domains = ['sypost.net']

    useragent = random.choice(USER_AGENTS)
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Acccept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Use-Agent': useragent,
        'Host': 'www.sypost.net',
        'Upgrade-Insecure-Requests': 1,
        'Cache-Control': 'max-age=0',
    }

    def start_requests(self):
        url = 'http://www.sypost.net/query'
        orderno = Orderno()
        syb_orderno = orderno.repleni_orderno()
        print(len(syb_orderno))

        for connotNo in syb_orderno:

           yield scrapy.FormRequest(url=url, headers=self.headers, formdata={"connotNo": connotNo}, callback=self.parse,
                                         meta={'tracking_number': connotNo})

    def parse(self, response):

        tracking_number = response.meta['tracking_number']

        j = json.loads(response.text)

        if j['data'][0]['has'] == True:
            item = SytrackItem(j=j, tracking_number=None)
            yield item

        else:
            print('无法识别的物流单号%s' % tracking_number)
            item = SytrackItem(j=None, tracking_number=tracking_number)
            yield item

