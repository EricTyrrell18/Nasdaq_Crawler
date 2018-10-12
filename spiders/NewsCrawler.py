# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join

from NasdaqCrawler.items import NasdaqcrawlerItem 

import re

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.nasdaq.com']
    stock_tickers = ['aapl', 'msft', 'googl']
    start_urls = ['https://www.nasdaq.com/symbol/'+ ticker + '/news-headlines/' for ticker in stock_tickers]
    # Nasdaq.com/robots.txt requests a 30 second crawl delay
    #Nasdaq might ban your ip if you delete this
    download_delay = 32.0
    
    def parse(self, response):
        """scrapes all articles from the aappl/news-headlines"""
        next_selector = response.xpath('//div//li/a[@id="quotes_content_left_lb_NextPage"]/@href')
        ticker = re.findall('symbol/(.+?)/', response.url)[0]

        for url in next_selector.extract():
            yield Request(url, callback = self.parse)
            
        links = response.xpath('//div//span[@class="fontS14px"]/a/@href').extract()
        for link in links:
            # meta is passed along with the response into the spider
            # allowing it to access what ticker it's using
            yield Request(link, callback = self.parse_articles, meta = {'ticker': ticker})
        
    def parse_articles(self, response):
        """scrapes the articles for author, date, text"""
        item = NasdaqcrawlerItem()
        item['date_published'] = response.xpath('//span[@itemprop="datePublished"]/text()').extract()
        item['text'] = "".join(self.clean_text(response.xpath('//div[@id="articlebody"]//p//text()').extract()))
        item['title'] = response.xpath('//h1/text()').extract()
        item['stock_ticker'] = response.meta['ticker']
        # captures any text between symbol/ and /
        # this should only return a single item
       
        yield item

    def clean_text(self, text):
        for each in text:
            # allows join to be called on the colleciton
            yield each.strip()
    

