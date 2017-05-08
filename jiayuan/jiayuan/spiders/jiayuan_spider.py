#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# author:Samray <samrayleung@gmail.com>
import http.cookiejar
import json
import logging
from urllib import parse, request
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request

from jiayuan.items import (EdutationItem, FinancialSituationItem, ImageItem,
                           LifeStyleItem, ProfileItem, RequirementItem,
                           WorkItem)


class JiaYuanSpider(scrapy.Spider):
    name = "jiayuan"
    start_urls = ['http://www.jiayuan.com/']

    def __init__(self):
        self.gender_total_page = {'f': 60114, 'm': 84951}
        self.cookies = self.get_cookie()
        self.search_url = "http://search.jiayuan.com/v2/search_v2.php"

    def start_requests(self):
        post_data = {"sex": "m", "key": "", "stc": "", "sn": "default",
                     "sv": 1, "p": 1, "f": "select", "listStyle": "bigPhoto",
                     "pri_uid": 163251260, "jsversion": "v5"}
        yield Request(url=self.search_url, meta={'cookiejar': self.cookies},
                      method="POST", body=parse.urlencode(post_data),
                      callback=self.parse)

    def parse(self, response):
        # check login succeed before going on
        if r"/login/err.php?err_type=2&pre_url=" in response.css('script::text').extract():
            self.logger.error("Login failed")
            return
        # We've successfully authenticated, let's have some fun!
        else:
            for gender, total_page in self.gender_total_page.items():
                for page_numer in range(1, 20 + 1):
                    post_data = {"sex": gender, "key": "", "stc": "",
                                 "sn": "default", "sv": 1, "p": page_numer,
                                 "f": "select", "listStyle": "bigPhoto",
                                 "pri_uid": 163251260, "jsversion": "v5"}
                    yield Request(url=self.search_url,
                                  method="POST",
                                  meta={'cookiejar': self.cookies},
                                  body=parse.urlencode(post_data),
                                  callback=self.parse_search_result)

        # continue scraping with authenticated session...
    def parse_search_result(self, response):
        response_broken_json = str(response.body, 'utf-8')
        response_broken_json.replace('##jiayser##', '')
        response_fixed_json = response_broken_json.replace(
            r'##jiayser##\\', '')
        result = json.loads(response_fixed_json)
        user_info = result.get('userInfo')
        user_id = [info.get("realUid") for info in user_info]
        user_id = list(map(str, user_id))
        user_profile_url = [urljoin('http://www.jiayuan.com', id)
                            for id in user_id]
        for url in user_profile_url:
            self.logger.debug("user url: %s", url)
            yield Request(url, callback=self.parse_profile, method='GET',
                          )

    def parse_profile(self, response):
        items = []
        profile_item = ProfileItem()
        profile_item['username'] = response.xpath(
            "//div[5]/div/div[1]/div[2]/h4/text()").extract()
        profile_item['userid'] = response.xpath(
            '//div[5]/div/div[1]/div[2]/h4/span/text()').extract().replace("ID:", "")
        profile_item['introduction'] = response.xpath(
            "//div[6]/div[1]/div[2]/div/div/text()").extract()
        profile_item['attraction_rate'] = response.xpath(
            "//div[5]/div/div[1]/div[2]/div[1]/a/h6").extract()
        profile_item['height'] = response.xpath(
            "//div[5]/div/div[1]/div[2]/ul/li[2]/div[2]/em").extract()
        profile_item['weigh'] = response.xpath(
            "//div[5]/div/div[1]/div[2]/ul/li[6]/div[2]/em").extract()
        profile_item['degree'] = response.xpath(
            "//div[5]/div/div[1]/div[2]/ul/li[1]/div[2]/em")

    def parse_requirement(self, response):
        pass

    def parse_lift_style(self, response):
        pass

    def parse_financial_situation(self, response):
        pass

    def parse_work(self, response):
        pass

    def parse_educatin(self, response):
        pass

    def parse_marriage_view(self, response):
        pass

    def parse_image(self, response):
        image_urls = response.xpath(
            "id('smallImg')/div/ul/li/a/img").css('img').xpath('@_src').extract()

    def get_cookie(self):
        cookie = http.cookiejar.CookieJar()
        handler = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(handler)
        account_data = {"name": 15577262746, "password": "6uQs3z328rZFjdy4"}
        encoded_data = parse.urlencode(account_data).encode('utf-8')
        login_url = "http://www.jiayuan.com/login/dologin.php"
        opener.open(login_url, encoded_data)
        return cookie
