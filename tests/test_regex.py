# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse

with open('/home/mininet/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
p_ticket = p('#J-Ticket')
# p_ticket('table.ticket-table').replace_with('<ticket>123</ticket>')
#一级标题
for i in p_ticket('.ticket-detail-title').items():
    i.replace_with("<ticket class='head-level-1'>%s<ticket>"%i.text())
    print(i.html())

# ticket_set =
# for i in p('#J-Ticket > div').items('table.ticket-table'):
# ticket_list = list()
# for i in p('#J-Ticket > div').items('table.ticket-table'):
#     title = i.parent().prev()
#     if title:
#         while(True):
#             print(title.attr('class'))
#             title = title.prev()
#             if not title:
#                 break