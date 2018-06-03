# -*- coding:utf-8 -*-

from spider.fliggyspotspider import FliggySpotSpider
import sys
from spider.driver.spider.base.travel.fields import *
from spider.driver.spider.base.travel.params import *

fields_shop1 = [
    Field(name=FieldName.SHOP_NAME,
          css_selector='div.item-info > div.item-text-container > div.item-text.item-title.line-count-1 > span'),
    Field(name=FieldName.SHOP_URL, attr='href'),
    Field(name=FieldName.SHOP_IMG,
          css_selector='div.item-image-container > img',
          attr='src'),
    Field(name=FieldName.SHOP_PRICE,
          css_selector='div.item-info > div.price-container > div.rpi-price.price > span:nth-child(2)'),
    Field(name=FieldName.SHOP_RATE,
          css_selector='div.item-info > div.item-text-container > div.item-sub-text.item-desc3.line-count-1',
          regex='[^A\d]*'),
    Field(name=FieldName.SHOP_TITLE,
          css_selector='div.item-info > div.item-text-container > div.item-sub-text.item-desc.line-count-1 > span'),
    Field(name=FieldName.SHOP_VOLUME,
          css_selector='div.item-info > div.price-container > div.price-desc',
          regex='\|.*$'),
    Field(name=FieldName.SHOP_COMMENT_NUM,
          css_selector='div.item-info > div.price-container > div.price-desc',
          regex='^[^\|]*|')
]

field_shop2 = [
    Field(name=FieldName.SHOP_ADDRESS,
          css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(4) > div > span'),
    Field(name=FieldName.SHOP_DETAIL_URL,
          css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(3) > div:nth-child(1)',
          attr='href',regex='[/]*(.+)',repl='https://\1'),
    Field(name=FieldName.COMMENT_URL,
          css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(3) > div:nth-child(2)',
          attr='href')
]

field_shop3 = [
    Field(name=FieldName.SHOP_TIME,
          css_selector='body > div > div > div:nth-child(1) > div > div:nth-child(2) > span:nth-child(1)'),
    Field(name=FieldName.SHOP_INTRO,
          css_selector='body > div > div > div:nth-child(2) > div > div:nth-child(2) > span')
]

field_comment1 = [
    Field(name=FieldName.COMMENT_USER_NAME,
          css_selector='div.rate-info > div.avatar-info > div.user-nick'),
    Field(name=FieldName.COMMENT_USER_IMG,
          css_selector='div.rate-info > div.avatar-bg > img',
          attr='src'),
    Field(name=FieldName.COMMENT_TIME,
          css_selector='div.rate-info > div.avatar-info > div.info > div.time'),
    Field(name=FieldName.COMMENT_RATE_TAG,
          css_selector='div.rate-tags',timeout=1),
    Field(name=FieldName.COMMENT_CONTENT,
          css_selector='div.rate-content-container',regex='^(.+)收起$',repl='\1'),
    ListField(name=FieldName.COMMENT_PIC_LIST,
          list_css_selector='div.rate-images > div',item_css_selector='div',attr='data-src',timeout=1)
]

params_dict = {
    ParamType.SHOP_INFO_1 : Params_list(type=ParamType.SHOP_INFO_1,
      list_css_selector='#app > div > div.search-result-ctn > div > div > div > div:nth-child(7) > div > ul > div',
      item_css_selector='a',field_list=fields_shop1),
    ParamType.SHOP_INFO_2 : Params(type=ParamType.SHOP_INFO_2,field_list=field_shop2),
    ParamType.SHOP_INFO_3 : Params(type=ParamType.SHOP_INFO_3,field_list=field_shop3),
    ParamType.COMMENT_INFO_1 : Params_list(type=ParamType.COMMENT_INFO_1,
      list_css_selector='#app > div > div.poi-rate-container > div',field_list=field_comment1)
}

if __name__ == '__main__':
    spider = FliggySpotSpider(isheadless=True,ismobile=True,params_dict=params_dict,
                                id=sys.argv[1],
                                data_website=sys.argv[2],
                                data_region=sys.argv[3],
                                data_source=sys.argv[4])
    spider.run_spider()