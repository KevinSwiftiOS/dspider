# -*- coding:utf-8 -*-

from spider.dianpingspotspider import DianpingSpotSpider
import sys
from spider.driver.spider.base.travel.fields import *
from spider.driver.spider.base.travel.params import *

fields_shop1 = [
    Field(name=FieldName.SHOP_NAME,css_selector='div.item-content > div.item-title > h3'),
    Field(name=FieldName.SHOP_URL,attr='href',regex='^([^\?]+)\?.*$',repl='\1'),
    Field(name=FieldName.SHOP_ID,attr='href',regex='^[^\?\d]+([\d]+)\?.*$',repl='\1'),
    Field(name=FieldName.SHOP_IMG,css_selector='div.item-pic',attr='style',regex='^[^\(]+\((.*)\).*$',repl='\1'),
    Field(name=FieldName.SHOP_PRICE,css_selector='div.item-content > div.item-comment',regex='^[^￥]*￥([\d]*).*$',repl='\1'),
    Field(name=FieldName.SHOP_COMMENT_NUM,css_selector='div.item-content > div.item-comment',regex='^([\d]*)条.*$',repl='\1'),
    Field(name=FieldName.SHOP_TITLE,css_selector='div.item-content > div.item-info > div.item-info-left'),
    Field(name=FieldName.SHOP_GRADE,css_selector='div.item-content > div.item-comment > span',attr='class'),
    Field(name=FieldName.SHOP_DISTANCE,css_selector='div.item-content > div.item-info',regex='^[^\d]*([\d].*)$',repl='\1'),
]

fields_shop2 = [
    Field(name=FieldName.SHOP_ADDRESS,css_selector='#basic-info > div.expand-info.address'),
    Field(name=FieldName.SHOP_PHONE,css_selector='#basic-info > p'),
    Field(name=FieldName.SHOP_TIME,css_selector='#basic-info > div.other.J-other > p:nth-child(1) > span.item'),
    Field(name=FieldName.SHOP_INTRO,css_selector='#basic-info > div.other.J-other > p:nth-child(5)'),
]

fields_comment1 = [
    Field(name=FieldName.COMMENT_USER_NAME,
          css_selector='div > div.dper-info > a'),
    Field(name=FieldName.COMMENT_USER_URL,
          css_selector='div > div.dper-info > a',attr='href'),
    Field(name=FieldName.COMMENT_USER_IMG,css_selector='a > img',attr='src'),
    Field(name=FieldName.COMMENT_TIME,css_selector='div > div.misc-info.clearfix > span.time'),
    Field(name=FieldName.COMMENT_GRADE,css_selector='div > div.review-rank > span',attr='class',
          regex='^[^\d]*([\d]+)$',repl='\1'),
    Field(name=FieldName.COMMENT_CONTENT,css_selector='div > div.review-words',regex='^(.*)收起评论$',repl='\1'),
    ListField(name=FieldName.COMMENT_PIC_LIST,
              list_css_selector='div > div.review-pictures',item_css_selector='ul > li > a > img',attr='data-lazyload'),
    Field(name=FieldName.COMMENT_LIKE_NUM,css_selector='div.misc-info > span.actions > a.praise'),
    Field(name=FieldName.COMMENT_REPLY_NUM,css_selector='div.misc-info > span.actions > a.reply'),
    Field(name=FieldName.COMMENT_SCORE_TEXT,css_selector='div > div.review-rank > span.score'),
]

params_dict = {
    ParamType.SHOP_INFO_1 : Params_list(
        type=ParamType.SHOP_INFO_1,list_css_selector='#app > div > div.J_searchList > ul > li',
        item_css_selector='a',field_list=fields_shop1,
    ),
    ParamType.SHOP_INFO_2 : Params(
        type=ParamType.SHOP_INFO_2, field_list=fields_shop2,click_css_selector='#basic-info > a',
    ),
    ParamType.COMMENT_INFO_1 : Params_list(
        type=ParamType.COMMENT_INFO_1,
        list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li',
    ),
}

if __name__ == '__main__':
    spider = DianpingSpotSpider(isheadless=True,ismobile=False,params_dict=params_dict,
                                id=sys.argv[1],
                                data_website=sys.argv[2],
                                data_region=sys.argv[3],
                                data_source=sys.argv[4])
    spider.run_spider()