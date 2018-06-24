# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse
import xmltodict
with open('/home/mininet/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
p_ticket = p('#J-Ticket')
#一级标题
for i in p_ticket('div.ticket-detail-title').items():
    if not i.attr('style'):#一级标题没有style
        text = "%s"%i.text()
        i.replace_with("<ticket class='head-level-1'>%s</ticket>"%text)
#二级标题
for i in p_ticket('div.ticket-detail-title').items():
    if i.attr('style'):#一级标题有style
        text = "%s"%i.text()
        i.replace_with("<ticket class='head-level-2'>%s</ticket>"%text)
#三级标题
for i in p_ticket('table.ttd-hairline-top').items():
    if 'ticket-table' not in i.attr('class'):
        info_list = i.text().split('\n')[:-1]
        info_dict = {'名称':info_list[0], '参考门市价':info_list[1], '价格':info_list[2]}
        text = "%s"%json.dumps(info_dict,ensure_ascii=False)
        i.replace_with("<ticket class='head-level-3'>%s</ticket>"%text)
#正文
for i in p_ticket('table.ticket-table').items():
    thead_list = []
    for j in i('thead').items('td'):
        thead_list.append(j.text())
    tbody_dict_list = []
    for j in i('tbody').items():
        tbody_dict = {}
        for k in range(1, len(thead_list)+1):
            tbody_dict.setdefault(thead_list[k-1], j('td:nth-child(%s)'%k).text())
        tbody_dict_list.append(tbody_dict)
    text = "%s"%json.dumps(tbody_dict_list,ensure_ascii=False)
    i.replace_with("<ticket class='content'>%s</ticket>"%text)
from lxml import etree
root = etree.Element('ticket')
pointer = root
h1 = None
h2 = None
h3 = None
for i in p_ticket('ticket').items():
    if i.attr('class') == 'head-level-1':
        pointer = root
        pointer = etree.SubElement(pointer, 'h1')
        pointer.attrib['name'] = '%s'%i.text()
        h1 = pointer
    if i.attr('class') == 'head-level-2':
        pointer = h1
        pointer = etree.SubElement(pointer, 'h2')
        pointer.attrib['name'] = '%s'%i.text()
        h2 = pointer
    if i.attr('class') == 'head-level-3':
        pointer = h2
        pointer = etree.SubElement(pointer, 'h3')
        pointer.attrib['name'] = '%s'%i.text()
        h3 = pointer
    if i.attr('class') == 'content':
        pointer = etree.SubElement(pointer, 'content')
        pointer.text = "%s"%i.text()
        pointer = h3
tickets = str(etree.tostring(root, pretty_print=True, encoding='utf-8'), 'utf-8')
tickets= json.loads(json.dumps(xmltodict.parse(tickets), ensure_ascii=False))
print(tickets)
