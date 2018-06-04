# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse
with open('/home/mininet/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
grade_list = []
for i in p('div.hotel_user_remark > div.u2 > div.k3').items('div.label'):
    grade_list.append({i('div.name').text():i('div.score').text()})
comment_num_list = p('div.hotel_user_remark > div.tradeoffConclude').text().split(' ')
print(json.dumps({'grade_list':grade_list,'comment_num_list':comment_num_list},ensure_ascii=False))

