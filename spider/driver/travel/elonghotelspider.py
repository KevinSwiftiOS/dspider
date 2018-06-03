# -*- coding:utf-8 -*-

from .traveldriver import *

class ElongHotelSpider(TravelDriver):

    def get_shop_info_list(self):
        self.fast_get_page(url='http://hotel.elong.com/')
        self.until_send_text_by_css_selector(css_selector='#domesticDiv > div > dl:nth-child(1) > dd > input', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#domesticDiv > div > dl:nth-child(1) > dd > input')
        time.sleep(1000)

    def run_spider(self):
        try:
            self.get_shop_info_list()
            # self.get_comment_info()
        except Exception as e:
            self.error_log(e=e)
