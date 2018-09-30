# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join

from NasdaqCrawler.items import NasdaqcrawlerItem 


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.nasdaq.com']
    start_urls = ['https://www.nasdaq.com/symbol/aapl/news-headlines/']
    # Nasdaq.com/robots.txt requests a 30 second crawl delay
    #Nasdaq might ban your ip if you delete this
    DOWNLOAD_DELAY = 30.0
    def parse(self, response):
        """scrapes all articles from the aappl/news-headlines"""
        next_selector = response.xpath('//div//li/a[@id="quotes_content_left_lb_NextPage"]/@href')
        

        for url in next_selector.extract():
            yield Request(url, callback = self.parse)
            
        links = response.xpath('//div//span[@class="fontS14px"]/a/@href').extract()
        for link in links:
            yield Request(link, callback = self.parse_articles)
        
    def parse_articles(self, response):
        """scrapes the articles for author, date, text"""
        item = NasdaqcrawlerItem()
        item['date_published'] = response.xpath('//span[@itemprop="datePublished"]/text()').extract()
        item['text'] = "".join(self.clean_text(response.xpath('//div[@id="articlebody"]//p//text()').extract()))
        item['title'] = response.xpath('//h1/text()').extract()
        yield item

    def clean_text(self, text):
        for each in text:
            # allows join to be called on the colleciton
            yield each.strip()
    

