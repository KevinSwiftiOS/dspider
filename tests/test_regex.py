# -*- coding:utf-8 -*-

import re,json
from pyquery import PyQuery
from urllib.parse import urlparse
with open('/home/wjl/test.txt', 'r') as f:
    _str = f.read()
p = PyQuery(_str)
statistics = {}
# 点评
dianping = []
for i in p('div.comment_sumary_box>div.comment_total_score').items('span'):
    (lambda x: dianping.append(x.strip()) if x else '')(i.text())
for i in p('div.comment_sumary_box>div.bar_score').items('p'):
    text = i.text()
    dianping.append({re.sub(r'[^\u4e00-\u9fa5]', '', text):re.sub(r'[^\d.]', '', text)})
statistics.setdefault('点评', dianping)
# 印象
impression = []
count = 0
for i in p('div.user_impress').items('a'):
    count += 1
    text = i.text()
    impression.append({(lambda x: x if x else '第一个%s' % count)(re.sub(r'[^\u4e00-\u9fa5]', '', text)): re.sub(
        r'[^\d]', '', text)})
statistics.setdefault('印象', impression)
left = []
for i in p('div.comment_box_bar_new.clearfix > div.bar_left').items('a'):
    left.append({re.sub(r'[^\u4e00-\u9fa5]*','',i.text()):re.sub(r'[^\d]*','',i.text())})
statistics.setdefault('评论好评统计',left)
right = []
for i in p('div.comment_box_bar_new.clearfix > div.bar_right > select.select_room').text().split('\n')[1:]:
    right.append({re.sub(r'[^\u4e00-\u9fa5]*','',i):re.sub(r'[^\d]*','',i)})
statistics.setdefault('评论房型统计',right)
print(json.dumps(statistics, ensure_ascii=False))

