#!/usr/bin/env python
# encoding: utf-8
# @author   : changhsing
# @time     : 2020/8/3 23:12
# @site     : 
# @file     : test.py
# @software : PyCharm
import requests

header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN',
    'User-Agent': 'ApiPOST Runtime +https://www.apipost.cn'
}
re = requests.get(url='https://www.zhihu.com/api/v4/search/top_search', headers=header)
j = re.json()['top_search']['words']
r = []
for i in j:
    r.append(i['display_query'])
print(r)