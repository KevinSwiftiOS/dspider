# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse
with open('/home/wjl/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
print(json.dumps({'grade_list':p('div:nth-child(3) > div.review-filter > ul.ta-list.clearfix > li.taService').text().split('\n'),
                  'comment_num_list':p('div:nth-child(3) > div.review-filter > ul.filter-list.clearfix').text().split('\n')[1:]},ensure_ascii=False))