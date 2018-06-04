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
    Field(fieldname=FieldName.SHOP_NAME,css_selector='li.hotel_item_name > h2 > a',regex=r'^[\d]*(.*)$',repl=r'\1'),
    Field(fieldname=FieldName.SHOP_URL,css_selector='li.hotel_item_name > h2 > a',attr='href',regex=r'^([^\?]*)?.*$',repl=r'\1'),
    Field(fieldname=FieldName.SHOP_ID, css_selector='li.hotel_item_name > h2 > a', attr='href',regex=r'^[^\?\d]*([\d]*).html?.*$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='li.pic_medal > div > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='li.hotel_item_name > p.hotel_item_htladdress'),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.hotel_value'),
    Field(fieldname=FieldName.SHOP_STATISFACTION_PERCENT,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.total_judgement_score > span'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='li.hotel_item_name > span', attr='innerHTML',regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_ACTIVE_STATUS, css_selector='li.hotel_item_name > p.hotel_item_last_book'),
    Field(fieldname=FieldName.SHOP_PRICE,css_selector='span.J_price_lowList'),
    Field(fieldname=FieldName.SHOP_CATEGORY_NAME, css_selector='li.hotel_item_name > p.medal_list > span'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.hotel_judgement > span'),
    Field(fieldname=FieldName.SHOP_GRADE_TEXT,css_selector='li.hotel_item_judge.no_comment > div.hotelitem_judge_box > a > span.recommend'),
)


def get_recommend_all_room_dict(self, str):
    p = PyQuery(str)
    item_list = []
    for each in p('tr').items():
        if each.attr('class'):
            item_list.append(each)
    recommend_all_room_dict = {}
    all_room_list = []
    recommend_room = {}
    room_detail = {}
    room_info_list = []
    for item in item_list[::-1]:
        if item.attr('class') == 'clicked hidden':
            if room_detail and room_info_list:
                all_room_list.append({'room_detail': room_detail, 'room_info_list': room_info_list})
            room_detail = {}  # 重置
            room_info_list = []  # 重置
            room_detail.setdefault('房型', (lambda x: x.replace('\n', '').strip() if x else x)(item('div.hrd-title').text()))
            for i in item('ul.hrd-info-base-list>li').items():
                kv = i.text().split(':')
                if len(kv) == 1:
                    kv = i.text().split('：')
                if len(kv) == 1:
                    kv.append(kv[0])
                room_detail.setdefault(kv[0].strip(), kv[1].strip())
            for i in item('ul.hrd-allfac-list>li').items():
                kv = i.text().split(':')
                if len(kv) == 1:
                    kv = i.text().split('：')
                if len(kv) == 1:
                    kv.append(kv[0])
                room_detail.setdefault(kv[0].strip(), kv[1].strip())
        elif item.attr('class') == 'hidden':
            pass
        else:
            room_info = {}
            room_info.setdefault('满意度', (lambda x:x.replace('\n', '').strip() if x else x)(item('td.child_name').text()))
            room_info.setdefault('床型', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col3').text()))
            room_info.setdefault('早餐', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.text_green.col4').text()))
            room_info.setdefault('宽带', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col5').text()))
            room_info.setdefault('入住人数', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col_person>span').attr('title')))
            room_info.setdefault('政策', (lambda x: x.replace('\n', '').strip() if x else x)(item('td.col_policy').text()))
            room_info.setdefault('房价', (lambda x: x.replace('\n', '').strip() if x else x)(item('td>div>span.base_price').text()))
            room_info_list.append(room_info)
    if room_detail and room_info_list:
        recommend_room = {'room_detail': room_detail, 'room_info_list': room_info_list}
    recommend_all_room_dict.setdefault('recommend_room', recommend_room)
    recommend_all_room_dict.setdefault('all_room', all_room_list)
    return json.dumps(recommend_all_room_dict, ensure_ascii=False)

def get_favourable_room(self, str):
    favourable = {}
    room = {}
    p = PyQuery(str)
    tr1 = p('tr.group_hotel.J_GroupRoom')
    room.setdefault('房型', (lambda x: x.strip() if x else x)(tr1('td.room_type').text()))
    room.setdefault('活动', (lambda x: x.strip() if x else x)(tr1('td.child_name').text()))
    room.setdefault('床型', tr1('td:nth-child(3)').text())
    room.setdefault('早餐', tr1('td:nth-child(4)').text())
    room.setdefault('宽带', tr1('td:nth-child(5)').text())
    room.setdefault('政策', tr1('td:nth-child(6)').text())
    room.setdefault('房价', tr1('td:nth-child(7)').text())
    favourable.setdefault('优惠房', room)
    tr2 = p('tr.rooms_sales.J_MeetingRooms')
    favourable.setdefault((lambda x: x.replace('\n', ',').strip() if x else '优惠')(tr2('td.room_type').text()),
                          (lambda x: x.replace('\n', '').strip() if x else x)(tr2('td:nth-child(2)').text()))
    tr3 = p('tr.hotel_spot.J_ShxDpSpot')
    package_list = []
    for i in tr3('td.room_type').items('div'):
        package_list.append({(lambda x: x if x else '房型')(tr3('p').text()): (
            lambda x: x.replace('\n', ',').strip() if x else x)(tr3('span').text())})
    package_list.append({(lambda x: x.replace('\n', ',').strip() if x else '套餐价')(
        tr3('td:nth-child(3)>p:nth-child(1)').text()): (lambda x: x.replace('\n', ',').strip() if x else x)(
        tr3('td:nth-child(3)>p:nth-child(2)').text())})
    favourable.setdefault((lambda x: x.replace('\n', ',').strip() if x else '优惠套餐')(tr3('td:nth-child(1)').text()),
                          package_list)
    return json.dumps(favourable, ensure_ascii=False)

def get_hotel_intro(self, str):
    p = PyQuery(str)
    hotel_intro_dict = {}
    # 酒店介绍
    intro = {}
    label = []
    for i in p('div.special_label').items('i'):
        label.append(i.text())
    intro.setdefault('label', label)
    info = []
    info_count = 0
    for i in p('div.special_info>ul').items('li'):
        info_count += 1
        info.append({(lambda x: re.sub(r'[^\u4e00-\u9fa5]', '', x) if x else '%s' % info_count)(i('span').text()): (
            lambda x: x if x else x)(i.text())})
    intro.setdefault('info', info)
    intro.setdefault('other',
                     (lambda x: x.replace('\n', ',').strip() if x else x)(p('div.htl_room_txt.text_3l').text()))
    hotel_intro_dict.setdefault('酒店介绍', intro)
    # 酒店设施
    facilities = {}
    for i in p('#J_htl_facilities > table > tbody').items('tr'):
        item = (lambda x: x if x else '')(i.text()).split('\n')
        facilities.setdefault(item[0], (lambda x: x[1:] if len(x) >= 2 else [''])(item))
    hotel_intro_dict.setdefault('酒店设施', facilities)
    # policy
    policy = {}
    for i in p('div.htl_info_table > table.detail_extracontent > tbody').items('tr'):
        item = (lambda x: x if x else '')(i.text()).split('\n')
        if '支付方式' in item[0]:
            item = item[:1]#初始化
            for j in i('div.card_cont_img').items('span'):
                p_pay = PyQuery(j.attr('data-params'))
                item.append(p_pay('div.jmp_bd').text().split('\'')[0])
            for j in i('span.detail_cardname').items():
                item.append(j.text().strip())
        policy.setdefault(item[0], (lambda x: x[1:] if len(x) >= 2 else [''])(item))
    hotel_intro_dict.setdefault('酒店政策', policy)
    return json.dumps(hotel_intro_dict, ensure_ascii=False)

def get_shop_statistics(self, str):
    p = PyQuery(str)
    statistics = {}
    # 点评
    dianping = []
    for i in p('div.comment_sumary_box>div.comment_total_score').items('span'):
        (lambda x: dianping.append(x.strip()) if x else '')(i.text())
    for i in p('div.comment_sumary_box>div.bar_score').items('p'):
        text = i.text()
        dianping.append({re.sub(r'[^\u4e00-\u9fa5]', '', text):re.sub(r'[^\d.]', '', text)})
    statistics.setdefault('点评', dianping)
    # 印象
    impression = []
    count = 0
    for i in p('div.user_impress').items('a'):
        count += 1
        text = i.text()
        impression.append({(lambda x: x if x else '第一个%s' % count)(re.sub(r'[^\u4e00-\u9fa5]', '', text)): re.sub(
            r'[^\d]', '', text)})
    statistics.setdefault('印象', impression)
    return json.dumps(statistics, ensure_ascii=False)

def get_around_facilities(self, str):
    str = re.sub(r'^.*<h2 class=\"detail_title\">周边设施</h2>(.*)$', r'\1', str)
    p = PyQuery(str)
    around = {}
    for i in p('div.htl_info_table > table > tbody').items('tr'):
        item = (lambda x: x if x else '')(i.text()).split('\n')
        if len(item) >= 2:
            around.setdefault(item[0], (lambda x: x[1:] if len(x) >= 2 else [''])(item))
    return json.dumps(around, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL,css_selector='#hotelRoomBox', attr='innerHTML', filter_func=get_recommend_all_room_dict,offset=6,try_times=20,pause_time=5),
    Field(fieldname=FieldName.SHOP_ROOM_FAVOURABLE,css_selector='#divDetailMain > div.htl_room_table',attr='innerHTML', filter_func=get_favourable_room),
    Field(fieldname=FieldName.SHOP_INTRO, css_selector='#hotel_info_comment > div',attr='innerHTML', filter_func=get_hotel_intro),
    Field(fieldname=FieldName.SHOP_PHONE, css_selector='#J_realContact', attr='data-real', regex='^([^<]*).*$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#commentList > div.detail_cmt_box',attr='innerHTML',filter_func=get_shop_statistics),
    Field(fieldname=FieldName.SHOP_AROUND_FACILITIES, css_selector='#hotel_info_comment > div', attr='innerHTML',filter_func=get_around_facilities),
)

page_shop_1 = Page(name='携程酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#hotel_list > div.hotel_new_list', item_css_selector='ul.hotel_item'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='携程酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='li.hotel_price_icon > div.action_info > p > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=True)

class XiechengHotelSpider(TravelDriver):

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://hotels.ctrip.com/')
        time.sleep(1)
        self.until_presence_of_element_located_by_css_selector(css_selector="#txtCity").clear()
        self.until_send_text_by_css_selector(css_selector="#txtCity", text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#txtCity')
        self.fast_click_same_page_by_css_selector(click_css_selector='#btnSearch')
        self.until_click_no_next_page_by_css_selector(func=self.get_shop_info, css_selector='#downHerf.c_down')

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=e)