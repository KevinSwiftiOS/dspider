# -*- coding:utf-8 -*-

from spider.lvmamaspotspider import LvmamaSpotSpider
import sys
from spider.driver.spider.base.travel.fields import *
from spider.driver.spider.base.travel.params import *

fields_shop1 = [
    Field(name=FieldName.SHOP_NAME,css_selector='div.ml-pro-info > p'),
    Field(name=FieldName.SHOP_URL,attr='href'),
    Field(name=FieldName.SHOP_ID,attr='href',regex='[^\d]*'),
    Field(name=FieldName.SHOP_IMG,css_selector='div.ml-pro-img > img',attr='src'),
    Field(name=FieldName.SHOP_PRICE,css_selector='div.ml-pro-info > div.ml-pro-price > span.price'),
    Field(name=FieldName.SHOP_ACTIVE_STATUS,css_selector='div.ml-pro-info > div.ml-pro-price'),
    Field(name=FieldName.SHOP_RATE,css_selector='div.ml-pro-info > div.orderNum.adress',
          regex='^[^\d\w.]*([\d\w]*)[^\d\w.]+[\d\w.]*$',
          repl='\1'),
    Field(name=FieldName.SHOP_DISTANCE,css_selector='div.ml-pro-info > div.orderNum.adress',
          regex='^[^\d\w.]*[\d\w]*[^\d\w.]+([\d\w.]*)$',
          repl='\1'),
    Field(name=FieldName.COMMENT_URL, attr='href',regex='^(.*)$',repl='\1/comment'),
]

fields_shop2 = [
    Field(name=FieldName.SHOP_ADDRESS,
          css_selector='#tpl > div.detail-page > div.viewspot-infos.borderRedius > div.addressWrap > p'),
    Field(name=FieldName.SHOP_COMMENT_NUM,
          css_selector='#tpl > div.detail-page > div.viewspot-infos.borderRedius > div.intro-main > div.right > span'),
    Field(name=FieldName.SHOP_STATISFACTION_PERCENT,
          css_selector='#tpl > div.detail-page > div.viewspot-infos.borderRedius > div.intro-main > div.right > p'),
    Field(name=FieldName.SHOP_TIME,
          css_selector='#tpl > div.detail-page > div.viewspot-details.hasFreeTour > div > section > article.tabChange.order-ticket.comment.pdb0.pdt66 > div.notice.detail-notice.JQXZ.hideTitles > div.detailSpots.detailShow > div:nth-child(1)',offset=100),
    Field(name=FieldName.SHOP_STATISTICS, css_selector='#tpl > div.detail-page > div.viewspot-details > div > section > article.tabChange.order-ticket.comment.pdb0.pdt66 > div.comment-list > div.firstScores',offset=100)
]

fields_comment1 = [
    Field(name=FieldName.COMMENT_USER_NAME,css_selector='div.top > div.tourist > div'),
    Field(name=FieldName.COMMENT_TIME,css_selector='div.comment-bottom > p'),
    Field(name=FieldName.COMMENT_CONTENT,css_selector='div.comment-txt'),
    ListField(name=FieldName.COMMENT_PIC_LIST,list_css_selector='div.comment-pic',
              item_css_selector='img',attr='src'),
    Field(name=FieldName.COMMENT_LIKE_NUM,css_selector='div.comment-bottom > div.usefulCount.ticket'),
    Field(name=FieldName.COMMENT_REPLY_NUM,css_selector='div.comment-bottom > div.chatReply'),
]

params_dict = {
    ParamType.SHOP_INFO_1 : Params_list(type=ParamType.SHOP_INFO_1,
    list_css_selector='article.masterplate-list > ul > li',
    item_css_selector='a',field_list=fields_shop1),
    ParamType.SHOP_INFO_2 : Params(type=ParamType.SHOP_INFO_2,field_list=fields_shop2),
    ParamType.COMMENT_INFO_1 : Params_list(type=ParamType.COMMENT_INFO_1,
    list_css_selector='#view > div.comment > div.wrap2 > div',
    field_list=fields_comment1),
}

if __name__ == '__main__':
    spider = LvmamaSpotSpider(isheadless=True,ismobile=True,isvirtualdisplay=True,params_dict=params_dict,
                              id=sys.argv[1],
                              data_website=sys.argv[2],
                              data_region=sys.argv[3],
                              data_source=sys.argv[4])
    spider.run_spider()