# -*- coding: utf-8 -*-

import json
import requests
from pyquery import PyQuery as pq


proxies = {
    'http': 'http://182.90.13.46:80',  # 代理，反爬虫的方式之一
}


def get_first_url(url):
    r = requests.get(url)
    d = pq(r.text)
    first_class_url = []
    first_class_nodes = d('.lh22 .citysearch ul a')
    for node in first_class_nodes:
        dollar = pq(node)
        url = dollar.attr('href')
        first_class_url.append('http://www.yb21.cn' + url)  # 不加前缀的话，读出的URL会不全，最终会报错
    return first_class_url


def get_second_url(url):
    r = requests.get(url)
    d = pq(r.text)
    second_class_url = []
    second_class_nodes = d('tbody tr[align] td strong a')
    for node in second_class_nodes:
        dollar = pq(node)
        url = dollar.attr('href')
        second_class_url.append('http://www.yb21.cn' + url)  # 同上
    return second_class_url


def get_third_class_info(url):
    r = requests.get(url, proxies=proxies)  # 代理
    r.encoding = 'gbk'  # 编码解决方式，scrapy这个项目不能用的原因，不了解它内部的编码方式，所以采用pyquery方式写
    d = pq(r.text)
    res = []
    code = d('.success h1').text()
    three_info = d('td[width="649"]').text().split('-')
    province = three_info[0]
    city = three_info[1]
    district = three_info[2]
    address_nodes = d('td[bgcolor="#f9f9f9"] .lh22 tr').remove('td[colspan]')
    for item in pq(address_nodes)('td'):  # 读地址时，让它们一行行显示，方便去加入
        addr = pq(item).text()
        addr.replace(u'邮编', '').replace(u'邮政编码', '')  # 去掉字符串末尾的无用字符
        res.append({'code': code, 'province': province, 'city': city, 'district': district, 'addr': addr})  # 一次性加入列表中
    return res


def run():
    urls = []
    res = []
    # first_class_url = get_first_url('http://www.yb21.cn')
    # for url in first_class_url:
    #     print 'now crawl: %s' % url # 打log，方便调试
    #     second_class_url = get_second_url(url)
    #     urls.extend(second_class_url)
    # print 'first class complete!'
    # with open('urls.json', 'w') as f: # 打开文件
    #     f.write(json.dumps(urls)) # 写文件，参数必须是字符串，dumps是把url变成了一个字符串
    # print len(urls)

    with open('urls.json', 'r') as f:
        data = f.read()
        urls = json.loads(data)
    print len(urls)  # 34021，一共要爬的数据量

    for idx, link in enumerate(urls):  # enumerate显示列表元素，同时会出现元素的编号
        print 'now crawl detail: %s' % link  # 打log
        try:
            tmp = get_third_class_info(link)
            res.extend(tmp)
        except Exception, err:
            print err
            print idx
            with open('res_%s.json' % idx, 'w') as out:
                out.write(json.dumps(res))
            return

    with open('res.json', 'w') as out:
        out.write(json.dumps(res))
    print 'complete!'


run()
