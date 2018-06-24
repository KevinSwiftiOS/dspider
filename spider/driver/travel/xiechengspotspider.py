# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
import re
import time
import json
from pyquery import PyQuery

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div.search_ticket_title > h2 > a'),
    Field(fieldname=FieldName.SHOP_URL,css_selector='div.search_ticket_title > h2 > a',attr='href'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.search_ticket_title > div.adress'),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div.search_ticket_assess > span.grades > em'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div.search_ticket_assess > span.grades', regex=r'^[^\(]*\(([\d]+)[^\)\d]*\)$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div.search_ticket_title > div.exercise'),
)

def get_shop_service(self, _str):
    p = PyQuery(_str)
    service_list = []
    for i in p('span').items():
        service_list.append(i.text().strip())
    return json.dumps(service_list, ensure_ascii=False)

def get_shop_ticket(self, _str):
    with open('/home/mininet/test.txt','w+') as f:
        f.write(_str)
    return ''

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.spot-price > div > span', pause_time=3, is_focus=True),
    Field(fieldname=FieldName.SHOP_TIME, css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.brief-right > ul > li.time > span', is_focus=True),
    Field(fieldname=FieldName.SHOP_SERVICE,css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.brief-right > ul > li.promise',attr='innerHTML', filter_func=get_shop_service, is_focus=True),
    Field(fieldname=FieldName.SHOP_TICKET, css_selector='#booking-wrapper',attr='innerHTML', filter_func=get_shop_ticket, is_focus=True),
    # Field(fieldname=FieldName.SHOP_PHONE, css_selector='#J_realContact', attr='data-real', regex='^([^<]*).*$', repl=r'\1', is_focus=True),
    # Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#commentList > div.detail_cmt_box',attr='innerHTML',filter_func=get_shop_statistics, is_focus=True),
    # Field(fieldname=FieldName.SHOP_AROUND_FACILITIES, css_selector='#hotel_info_comment > div', attr='innerHTML',filter_func=get_around_facilities, is_focus=True),
)

page_shop_1 = Page(name='携程景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#searchResultContainer > div > div', item_end=1), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='携程景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.search_ticket_title > h2 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=True)

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.user_info.J_ctrip_pop > p.name'),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div.comment_main > div.comment_txt > div.comment_bar > p > span', regex=r'[^\d-]*'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#J_htl_info > div.name > h2.cn_n', is_isolated=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div.comment_main > div.comment_txt > div.J_commentDetail'),
    Field(fieldname=FieldName.COMMENT_USER_IMG, css_selector='div.user_info.J_ctrip_pop > p.head > span > img', attr='src'),
    Field(fieldname=FieldName.COMMENT_USER_CHECK_IN, css_selector='div.comment_main > p > span.date'),
    Field(fieldname=FieldName.COMMENT_USER_ROOM, css_selector='div.comment_main > p > a'),
    Field(fieldname=FieldName.COMMENT_TYPE, css_selector='div.comment_main > p > span.type'),
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='div.comment_main > p > span.score', regex=r'[^\d.]*'),
    Field(fieldname=FieldName.COMMENT_SCORE_TEXT, css_selector='div.comment_main > p > span.small_c', attr='data-value'),
    Field(fieldname=FieldName.COMMENT_USER_NUM, css_selector='div.user_info.J_ctrip_pop > p.num'),
    Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div.comment_txt > div.comment_pic', item_css_selector='div.pic > img', attr='src', timeout=0),
    Field(fieldname=FieldName.COMMENT_REPLAY, css_selector='div.comment_main > div.htl_reply > p.text.text_other'),
)

page_comment_1 = Page(name='携程酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#divCtripComment > div.comment_detail_list > div.comment_block'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class XiechengSpotSpider(TravelDriver):

    def get_shop_comment(self):
        try:
            self.until_scroll_to_center_select_by_visible_text_by_css_selector(
                css_selector='#divCtripComment > div.comment_box_bar_new.clearfix > div.bar_right > select.select_sort',
                text='入住时间排序')
        except Exception:
            self.error_log(e='点击入住时间排序出错!!!')
        time.sleep(5)  # 为了缓冲页面排序的变化
        field_shop_name = None
        for field in page_comment_1.fieldlist:
            if field.fieldname == FieldName.SHOP_NAME:
                field_shop_name = field
                break
        if field_shop_name:
            shop_name = self.until_presence_of_element_located_by_css_selector(css_selector=field_shop_name.css_selector, timeout=field_shop_name.timeout).text
            time_list = [i.get(FieldName.COMMENT_TIME) for i in page_comment_1.mongodb.get_collection().find(self.merge_dict(self.data_key, {FieldName.SHOP_NAME:shop_name}), {FieldName.COMMENT_TIME:1,FieldName.ID_:0})]
            time_list.sort(reverse=True)
            newest_time = (lambda tl:tl[0] if len(tl) >=1 else '')(time_list)#最新的时间
            self.debug_log(data='数据库评论最新时间:%s'%newest_time)
            try:
                self.until_click_no_next_page_by_css_selector(css_selector='#divCtripComment > div.c_page_box > div > a.c_down', pause_time=3, func=self.from_page_get_comment_data_list, page=page_comment_1, newest_time=newest_time)
            except Exception:
                pass
        else:
            self.error_log(e='%s字段不存在!!!'%FieldName.SHOP_NAME)
            raise ValueError

    def shop_page_func(self):
        for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='展开', timeout=1):
            self.scroll_to_center(ele=i)
            i.click()

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list, page_func=self.shop_page_func)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://piao.ctrip.com/', is_scroll_to_bottom=False, max_time_to_wait=30,min_time_to_wait=25, is_max=True)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector="#mainInput", text=self.data_region)
        time.sleep(1)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector="#mainInput")
        self.until_click_no_next_page_by_css_selector(css_selector='#searchResultContainer > div.pkg_page.basefix > a.down', stop_css_selector='#searchResultContainer > div.pkg_page.basefix > a.down.down_nocurrent', func=self.get_shop_info, is_next=False)
        time.sleep(1000)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=e)