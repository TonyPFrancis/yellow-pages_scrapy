# -*- coding: utf-8 -*-
import re
import requests
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import urlparse, urljoin
from scrapy.selector import Selector
from time import sleep
import urllib
from yellowpages.items import YellowpagesItem
from scrapy.http import Request, FormRequest
from dateutil import rrule, parser
from dateutil import relativedelta
from datetime import timedelta, datetime
from scrapy.log import ScrapyFileLogObserver
from scrapy import log
from scrapy.shell import inspect_response
import time
import json

class YellowpagesSpider(Spider):
    name = 'yellowpages'
    start_urls = ['http://www.yellow-pages.ph/search/schools/cebu/page-1', ]
    allowed_domains = ['yellow-pages.ph']
    TIMEZONE = ''
    BASE_URL = 'http://www.yellow-pages.ph'

    def __init__(self, name=None, **kwargs):
        ScrapyFileLogObserver(open("spider.log", 'w'), level=log.INFO).start()
        ScrapyFileLogObserver(open("spider_error.log", 'w'), level=log.ERROR).start()
        super(YellowpagesSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        sel = Selector(response)

        EVENT_LINK_XPATH = '//section[@class="regular"]//div[@class="result-img"]/a/@href'

        events = sel.xpath(EVENT_LINK_XPATH).extract()
        if events:
            for event_link in events:
                event_link = event_link if event_link.startswith('http') else self.BASE_URL+event_link
                yield Request(url = event_link, dont_filter=True, callback=self.parse_events)
        else:
            return

        NEXT_XPATH = '//a[text()="Next"]/@href'
        next_page = sel.xpath(NEXT_XPATH).extract()
        next_page = [next_page[0] if next_page[0].startswith('http') else self.BASE_URL+next_page[0]] if next_page else ''
        if next_page:
            yield Request(url = next_page, callback=self.parse)

    def parse_events(self, response):
        item = YellowpagesItem(url = response.url)
        yield item