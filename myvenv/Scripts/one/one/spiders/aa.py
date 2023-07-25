import scrapy
from scrapy import Request, Spider
from urllib.parse import quote
import logging
from scrapy.selector import Selector
class ByteSpider(scrapy.Spider):
    name = 'Byte'
    
    url = "https://www.google.com.hk/search?q=aa"
    offset = 0

    def start_requests(self):
        logging.debug('starting requests')
        self.offset+=1
        yield Request(url = self.url, callback = self.parse,meta = {'offset': self.offset}, dont_filter = True)

    def parse(self, response):
        # 解析下一页的数据
        # ...
        myvar = response.meta
        self.logger.error(f"Meta variable myvar = {myvar}")
        
        yield myvar
        # 获取下一页的链接
         # 使用Selector选择器选择HTML文本
        sel = Selector(text=response.text, type='html')

        # 使用ID选择器选择元素
        next_page_url = sel.css('#pnnext::attr(href)').get()
        next_page_url="https://www.google.com.hk"+next_page_url
        # next_page_url = response.xpath('//a[@id="pnnext"]/@href').get()
        self.logger.error(f"Meta variable next_page_url = {next_page_url}")
        if next_page_url:
            # 发送请求获取下一页的数据
            yield scrapy.Request(next_page_url, callback=self.parse)
   