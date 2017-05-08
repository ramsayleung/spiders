#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# author:Samray <samrayleung@gmail.com>
import http.cookiejar
import json
import logging
import uuid
from urllib import parse, request
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request

from jiayuan.items import (EducationItem, FinancialSituationItem, ImageItem,
                           LifeStyleItem, MarriageViewItem, ProfileItem,
                           RequirementItem, WorkItem)


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
                for page_numer in range(1, 5 + 1):
                    post_data = {"sex": gender, "key": "", "stc": "",
                                 "sn": "default", "sv": 1, "p": page_numer,
                                 "f": "select", "listStyle": "bigPhoto",
                                 "pri_uid": 163251260, "jsversion": "v5"}
                    logging.debug("post data: {}".format(post_data))
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
            yield Request(url, callback=self.parse_personal_information,
                          method='GET',
                          )

    def parse_personal_information(self, response):
        items = []
        profile_item = self.parse_profile(response)
        items.append(profile_item)
        requirement_item = self.parse_requirement(response)
        items.append(requirement_item)
        life_style_item = self.parse_life_style(response)
        items.append(life_style_item)
        financial_situation = self.parse_financial_situation(response)
        items.append(financial_situation)
        work_item = self.parse_work(response)
        items.append(work_item)
        education_item = self.parse_education(response)
        items.append(education_item)
        marriage_view = self.parse_marriage_view(response)
        items.append(marriage_view)
        image_item = self.parse_image(response)
        items.append(response)
        yield items

    def parse_profile(self, response):
        profile_item = ProfileItem()
        profile_item['item_name'] = 'profile'
        profile_item['_id'] = str(uuid.uuid4())
        profile_item['username'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/text()").extract_first()
        profile_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        profile_item['introduction'] = response.xpath(
            "//div[@class='js_text']/text()").extract_first()
        profile_item['attraction_rate'] = response.xpath(
            "//div[@class='member_info_r yh']/div[1]/a/h6/text()").extract_first()
        profile_item['height'] = response.xpath(
            "//div[@class='member_info_r yh']/ul/li[2]/div[2]/em/text()").extract_first()
        profile_item['weigh'] = response.xpath(
            "//div[@class='member_info_r yh']/ul/li[6]/div[2]/em/text()").extract_first()
        profile_item['degree'] = response.xpath(
            "//div[@class='member_info_r yh']/ul/li[1]/div[2]/em/text()").extract_first()
        return profile_item

    def parse_requirement(self, response):
        requirement_item = RequirementItem()
        requirement_item['item_name'] = 'requirement'
        requirement_item['_id'] = str(uuid.uuid4())
        requirement_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        requirement_item['age'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[1]/div/text()").extract_first()
        requirement_item['height'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[2]/div/text()").extract_first()
        requirement_item['nation'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[3]/div/text()").extract_first()
        requirement_item['degree'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[4]/div/text()").extract_first()
        requirement_item['album'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[5]/div/text()").extract_first()
        requirement_item['marriage_state'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[6]/div/text()").extract_first()
        requirement_item['live_in'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[7]/div/text()").extract_first()
        requirement_item['integrity'] = response.xpath(
            "//div[@class='content_705']/div[4]/div/ul/li[8]/div/text()").extract_first()
        return requirement_item

    def parse_life_style(self, response):
        life_style_item = LifeStyleItem()
        life_style_item['_id'] = str(uuid.uuid4())
        life_style_item['item_name'] = 'life_style'
        life_style_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        life_style_item['smoke'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[1]/div/em/text()").extract_first()
        life_style_item['drink'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[2]/div/em/text()").extract_first()
        life_style_item['exercise_habit'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[3]/div/em/text()").extract_first()
        life_style_item['diet_habit'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[4]/div/em/text()").extract_first()
        life_style_item['shopping'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[5]/div/em/text()").extract_first()
        life_style_item['religious_belief'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[6]/div/em/text()").extract_first()
        life_style_item['schedule'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[7]/div/em/text()").extract_first()
        life_style_item['social_circle'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[8]/div/em/text()").extract_first()
        life_style_item['maximum_consumption'] = response.xpath(
            "//div[@class='content_705']/div[5]/div/ul/li[9]/div/em/text()").extract_first()
        return life_style_item

    def parse_financial_situation(self, response):
        financial_situation_item = FinancialSituationItem()
        financial_situation_item['_id'] = str(uuid.uuid4())
        financial_situation_item['item_name'] = 'financial_situation'
        financial_situation_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        financial_situation_item['wage'] = response.xpath(
            "//div[@class='content_705']/div[6]/div/ul/li[1]/div/text()").extract_first()
        financial_situation_item['house_purchase'] = response.xpath(
            "//div[@class='content_705']/div[6]/div/ul/li[2]/div/text()").extract_first()
        financial_situation_item['car_purchase'] = response.xpath(
            "//div[@class='content_705']/div[6]/div/ul/li[3]/div/text()").extract_first()
        financial_situation_item['financial_view'] = response.xpath(
            "//div[@class='content_705']/div[6]/div/ul/li[4]/div/text()").extract_first()
        financial_situation_item['investment_and_financial_management'] = response.xpath(
            "//div[@class='content_705']/div[6]/div/ul/li[5]/div/text()").extract_first()
        financial_situation_item['debt_loan'] = response.xpath(
            "//div[@class='content_705']/div[6]/div/ul/li[6]/div/text()").extract_first()
        return financial_situation_item

    def parse_work(self, response):
        work_item = WorkItem()
        work_item['_id'] = str(uuid.uuid4())
        work_item['item_name'] = 'work'
        work_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        work_item['position'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[1]/div/em/text()").extract_first()
        work_item['company_category'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[2]/div/em/text()").extract_first()
        work_item['company_type'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[3]/div/em/text()").extract_first()
        work_item['welfare_treatment'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[4]/div/em/text()").extract_first()
        work_item['work_status'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[5]/div/em/text()").extract_first()
        work_item['promote_possibility'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[6]/div/em/text()").extract_first()
        work_item['work_vs_family'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[7]/div/em/text()").extract_first()
        work_item['work_abord_possibility'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[1]/li[8]/div/em/text()").extract_first()
        return work_item

    def parse_education(self, response):
        education_item = EducationItem()
        education_item['_id'] = str(uuid.uuid4())
        education_item['item_name'] = 'education'
        education_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        education_item['graduated_from'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[2]/li[1]/div/em/text()").extract_first()
        education_item['major'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[2]/li[2]/div/em/text()").extract_first()
        education_item['language_skill'] = response.xpath(
            "//div[@class='content_705']/div[7]/div/ul[2]/li[3]/div/em/text()").extract_first()
        return education_item

    def parse_marriage_view(self, response):
        marriage_view_item = MarriageViewItem()
        marriage_view_item['_id'] = str(uuid.uuid4())
        marriage_view_item['item_name'] = 'marriage_view'
        marriage_view_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        marriage_view_item['native_place'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[1]/div/em/text()").extract_first()
        marriage_view_item['family_location'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[2]/div/em/text()").extract_first()
        marriage_view_item['nationality'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[3]/div/em/text()").extract_first()
        marriage_view_item['personality'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[4]/div/em/text()").extract_first()
        marriage_view_item['sense_of_humor'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[5]/div/em/text()").extract_first()
        marriage_view_item['temper'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[6]/div/em/text()").extract_first()
        marriage_view_item['about_relationship'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[7]/div/em/text()").extract_first()
        marriage_view_item['about_child'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[8]/div/em/text()").extract_first()
        marriage_view_item['marriage_time'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[9]/div/em/text()").extract_first()
        marriage_view_item['about_love_in_different_place'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[10]/div/em/text()").extract_first()
        marriage_view_item['ideal_marriage'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[11]/div/em/text()").extract_first()
        marriage_view_item['live_with_spouse_family'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[12]/div/em/text()").extract_first()
        marriage_view_item['kid_situation_in_family'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[13]/div/em/text()").extract_first()
        marriage_view_item['parents_financial_situation'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[14]/div/em/text()").extract_first()
        marriage_view_item['sibing_situation'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[15]/div/em/text()").extract_first()
        marriage_view_item['parents_situation'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[16]/div/em/text()").extract_first()
        marriage_view_item['parents_work'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[17]/div/em/text()").extract_first()
        marriage_view_item['health_insurance_about_parents'] = response.xpath(
            "//div[@class='content_705']/div[8]/div/ul[1]/li[18]/div/em/text()").extract_first()
        return marriage_view_item

    def parse_image(self, response):
        image_item = ImageItem()
        image_item['_id'] = str(uuid.uuid4())
        image_item['item_name'] = 'image'
        image_item['userid'] = response.xpath(
            "//div[@class='member_info_r yh']/h4/span/text()").extract_first().replace("ID:", "")
        image_item['image_urls'] = response.xpath(
            "id('smallImg')/div/ul/li/a/img").css('img').xpath('@_src').extract()
        return image_item

    def get_cookie(self):
        cookie = http.cookiejar.CookieJar()
        handler = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(handler)
        account_data = {"name": 15577262746, "password": "6uQs3z328rZFjdy4"}
        encoded_data = parse.urlencode(account_data).encode('utf-8')
        login_url = "http://www.jiayuan.com/login/dologin.php"
        opener.open(login_url, encoded_data)
        return cookie
