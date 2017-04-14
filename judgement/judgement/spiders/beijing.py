# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from judgement.items import JudgementItem
import re
import time


class BeijingSpider(Spider):
    name = "beijing"
    allowed_domains = ["www.bjcourt.gov.cn"]
    start_url = 'http://www.bjcourt.gov.cn'

    def start_requests(self):
        yield Request(url=self.start_url + '/cpws/index.htm', callback=self.parse_judgements)

    def parse_judgements(self, response):
        selector = Selector(response)
        urls = selector.xpath("//*/ul[@class='ul_news_long']/li/a/@href").extract()
        for url in urls:
            url = "%s%s" % (self.start_url, url)
            yield Request(url=url, callback=self.parse_content)

    def parse_content(self, response):
        selector = Selector(response)
        title = selector.xpath("//div[@class='article_hd']/h3/text()").extract_first()
        try:
            p_date = selector.xpath("//p[@class='p_date']/text()").extract_first().split(u'：')[1]
            p_date = time.mktime(time.strptime(p_date, "%b %d, %Y"))
        except:
            p_date = None
        print title
        print p_date
