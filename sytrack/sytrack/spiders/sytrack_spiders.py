#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from sytrack.items import SytrackItem
from sytrack.spiders.OrderNo import Orderno
from sytrack.settings import USER_AGENTS
import random
import json
import datetime
import jsonpath


class SytrackSpider(scrapy.Spider):
    """
    顺友国际订单
    """
    name = 'sytrack'
    allow_domains = ['sypost.net']

    useragent = random.choice(USER_AGENTS)
    headers = {
        'Use-Agent': useragent,
        'Host': 'www.sypost.net',
    }

    def start_requests(self):
        url = 'http://www.sypost.net/query'
        orderno = Orderno()
        syb_orderno = orderno.repleni_orderno()

        for connotNo in syb_orderno:

           yield scrapy.FormRequest(url=url, headers=self.headers, formdata={"connotNo": connotNo}, callback=self.parse,
                                         meta={'tracking_number': connotNo})

    def parse(self, response):

        tracking_number = response.meta['tracking_number']

        result = json.loads(response.text)
        has = result.get('data')[0]['has']

        if has == True:
            item = SytrackItem(j=result, tracking_number=None)
            yield item

        else:
            print('无法识别的物流单号%s' % tracking_number)
            item = SytrackItem(j=None, tracking_number=tracking_number)
            yield item

