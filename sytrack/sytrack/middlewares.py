# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from sytrack.settings import USER_AGENTS
import base64

# 代理服务器
proxyServer = ""

# 代理隧道验证信息
proxyUser = ""
proxyPass = ""
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class RandomUserAgent(object):

    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', useragent)


class RandomProxy(object):

    def process_request(self, request, spider):
        # proxy = random.choice(PROXIES)
        # request.meta['proxy'] = "http://" + proxy
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth