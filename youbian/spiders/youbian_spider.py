# -*- coding: utf-8 -*-
import html2text
import scrapy
from youbian.items import YoubianItem
import html2text


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
        import ipdb
        ipdb.set_trace()
        item = YoubianItem()
        code = response.css('.success h1::text').extract()
        item['code'] = code
        res = response.css('td[width="649"]::text').extract()
        test = res[0].strip("'u")
        test = res[0].split("'u")
        test_1 = test.encode('utf-8', 'ignore')
        print test_1
        print '@@'*20
        # print test.encode('GB18030')
        # print '@@'*20
        # converter = html2text.HTML2Text()
        # converter.ignore_links = True
        # for i in res:
        #     print converter.handle(i.decode('utf-8', 'ignore'))
        #     print "@@"*10


        # def is_str(s):
        #     return isinstance(s, basestring)
        # a = is_str(res)  # 经判断不是res不是str,是unicode,(str.decode/unicode.encode)
        # print a
        # print '@@'*20
        # converter = html2text.HTML2Text()
        # converter.ignore_links = True
        # print converter.handle(i.encode('gbk', 'ignore'))
        # with open('D:/bbb.txt', 'w') as f:
        #     f.write(res[0].encode('gbk', 'ignore'))
        # print res[0].encode('gbk')
        # print '@@'*20
        # converter = html2text.HTML2Text()
        # print converter.handle(unicode(res).encode('gbk', 'ignore'))





