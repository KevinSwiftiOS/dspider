# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery
import json
import re

class DianpingHotelSpider(TravelDriver):

    # def get_shop_info(self):
    #     try:
    #         shop_data_list = self.from_page_get_data_list(page=page_shop_1)
    #         self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1, page_func=self.page_shop_2_func)
    #     except Exception as e:
    #         self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://www.dianping.com/')
        time.sleep(2)
        self.fast_click_first_item_page_by_partial_link_text(link_text='酒店')
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#J_h-s-destn-wrap > input', text=self.data_region)
        time.sleep(2)
        self.fast_enter_page_by_css_selector(css_selector='#J_h-s-destn-wrap > input')
        self.vertical_scroll_to()#滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='下一页', func=None)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()

