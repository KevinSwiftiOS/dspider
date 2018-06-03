# -*- coding:utf-8 -*-
from .field import Fieldlist
from .tabsetup import TabSetup
from .listcssselector import ListCssSelector
from .mongodb import Mongodb

class Page(object):
    def __init__(self, name='', fieldlist=Fieldlist(), is_save=False, mongodb=Mongodb(), listcssselector=ListCssSelector(), tabsetup=TabSetup()):
        """

        :param name:
        :param fieldlist:
        :param is_save:
        :param mongodb:
        :param listcssselector:
        :param tabsetup:
        """
        self.name = name
        self.fieldlist = fieldlist
        self.is_save = is_save
        self.mongodb = mongodb
        self.listcssselector = listcssselector
        self.tabsetup = tabsetup

    def __str__(self):
        if not self.name or self.fieldlist == None:
            return str(None)
        else:
            result = {'name':self.name,'is_save':self.is_save}
            if self.fieldlist != None:
                result.setdefault('fieldlist',str(self.fieldlist))
            if self.is_save:
                result.setdefault('mongodb',str(self.mongodb))
            if self.listcssselector != None:
                result.setdefault('listcssselector',str(self.listcssselector))
            if self.tabsetup != None:
                result.setdefault('tabsetup',str(self.tabsetup))
            return str(result).replace('\\','')

    def __eq__(self, other):
        if other is None:
            return not self.name or self.fieldlist == None
        else:
            if vars(other) == vars(self):
                return True
            else:
                super.__eq__(self, other)

    def __iter__(self):
        return self

    def set_fieldlist(self, fieldlist):
        self.fieldlist = fieldlist

class PageGroup(object):
    def __init__(self, *args:Page):
        self.iter = iter(args)
        self.tuple = args

    def __iter__(self):
        return self

    def __next__(self):
        for i in self.iter:
            return i

    def __str__(self):
        return '(%s)'%','.join([str(i) for i in self.tuple])

    def __eq__(self, other):
        if other is None or other == []:
            return not self
        else:
            super.__eq__(self, other)


