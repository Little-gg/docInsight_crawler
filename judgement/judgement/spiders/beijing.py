# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from judgement.items import JudgementItem
import re
import time
from selenium import webdriver


class BeijingSpider(Spider):
    name = "beijing"
    allowed_domains = ["www.bjcourt.gov.cn"]
    start_url = 'http://www.bjcourt.gov.cn'

    def __init__(self):
        # Need to install chromedriver first
        # brew install chromedriver on MacOS
        self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.close()

    def start_requests(self):
        yield Request(url=self.start_url + '/cpws/index.htm', callback=self.parse_judgements)

    def parse_judgements(self, response):
        self.driver.get(response.url)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath("//span[@class='sp_next']")
                next_page.click()
                self.check_pause(self.driver)
                self.find_yzm(self.driver)
                urls_elements = self.driver.find_elements_by_xpath("//ul[@class='ul_news_long']/li/a")
                for url_element in urls_elements:
                    url = url_element.get_attribute("href")
                    yield Request(url=url, callback=self.parse_content)
            except:
                break

        self.driver.close()

    def parse_content(self, response):
        driver = webdriver.Chrome()
        driver.get(response.url)
        self.check_pause(driver)
        self.find_yzm(driver)
        title = driver.find_element_by_xpath("//div[@class='article_hd']/h3").text
        try:
            p_date = driver.find_element_by_xpath("//p[@class='p_date']").text.split(u'：')[1]
            p_date = time.mktime(time.strptime(p_date, "%b %d, %Y"))
        except:
            p_date = 0
        content = driver.find_element_by_xpath("//div[@class='article_con']").text
        judgement_item = JudgementItem()
        judgement_item["url"] = response.url
        judgement_item["title"] = title
        judgement_item["publish_date"] = p_date
        judgement_item["content"] = content
        driver.close()
        yield judgement_item

    def find_yzm(self, driver):
        try:
            driver.find_element_by_xpath('//img[@id="yzmImg"]')
            driver.save_screenshot('yzm.png')
            yzm = driver.find_element_by_xpath('//input[@id="yzmInput"]')
            yzm.clear()
            yzm_input = raw_input("查看yzm.png并输入验证码")
            yzm.send_keys(yzm_input)
            submit = driver.find_element_by_xpath('//a[@id="loginBtn"]')
            submit.click()
            # x = yzm_img.location['x']
            # y = yzm_img.location['y']
            # from PIL import Image
            # yzm = Image.open('yzm_.jpg')
            # yzm.crop(x, y, x+70, y+43).save('yzm.jpg')
        except:
            pass

    def check_pause(self, driver):
        try:
            driver.find_element_by_xpath('//div[@class="error_c"]')
            raw_input("访问频率太高，等待...")
        except:
            pass
