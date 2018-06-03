# -*- coding:utf-8 -*-

from spider.driver.base.field import Field,Fieldlist
from spider.driver.base.regex import Regexlist,Regex

rl = Regexlist(Regex(1,2),Regex(3,4))
f = Field(fieldname=12,regexlist=rl)
fl = Fieldlist(f,f)
print(Regexlist() == None)

