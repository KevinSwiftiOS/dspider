# -*- coding:utf-8 -*-

from spider.driver.base.field import *
from spider.driver.travel.traveldriver import WebsiteName,DataSourceName,TravelDriver
from spider.driver.base.mongodb import Mongodb
import re
import json
shops = Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection,host='10.1.17.15').get_collection()
comments = Mongodb(db=TravelDriver.db,collection=TravelDriver.comments_collection).get_collection()
key = {
    FieldName.DATA_SOURCE:DataSourceName.HOTEL,
    FieldName.DATA_WEBSITE:WebsiteName.FLIGGY,
}
print(shops.remove(key))



