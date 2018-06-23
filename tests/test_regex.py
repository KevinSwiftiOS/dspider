# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse

with open('/home/wjl/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
for i in p('#J-Ticket > div').items('table.ticket-table'):
    print(i.parent().text())
    break