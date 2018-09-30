# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import string
import calendar
import quandl
import config
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
        month = self.month_to_number(temp[0])
        day = temp[1]
        year = temp[2]
        date = year + "-" + str(month) + "-" + day
        
        return date
        
    def month_to_number(self, month):
        #for some reason scrapy was giving a u in front of the month
        #This could create some more errors
        #TODO: Figure out whats wrong with month
        month = month[1:4]

        #https://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
        month = str(list(calendar.month_abbr).index(month))
        #Formatting
        if len(month) < 2:
            month = '0' + month
            
        
        return month

        
