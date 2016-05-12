# -*- coding: utf-8 -*-
import scrapy

from shoe.items import ShoeItem
from .. import items
from scrapy import  Request



#from scrapy.contrib.spiders import CrawlSpider, Rule

class shoeSpider(scrapy.Spider):
    name = "shoe"
    allowed_domains = ["hepsiburada.com"]
    start_urls = [ "http://www.hepsiburada.com/erkek-ayakkabilar-c-60000117?siralama=yorumsayisi"]

    def parse(self,response):
        base_url2="http://www.hepsiburada.com/erkek-ayakkabilar-c-60000117?sayfa=%s&siralama=yorumsayisi"
        for i in range(1,23):
            yield Request(base_url2 % i,self.parse2)
    def parse2(self, response):
        shoe_links=response.css("li.search-item > div > a::attr(href)").extract()
        base_url="http://www.hepsiburada.com%s"
        for link in shoe_links:
            yield Request(base_url % link , self.parse_brand)

    def parse_brand(self,response):
        base_url=response.url +"-yorumlari"
        item= items.ShoeItem()
        brand = response.css("table.data-list:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > a::text").extract()
        item['brand']=brand[0]
        yield Request(base_url , self.parse_shoe, meta={"item":item})

    def parse_shoe(self,response):
        item= response.meta["item"]
        li = response.xpath("//li[@class='review-item']")
        for i in li:
            comment=i.xpath("p[@class='review-text']/text()").extract()
            item['comment'] = comment[0].encode('utf-8')
            yield item
            # print(item['comment'])

        #comment = response.css("li.review-item > p::text").extract()