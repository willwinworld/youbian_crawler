# -*- coding: utf-8 -*-
import html2text
import scrapy
from youbian.items import YoubianItem


# 第一层获取北京市和所有的url
class YouBian(scrapy.Spider):
    name = 'youbian'
    download_delay = 0.5
    allowed_domains = ['yb21.cn']
    start_urls = ['http://www.yb21.cn/']

    def parse(self, response):
        block = response.css('.lh22 .citysearch ul a::attr(href)').extract()
        for path in block:
            url = response.urljoin(path)
            yield scrapy.Request(url, callback=self.parse_sec)
            break

    def parse_sec(self, response):
        block = response.css('tbody tr[align] td strong a::attr(href)').extract()
        for path in block:
            url = response.urljoin(path)
            yield scrapy.Request(url, callback=self.parse_thd)
            break

    def parse_thd(self, response):
        item = YoubianItem()
        code = response.css('.success h1::text').extract()
        item['code'] = code
        res = response.css('td[width="649"]::text').extract().pop()
        print res
        print '##'*20
        # with open('D:/bbb.txt', 'w') as f:
        #     f.write(res[0].encode('gbk', 'ignore'))
        # print res[0].encode('gbk')
        # print '@@'*20
        # converter = html2text.HTML2Text()
        # print converter.handle(unicode(res).encode('gbk', 'ignore'))





