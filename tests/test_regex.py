# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse
with open('/home/wjl/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
tag_list = []
for i in list(p('span').items())[1:]:
    tag_list.append(i.text())
print(json.dumps(tag_list, ensure_ascii=False))

