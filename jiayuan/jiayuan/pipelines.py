# -*- coding: utf-8 -*-


# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
# Define your item pipelines here
#
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        self.collections = ["profile", "requirement", "life_style",
                            "financial_situation", "work", "education",
                            "marriage_view", "image"]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}".format(data))
        if valid:
            for collection in self.collections:
                if collection == item['item_name']:
                    self.db[collection].insert(dict(item))
                    logging.debug(
                        "{} added to MongoDB".format(item['item_name']))

        return item
