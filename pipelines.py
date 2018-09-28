# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import string
class NasdaqcrawlerPipeline(object):
    def process_item(self, item, spider):
        item['text'] = item['text'].strip()
        item['date_published'] = self.normalize_date(item)
        return item

    
    def normalize_date(self, item):
        date = str(item['date_published'])
        #have to get rid of a comma in the line to make it easier to read in
        #Not that kind of stripper

        date = date.translate(None, string.punctuation)
        #grabbing important parts of date
        temp =date.split(" ")
        month = temp[0]
        day = temp[1]
        year = temp[2]
        date = month + " " + day + " " + year
        
        return date
        
