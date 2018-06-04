# -*- coding:utf-8 -*-
from spider.driver.travel.core.traveldriver import TravelDriver
from .consts import *
from .fields import *
import time

field_shop1 = [
    Field(name=FieldName.SHOP_URL,css_selector='a',attr='href'),
    Field(name=FieldName.SHOP_ID,css_selector='a',attr='href',regex=r'[^\d]*'),
    Field(name=FieldName.SHOP_NAME,css_selector='div.search_ticket_title > h2 > a'),
    Field(name=FieldName.SHOP_IMG,css_selector='a > img',attr='src'),
    Field(name=FieldName.SHOP_RATE,css_selector='div.search_ticket_title > h2 > span > span.rate'),
    Field(name=FieldName.SHOP_ADDRESS,css_selector='div.search_ticket_title > div.adress'),
    Field(name=FieldName.SHOP_TITLE,css_selector='div.search_ticket_title > div.exercise'),
    Field(name=FieldName.SHOP_GRADE,css_selector='div.search_ticket_assess > span.grades > em'),
    Field(name=FieldName.SHOP_COMMENT_NUM,css_selector='div.search_ticket_assess > span.grades',regex=r'^.*\((.*)\).*$',repl=r'\1'),
]

field_shop2 = [
    Field(name=FieldName.SHOP_TIME,css_selector='#media-wrapper > div.media-right > ul > li.time > span'),
    Field(name=FieldName.SHOP_PRICE,css_selector='#media-wrapper > div.media-price > div > span'),
    Field(name=FieldName.SHOP_ACTIVE_STATUS,css_selector='#media-wrapper > div.media-price',
          regex=r'^.+起([\d]+分钟前有人预订).+$',repl=r'\1'),
]

field_comment1 = [
    Field(name=FieldName.COMMENT_USER_NAME,css_selector='div > span',
          regex=r'^(.+)[\d]{4}-[\d]{2}-[\d]{2}[ ]+[\d]{2}:[\d]{2}$',repl=r'\1',timeout=5),
    Field(name=FieldName.COMMENT_GRADE,css_selector='h4 > span',timeout=5),
    Field(name=FieldName.COMMENT_TIME,css_selector='div > span',
          regex=r'^.+([\d]{4}-[\d]{2}-[\d]{2}[ ]+[\d]{2}:[\d]{2})$',repl=r'\1',timeout=5),
    Field(name=FieldName.COMMENT_CONTENT,css_selector='p',timeout=5),
]

SHOP_INFO_1 = ParamsList(type=ParamType.SHOP_INFO_1,
                         list_css_selector='#searchResultContainer > div > div',
                         field_list=field_shop1)
SHOP_INFO_2 = Params(type=ParamType.SHOP_INFO_2,
                     click_css_selector='div.search_ticket_assess > span.comment > a',
                     field_list=field_shop2)
COMMENT_INFO_1 = ParamsList(type=ParamType.COMMENT_INFO_1,
                            list_css_selector='#J-comments > ul > li', field_list=field_comment1)

class XiechengSpotSpider(TravelDriver):
    def get_comment_info2(self,shop_url):
        """

        :param shop_url:
        :return:
        """
        shop_data_current = {}
        for shop_data in self.get_current_data_list_from_db(self.shops_collections):
            if shop_data.get(FieldName.SHOP_URL) == shop_url:
                shop_data_current = shop_data
        try:
            self.vertical_scroll_by(offset=20000)
            self.scroll_into_view(
                ele=self.until_presence_of_element_located_by_css_selector(css_selector=COMMENT_INFO_1.list_css_selector))
            while (True):
                external_key = {
                    FieldName.SHOP_NAME : shop_data_current.get(FieldName.SHOP_NAME),
                }
                self.get_spider_data_list(params_list=COMMENT_INFO_1,
                                          is_save=True,external_key=external_key,target=self.comments_collections)
                try:
                    self.until_click_by_css_selector(css_selector='#J-Pages > a.c_down')
                    time.sleep(3)
                except Exception as e:
                    self.info_log(name='评论翻页', data=e)
                    break
        except Exception as e:
            self.error_log(e=e)

    def get_comment_info(self):
        """

        :return:
        """
        try:
            for each in self.until_presence_of_all_elements_located_by_css_selector(css_selector=SHOP_INFO_1.list_css_selector):
                ele = self.until_presence_of_element_located_by_css_selector(ele=each,css_selector=SHOP_INFO_2.click_css_selector)
                shop_url = ele.get_attribute('href')
                self.run_tab_task(click_ele=ele,func=self.get_comment_info2,shop_url=shop_url)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info(self):
        """

        :return:
        """
        shop_data_list = self.get_spider_data_list(params_list=SHOP_INFO_1)
        shop_data_list = self.add_spider_data_to_data_list(data_list=shop_data_list,params=SHOP_INFO_2)
        for shop_data in shop_data_list:
            key = {
                FieldName.SHOP_NAME : shop_data.get(FieldName.SHOP_NAME),
            }
            self.save_data_to_db(target=self.shops_collections,key=key,data=shop_data)

    def run_spider(self):
        """

        :return:
        """
        self.driver.get('http://www.ctrip.com')
        self.until_click_by_css_selector(css_selector='#nav_ticket')
        self.until_presence_of_element_located_by_css_selector(css_selector='#mainInput').clear()
        self.info_log(data='搜索%s'%(self.data_region))
        self.until_send_text_by_css_selector(css_selector='#mainInput',text='%s'%(self.data_region))
        self.until_click_by_css_selector(css_selector='#base_bd > div:nth-child(1) > div > div.main_right > div.search_wrap.basefix > a')
        while(True):
            self.get_shop_info()
            # self.get_comment_info()
            try:
                self.vertical_scroll_by(offset=5000)
                self.until_presence_of_element_located_by_css_selector(
                    css_selector='#searchResultContainer > div.pkg_page.basefix > a.down.down_nocurrent',timeout=4)
                break
            except Exception:
                self.info_log(data='点击下一页')
                self.vertical_scroll_by(offset=5000)
                try:
                    self.until_click_by_css_selector(css_selector='#searchResultContainer > div.pkg_page.basefix > a.down')
                except Exception as e:
                    self.error_log(e=e)