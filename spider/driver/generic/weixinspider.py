# -*- coding:utf-8 -*-
from spider.driver.base.driver import Driver
from spider.driver.base.mysql import Mysql
import time
from pyquery import PyQuery

class WeixinSpider(Driver):
    host = 'localhost'
    port = 3306

    def __init__(self,isheadless=False,ismobile=False,isvirtualdisplay=False,spider_id='',name=''):
        Driver.__init__(self, log_file_name=spider_id, ismobile=ismobile, isvirtualdisplay=isvirtualdisplay,
                        isheadless=isheadless)
        self.name = name
        self.debug_log(name=name)
        self.driver.set_page_load_timeout(1)

    def run_spider(self):
        for public in Mysql(host='10.1.17.25').query_data(table='weixin_public',field='public_name')[:1]:
            self.fast_get_page(url='http://weixin.sogou.com/')
            self.until_send_text_by_css_selector(css_selector='#query', text=public[0])
            time.sleep(3)
            self.fast_enter_page_by_css_selector(css_selector='#query')
            time.sleep(2)
            # self.fast_click_same_page_by_css_selector(click_css_selector='#scroll-header > form > div > input.swz2')
            print(public[0])
            # self.driver.find_element_by_css_selector('#query')
            # self.until_presence_of_element_located_by_css_selector(css_selector='#wap_0 > a',timeout=1).clear()
            # self.until_send_text_by_css_selector(css_selector='#wap_0 > a',text=public,timeout=1)
            # self.until_send_enter_by_css_selector(css_selector='#wap_0 > a',timeout=1)
            time.sleep(1000)

