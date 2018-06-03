# -*- coding:utf-8 -*-

import sys
from spider.elonghotelspider import ElongHotelSpider
from spider.driver.spider.base.travel.fields import *
from spider.driver.spider.base.travel.params import *

fields_list_shop1 = [
    Field(name=FieldName.SHOP_NAME,css_selector='div.h_info_text > div.h_info_base > p.h_info_b1 > a', attr='title'),
    Field(name=FieldName.SHOP_URL,css_selector='div.h_info_text > div.h_info_base > p.h_info_b1 > a',attr='href'),
    Field(name=FieldName.SHOP_ID,css_selector='div.h_info_text > div.h_info_base > p.h_info_b1 > a',attr='href',regex='[^\d]*'),
    Field(name=FieldName.SHOP_GRADE,css_selector='div.h_info_text > div.h_info_base > p.h_info_b1 > a > span > i:nth-child(1)'),
    Field(name=FieldName.SHOP_GRADE_TEXT,css_selector='div.h_info_text > div.h_info_base > p.h_info_b1 > a > span > i:nth-child(2)'),
    Field(name=FieldName.SHOP_ADDRESS,css_selector='div.h_info_text > div.h_info_base > p.h_info_b2 > a'),
    Field(name=FieldName.SHOP_ACTIVE_STATUS,css_selector='div.h_info_text > div.h_info_base > div.hotel_inf_sale > p'),
    Field(name=FieldName.SHOP_COMMENT_NUM,css_selector='div.h_info_text > div.h_info_comt > a > span:nth-child(2) > b'),
    Field(name=FieldName.SHOP_PRICE,css_selector='div.h_info_text > div.h_info_pri > p:nth-child(1) > a'),
    Field(name=FieldName.SHOP_IMG,css_selector='div.h_info_pic > a > img',attr='src'),
    Field(name=FieldName.SHOP_RATE,css_selector='div.h_info_text > div.h_info_base > p.h_info_b1 > b',attr='class',regex='[^\d]*'),
]

fields_shop2 = [
    Field(name=FieldName.SHOP_PHONE,css_selector='#hotelContent > div > dl:nth-child(1)'),
    Field(name=FieldName.SHOP_TIME,css_selector='#hotelContent > div > dl:nth-child(2)'),
    Field(name=FieldName.SHOP_STATISTICS,css_selector='#review > div.cmt_hd > div.cmt_tp'),
]

fields_list_comment1 = [
    Field(name=FieldName.COMMENT_USER_NAME,css_selector='div.cmt_userinfo > div > p.cmt_un'),
    Field(name=FieldName.COMMENT_GRADE,css_selector='div.cmt_info_mn > div.cmt_if_hd > div.if_hd > b'),
    Field(name=FieldName.COMMENT_TYPE,css_selector='div.cmt_userinfo > div > p.cmt_lvtxt'),
    Field(name=FieldName.COMMENT_CONTENT,css_selector='div.cmt_info_mn > p'),
    Field(name=FieldName.COMMENT_ROOM,css_selector='div.cmt_info_mn > div.cmt_if_hd > div.if_hd > span.cmt_tag'),
    Field(name=FieldName.COMMENT_TIME,css_selector='div.cmt_info_mn > div.cmt_if_hd > div.if_hd_r > span.cmt_con_time'),
]

params_dict = {
    ParamType.SHOP_INFO_1 : Params_list(type=ParamType.SHOP_INFO_1,
    list_css_selector='#hotelContainer > div.h_list > div.h_item > div.h_info',field_list=fields_list_shop1),
    ParamType.SHOP_INFO_2 : Params(type=ParamType.SHOP_INFO_2,
    click_css_selector='div.h_info_text > div.h_info_pri > div > a',field_list=fields_shop2),
    ParamType.COMMENT_INFO_1 : Params_list(type=ParamType.COMMENT_INFO_1,
    list_css_selector='#review > ul > li',field_list=fields_list_comment1),
}

if __name__ == '__main__':
    spider = ElongHotelSpider(isvirtualdisplay=True,params_dict=params_dict,
                              id=sys.argv[1],
                              data_website=sys.argv[2],
                              data_region=sys.argv[3],
                              data_source=sys.argv[4])
    spider.run_spider()