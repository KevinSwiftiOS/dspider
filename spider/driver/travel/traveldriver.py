# -*- coding:utf-8 -*-

from spider.driver.base.driver import *
from spider.driver.base.field import FieldName
from spider.driver.base.mongodb import Mongodb

class WebsiteName(object):
    """
    旅游网站名称
    """
    XIECHENG = '携程'
    DINGPING = '大众点评'
    FLIGGY = '飞猪'
    QUNAR = '去哪儿'
    LVMAMA = '驴妈妈'
    TUNIU = '途牛'
    MAFENGWO = '马蜂窝'
    ELONG = '艺龙'

WEBSITE_NAME_LIST = (lambda d:list({key:d[key] for key in d if '_' not in key}.values()))(vars(WebsiteName))

class DataSourceName(object):
    """
    数据来源名称
    """
    SPOT = '景点'
    HOTEL = '酒店'

DATASOURCE_NAME_LIST = (lambda d:list({key:d[key] for key in d if '_' not in key}.values()))(vars(DataSourceName))

class TravelSpiderName(object):
    """
    旅游网站爬虫的名称
    """
    XIECHENG_SPOT = WebsiteName.XIECHENG + DataSourceName.SPOT
    XIECHENG_HOTEL = WebsiteName.XIECHENG + DataSourceName.HOTEL
    DIANPING_SPOT = WebsiteName.DINGPING + DataSourceName.SPOT
    DIANPING_HOTEL = WebsiteName.DINGPING + DataSourceName.HOTEL
    FLIGGY_SPOT = WebsiteName.FLIGGY + DataSourceName.SPOT
    FLIGGY_HOTEL = WebsiteName.FLIGGY + DataSourceName.HOTEL
    QUNAR_SPOT = WebsiteName.QUNAR + DataSourceName.SPOT
    QUNAR_HOTEL = WebsiteName.QUNAR + DataSourceName.HOTEL
    LVMAMA_SPOT = WebsiteName.LVMAMA + DataSourceName.SPOT
    LVMAMA_HOTEL = WebsiteName.LVMAMA + DataSourceName.HOTEL
    TUNIU_SPOT = WebsiteName.TUNIU + DataSourceName.SPOT
    TUNIU_HOTEL = WebsiteName.TUNIU + DataSourceName.HOTEL
    MAFENGWO_SPOT = WebsiteName.MAFENGWO + DataSourceName.SPOT
    MAFENGWO_HOTEL = WebsiteName.MAFENGWO + DataSourceName.HOTEL
    ELONG_HOTEL = WebsiteName.ELONG + DataSourceName.HOTEL

class TravelDriver(Driver):
    host = '127.0.0.1'
    port = 27017
    db = 'dspider2'
    shop_collection = 'shops'
    comments_collection = 'comments'

    website_name = WebsiteName()
    website_name_list = WEBSITE_NAME_LIST
    datasource_name = DataSourceName()
    datasource_name_list = DATASOURCE_NAME_LIST
    travel_spider_name = TravelSpiderName()

    def __init__(self,isheadless=False,ismobile=False,isvirtualdisplay=False,spider_id='',
                 data_website='',
                 data_region='',
                 data_source=''):
        """
        isvirtualdisplay的优先级高于isheadless
        :param isheadless:
        :param ismobile:
        :param isvirtualdisplay:
        :param spider_id:
        :param data_website:
        :param data_region:
        :param data_source:
        """
        Driver.__init__(self,log_file_name=spider_id,ismobile=ismobile,isvirtualdisplay=isvirtualdisplay,isheadless=isheadless)
        if not data_website or not data_source or not data_region:
            self.error_log('data_website or data_source or data_region can not none!!!')
            raise ValueError
        self.data_website = data_website
        self.data_region = data_region
        self.data_source = data_source
        self.logger.debug('%s-%s-%s'%(self.data_website,self.data_region,self.data_source))
        self.data_key = {
            FieldName.DATA_WEBSITE: self.data_website,
            FieldName.DATA_REGION: self.data_region,
            FieldName.DATA_SOURCE: self.data_source,
        }