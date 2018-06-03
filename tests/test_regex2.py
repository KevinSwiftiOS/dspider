# -*- coding:utf-8 -*-

import re

print(re.sub(r'^.*来自([\d]*)条点评.*$',r'\1','97%好评率来自416条点评'))

