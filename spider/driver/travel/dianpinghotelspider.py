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

def get_shop_tag(self, _str):
    p = PyQuery(_str)
    tag_list = []
    for i in list(p('span').items())[1:]:
        tag_list.append(i.text())
    return json.dumps(tag_list, ensure_ascii=False)

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.hotel-info-ctn > div.hotel-info-main > h2 > a.hotel-name-link'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.hotel-info-ctn > div.hotel-remark > div.price > p > strong'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.hotel-info-ctn > div.hotel-remark > div.remark > div > div > span', attr='class', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.hotel-info-ctn > div.hotel-remark > div.remark > div > div > a', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_TAG, css_selector='div.hotel-info-ctn > div.hotel-info-main > p.hotel-tags', attr='innerHTML', filter_func=get_shop_tag, pause_time=3),
)

def get_shop_room_all(self, _str):
    with open('/home/wjl/test.txt','w+') as f:
        f.write(_str)
    return ''

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-right > div.hotel-appraise > div.hotel-scope > span'),
    Field(fieldname=FieldName.SHOP_PHONE, css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-left > div.main-detail-left-top.clearfix > div.hotel-detail-info > div > div.call-info > div > span.call-number'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='#poi-detail > div.container > div.base-info > div.main-detail.clearfix > div.main-detail-left > div.main-detail-left-top.clearfix > div.hotel-detail-price > div.hotel-address-box.clearfix > span.hotel-address'),
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#deal', attr='innerHTML', filter_func=get_shop_room_all),
)

page_shop_1 = Page(name='大众点评酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#poi-list > div.content-wrap > div > div.list-wrapper > div.content > ul > li', item_end=1), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='大众点评酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.hotel-info-ctn > div.hotel-info-main > h2 > a.hotel-name-link'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class DianpingHotelSpider(TravelDriver):

    def page_shop_2_func(self):
        pass

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1, page_func=self.page_shop_2_func)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://www.dianping.com/')
        time.sleep(2)
        self.fast_click_first_item_page_by_partial_link_text(link_text='酒店')
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#J_h-s-destn-wrap > input', text=self.data_region)
        time.sleep(2)
        self.fast_enter_page_by_css_selector(css_selector='#J_h-s-destn-wrap > input')
        self.vertical_scroll_to()#滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='下一页', func=self.get_shop_info, is_next=False)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()

