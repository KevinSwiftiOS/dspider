# -*- coding:utf-8 -*-
from spider.driver.base.driver import Driver
from spider.driver.base.mysql import Mysql
import time
from pyquery import PyQuery
from spider.driver.base.field import Field,FieldName,Fieldlist,FieldType
from spider.driver.base.page import Page
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb

fl_weixin1 = Fieldlist(
    Field(fieldname='', css_selector='div.weui_msg_card_hd'),
    Field(fieldname='title', css_selector='div.weui_msg_card_bd > div > div > h4', regex=r'[^\u4e00-\u9fa5]*')
)

# fl_weixin2 = Fieldlist(
#     Field(fieldname=FieldName.WEIXIN_1_CREATED_TIME, css_selector='div.weui_msg_card_hd'),
#     Field(fieldname=FieldName.WEIXIN_1_TITLE, css_selector='div.weui_msg_card_bd > div > div > h4', regex=r'[^\u4e00-\u9fa5]*')
# )

page_weixin_1 = Page(name='微信文章列表页面', fieldlist=fl_weixin1, listcssselector=ListCssSelector(list_css_selector='#history > div.weui_msg_card'))

# page_weixin_2 = Page(name='微信文章列表页面', fieldlist=fl_weixin2, listcssselector=ListCssSelector(list_css_selector='#history > div.weui_msg_card'))

class WeixinSpider(Driver):

    def __init__(self,isheadless=False,ismobile=False,isvirtualdisplay=False,spider_id='',name=''):
        Driver.__init__(self, log_file_name=spider_id, ismobile=ismobile, isvirtualdisplay=isvirtualdisplay,
                        isheadless=isheadless)
        self.name = name
        self.debug_log(name=name)

    def run_spider(self):
        for public in Mysql().query_data(table='weixin_public', field='public_name')[:1]:
            self.fast_get_page(url='http://weixin.sogou.com/')
            self.until_send_text_by_css_selector(css_selector='#query', text=public[0])
            time.sleep(3)
            self.fast_enter_page_by_css_selector(css_selector='#query')
            time.sleep(2)
            self.fast_click_same_page_by_css_selector(click_css_selector='#scroll-header > form > div > input.swz2')
            for item in self.until_presence_of_all_elements_located_by_css_selector(css_selector='#main > div.news-box > ul > li'):
                public_name = self.until_presence_of_element_located_by_css_selector(ele=item, css_selector='div > div.txt-box > p.tit > a').text
                self.fast_click_page_by_css_selector(ele=item, click_css_selector='div > div.txt-box > p.tit > a')
                self.driver.switch_to.window(self.driver.window_handles[-1])
                shop_data_list = self.from_page_get_data_list(page=page_weixin_1)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])