# -*- coding:utf-8 -*-

import re

print(re.sub(r'^[\d.]*[^\d]*([\d]*)[^\d]*$',r'\1','4.8&nbsp;棒极了共6886条点评收藏'))

