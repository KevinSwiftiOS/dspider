# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from pyvirtualdisplay import Display
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
import inspect
from selenium.webdriver.common.keys import Keys
import time
from spider.driver.base.logger import get_logger
from .page import Page
from .field import Field,FieldName,FieldType,Fieldlist
from .mongodb import Mongodb
import re
import json
from selenium.common.exceptions import TimeoutException
import sys

class Driver(object):
    desktop_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
    mobile_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1'
    curr_user_agent = desktop_user_agent
    def __init__(self,log_file_name='00000000',ismobile=False,isvirtualdisplay=False,isheadless=False):
        """

        :param log_file_name:
        :param ismobile:
        :param isvirtualdisplay:
        :param isheadless:
        """
        self.logger = get_logger(log_file_name)
        self.ismobile = ismobile
        self.isvirtualdisplay = isvirtualdisplay
        self.isheadless = isheadless
        self.driver = self.get_driver()
        self.data_key = {}

    def __del__(self):
        """

        :return:
        """
        self.driver.quit()

    def get_driver(self):
        """

        :return:
        """
        options = webdriver.ChromeOptions()
        if self.ismobile:
            options.add_argument(
                'user-agent="%s"'%self.mobile_user_agent)
            self.curr_user_agent = self.mobile_user_agent
        else:
            options.add_argument(
            'user-agent="%s"'%self.desktop_user_agent)
            self.curr_user_agent = self.desktop_user_agent
        options.add_argument('lang=zh_CN.UTF-8')
        if self.isvirtualdisplay:
            self.logger.debug('virtualdisplay is running')
            display = Display(visible=0, size=(1440, 900))
            display.start()
        if self.isvirtualdisplay == False and self.isheadless == True:
            self.logger.debug('headless is running')
            options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_page_load_timeout(10)
        return driver


    def __get_current_function_name__(self):
        """
        4 表示当前运行的层数,是通用的
        :return:
        """
        return (inspect.stack()[4][3],inspect.stack()[4][2],inspect.stack()[3][3],inspect.stack()[3][2])

    def __get_running_func__(self):
        """

        :return:
        """
        return "%s.%s[%s].%s[%s]" % (self.__class__.__name__, self.__get_current_function_name__()[0],
                               self.__get_current_function_name__()[1],
                              self.__get_current_function_name__()[2],
                              self.__get_current_function_name__()[3])

    def error_log(self, name='', e='', istraceback=True):
        """

        :param name:
        :param e:
        :return:
        """
        if not e:
            e = ''
        traceback_e = ''
        if istraceback:
            traceback_e = traceback.format_exc()
        self.logger.error('@%s %s: %s\n%s' % (self.__get_running_func__(),name, traceback_e,e))

    def warning_log(self, name='', e=''):
        """"""

        if not e:
            e = ''
        self.logger.warning('@%s %s: %s' % (self.__get_running_func__(),name, e))

    def info_log(self, name='', data=''):
        """

        :param name:
        :param data:
        :return:
        """
        if not data:
            data = ''
        self.logger.info('@%s %s: %s' % (self.__get_running_func__(),name, data))

    def debug_log(self, name='', data=''):
        """

        :param name:
        :param data:
        :return:
        """
        if not data:
            data = ''
        self.logger.debug('@%s %s: %s' % (self.__get_running_func__(),name, data))

    def new_window(self, url:str):
        """

        :param url:
        :return:
        """
        self.driver.execute_script('window.open("{}");'.format(url))

    def ramdon_vertical_scroll_to(self, min_offset=1000, max_offset=5000):
        """
        随机下拉滚动加载
        :param min_offset:
        :param max_offset:
        :return:
        """
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight + %s)' % random.randint(min_offset,max_offset))

    def vertical_scroll_to(self, offset=10000):
        """
        下拉滚动加载
        :param offset:
        :return:
        """
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight + %s)' % offset)

    def vertical_scroll_by(self, offset=100):
        """

        :param offset:
        :return:
        """
        self.driver.execute_script('window.scrollBy(0,%s)'%offset)

    def scroll_into_view(self, ele:WebElement):
        """

        :param ele:
        :return:
        """
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def focus_on_element(self, ele:WebElement):
        """
        把元素滚动到页面中间
        :param ele:
        :return:
        """
        self.driver.execute_script("arguments[0].focus();", ele)

    def focus_on_element_by_css_selector(self, css_selector=''):
        """
        把元素滚动到页面中间
        :param css_selector:
        :return:
        """
        ele = self.until_presence_of_element_located_by_css_selector(css_selector=css_selector)
        self.driver.execute_script("arguments[0].focus();", ele)

    def focus_on_element_by_partial_link_text(self, link_text=''):
        """
        把元素滚动到页面中间
        :param link_text:
        :return:
        """
        ele = self.until_presence_of_element_located_by_partial_link_text(link_text=link_text)
        self.driver.execute_script("arguments[0].focus();", ele)

    def until_scroll_into_view_by_css_selector(self, ele=None, css_selector=''):
        """

        :param ele:WebElement
        :param css_selector:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def until_scroll_into_view_by_partial_link_text(self, ele=None, link_text=''):
        """

        :param ele:WebElement
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_partial_link_text(ele=ele, link_text=link_text)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def until_scroll_into_view_by_link_text(self, ele=None, link_text=''):
        """

        :param ele:
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", ele)

    def until_click_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """

        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为None')
            return None
        if not ele:
            ele = self.driver
        return WebDriverWait(driver=ele, timeout=timeout)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()

    def until_click_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """

        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        return WebDriverWait(driver=ele, timeout=timeout)\
            .until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))).click()

    def until_click_by_link_text(self, ele=None, timeout=10, link_text=''):
        """

        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        return WebDriverWait(driver=ele, timeout=timeout)\
            .until(EC.element_to_be_clickable((By.LINK_TEXT, link_text))).click()

    def move_to_element(self, ele=None, xoffset=0, yoffset=0):
        """

        :param ele:WebElement
        :param xoffset:
        :param yoffset:
        :return:
        """
        if not ele:
            self.error_log(e='ele不可以为空')
            return None
        ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=xoffset,yoffset=yoffset).perform()

    def move_to_element_by_css_selector(self, ele=None, css_selector='', xoffset=0, yoffset=0):
        """

        :param ele:WebElement
        :param xoffset:
        :param yoffset:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return None
        if not ele:
            ele = self.driver
        ele = self.until_presence_of_element_located_by_css_selector(ele=ele, css_selector=css_selector)
        ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=xoffset,yoffset=yoffset).perform()

    def until_move_to_element_by_css_selector(self, ele=None, css_selector='', timeout=10):
        """

        :param ele:WebElement
        :param css_selector:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为None')
            return None
        if not ele:
            ele = self.driver
        ActionChains(self.driver).move_to_element(
            self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout)).perform()

    def until_move_to_element_by_partial_link_text(self, ele=None, link_text='', timeout=10):
        """

        :param ele:WebElement
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        ActionChains(self.driver).move_to_element(
            self.until_presence_of_element_located_by_partial_link_text(ele=ele,link_text=link_text,timeout=timeout)).perform()

    def until_move_to_element_by_link_text(self, ele=None, link_text='', timeout=10):
        """

        :param ele:WebElement
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        ActionChains(self.driver).move_to_element(
            self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text,timeout=timeout)).perform()

    def until_send_enter_by_css_selector(self, ele=None, css_selector='', timeout=10):
        """

        :param ele:WebElement
        :param css_selector:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout).send_keys(Keys.ENTER)

    def until_send_enter_by_link_text(self, ele=None, link_text='', timeout=10):
        """

        :param ele:WebElement
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text,timeout=timeout).send_keys(Keys.ENTER)

    def until_send_enter_by_partial_link_text(self, ele=None, link_text='', timeout=10):
        """

        :param ele:WebElement
        :param link_text:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_partial_link_text(ele=ele,link_text=link_text,timeout=timeout).send_keys(Keys.ENTER)

    def until_send_text_by_css_selector(self, ele=None, css_selector='', text='', timeout=10):
        """

        :param ele:WebElement
        :param css_selector:
        :param text:
        :return:
        """
        if not css_selector or not text:
            self.error_log(e='css_selector和text都不可以为空')
            return None
        if not ele:
            ele = self.driver
        self.until_presence_of_element_located_by_css_selector(ele=ele, css_selector=css_selector, timeout=timeout).clear()
        self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout).send_keys(text)

    def until_get_elements_len_by_css_selector(self, ele=None, css_selector='', timeout=1):
        """

        :param ele:WebElement
        :param css_selector:
        :param timeout:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为空')
            return None
        if not ele:
            ele = self.driver
        return len(self.until_presence_of_all_elements_located_by_css_selector(ele=ele,css_selector=css_selector,
                                                                               timeout=timeout))

    def until_send_key_arrow_down_by_css_selector(self, ele=None,css_selector='', min_frequency=100, max_frequency=300, timeout=1):
        """

        :param ele:WebElement
        :param css_selector:
        :param min_frequency:
        :param max_frequency:
        :param timeout:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不可以为None')
            return None
        if not ele:
            ele = self.driver
        for i in range(random.randint(min_frequency,max_frequency)):
            ActionChains(self.driver).move_to_element(
                self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=timeout))\
                .send_keys(Keys.ARROW_DOWN).perform()

    def until_send_key_arrow_down_by_partial_link_text(self, ele=None,link_text='', frequency=100):
        """

        :param ele:WebElement
        :param link_text:
        :param frequency:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        for i in range(frequency):
            ActionChains(self.driver).move_to_element(
                self.until_presence_of_element_located_by_partial_link_text(ele=ele,link_text=link_text))\
                .send_keys(Keys.ARROW_DOWN).perform()

    def until_send_key_arrow_down_by_link_text(self, ele=None,link_text='', frequency=100):
        """

        :param ele:WebElement
        :param link_text:
        :param frequency:
        :return:
        """
        if not link_text:
            self.error_log(e='link_text不可以为None')
            return None
        if not ele:
            ele = self.driver
        for i in range(frequency):
            ActionChains(self.driver).move_to_element(
                self.until_presence_of_element_located_by_link_text(ele=ele,link_text=link_text))\
                .send_keys(Keys.ARROW_DOWN).perform()

    def until_title_is(self, ele=None, timeout=10, title=''):
        """
        判断title,返回布尔值
        :param ele:WebElement
        :param timeout:
        :param title:
        :return:
        """
        if not ele:
            ele = self.driver
        if not title:
            self.error_log(e='标题为空!!!')
            return False
        return WebDriverWait(ele, timeout).until(EC.title_is(title))

    def until_title_contains(self, ele=None, timeout=10, title=''):
        """
        判断title，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param title:
        :return:
        """
        if not ele:
            ele = self.driver
        if not title:
            self.error_log(e='标题为空!!!')
            return False
        return WebDriverWait(ele,timeout).until(EC.title_contains(title))

    def until_presence_of_element_located_by_id(self, ele=None, timeout=10, id=''):
        """
        判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.ID, id)))

    def until_presence_of_element_located_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    def until_presence_of_element_located_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))

    def until_presence_of_element_located_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, link_text)))

    def until_visibility_of_by_id(self, ele=None, timeout=10, id=''):
        """
        判断元素是否可见，如果可见就返回这个元素
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.ID, id)))

    def until_visibility_of_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断元素是否可见，如果可见就返回这个元素
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.CSS_SELECTOR, css_selector)))

    def until_visibility_of_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断元素是否可见，如果可见就返回这个元素
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.LINK_TEXT, link_text)))

    def until_visibility_of_by_partial_link_text(self, ele=None, timeout=10, partial_link_text=''):
        """
        判断元素是否可见，如果可见就返回这个元素
        :param ele:WebElement
        :param timeout:
        :param partial_link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not partial_link_text:
            self.error_log(e='partial_link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.visibility_of((By.PARTIAL_LINK_TEXT, partial_link_text)))

    def until_presence_of_all_elements_located_by_id(self, ele=None, timeout=10, id=''):
        """
        判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.ID, id)))

    def until_presence_of_all_elements_located_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    def until_presence_of_all_elements_located_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.LINK_TEXT, link_text)))

    def until_presence_of_all_elements_located_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, link_text)))

    def until_visibility_of_any_elements_located_by_id(self, ele=None, timeout=10, id=''):
        """
        判断是否至少有一个元素在页面中可见，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.ID, id)))

    def until_visibility_of_any_elements_located_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断是否至少有一个元素在页面中可见，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    def until_visibility_of_any_elements_located_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断是否至少有一个元素在页面中可见，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.LINK_TEXT, link_text)))

    def until_visibility_of_any_elements_located_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断是否至少有一个元素在页面中可见，如果定位到就返回列表
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, link_text)))

    def until_text_to_be_present_in_element_located_by_id(self, ele=None, timeout=10, id=''):
        """
        判断指定的元素中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.ID, id)))

    def until_text_to_be_present_in_element_located_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断指定的元素中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    def until_text_to_be_present_in_element_located_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断指定的元素中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.LINK_TEXT, link_text)))

    def until_text_to_be_present_in_element_located_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断指定的元素中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, link_text)))

    def until_text_to_be_present_in_element_value_by_id(self, ele=None, timeout=10, id='', _text=''):
        """
        判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param id:
        :param _text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.ID, id),_text))

    def until_text_to_be_present_in_element_value_by_css_selector(self, ele=None, timeout=10, css_selector=None, _text=None):
        """
        判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :param _text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, css_selector),
                                                                                        _text))

    def until_text_to_be_present_in_element_value_by_link_text(self, ele=None, timeout=10, link_text='', _text=''):
        """
        判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :param _text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.LINK_TEXT, link_text),
                                                                                        _text))

    def until_text_to_be_present_in_element_value_by_partial_link_text(self, ele=None, timeout=10, link_text='', _text=''):
        """
        判断指定元素的属性值中是否包含了预期的字符串，返回布尔值
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :param _text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.text_to_be_present_in_element_value((By.PARTIAL_LINK_TEXT, link_text),
                                                                                        _text))

    def until_frame_to_be_available_and_switch_to_it(self, ele=None, timeout=10):
        """
        判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False
        :param ele:WebElement
        :param timeout:
        :return:
        """
        if not ele:
            ele = self.driver
        return WebDriverWait(ele, timeout).until(EC.frame_to_be_available_and_switch_to_it(ele))

    def until_invisibility_of_element_located_by_id(self, ele=None, timeout=10, id=''):
        """
        判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.ID, id)))

    def until_invisibility_of_element_located_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector)))

    def until_invisibility_of_element_located_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.LINK_TEXT, link_text)))

    def until_invisibility_of_element_located_by_partial_link_text(self, ele=None, timeout=10, partial_link_text=''):
        """
        判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素
        :param ele:WebElement
        :param timeout:
        :param partial_link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not partial_link_text:
            self.error_log(e='partial_link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.invisibility_of_element_located((By.LINK_TEXT, partial_link_text)))

    def until_element_to_be_clickable_by_id(self, ele=None, timeout=10, id=''):
        """
        判断某个元素中是否可见并且是enable的，代表可点击
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.ID, id)))

    def until_element_to_be_clickable_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断某个元素中是否可见并且是enable的，代表可点击
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

    def until_element_to_be_clickable_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素中是否可见并且是enable的，代表可点击
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))

    def until_element_to_be_clickable_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素中是否可见并且是enable的，代表可点击
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text)))

    def until_staleness_of_by_id(self, ele=None, timeout=10, id=''):
        """
        等待某个元素从dom树中移除
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.ID, id)))

    def until_staleness_of_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        等待某个元素从dom树中移除
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.CSS_SELECTOR, css_selector)))

    def until_staleness_of_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        等待某个元素从dom树中移除
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.LINK_TEXT, link_text)))

    def until_staleness_of_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        等待某个元素从dom树中移除
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.staleness_of((By.PARTIAL_LINK_TEXT, link_text)))

    def until_element_to_be_selected_by_id(self, ele=None, timeout=10, id=''):
        """
        判断某个元素是否被选中了,一般用在下拉列表
        :param ele:WebElement
        :param timeout:
        :param id:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.ID, id)))

    def until_element_to_be_selected_by_css_selector(self, ele=None, timeout=10, css_selector=''):
        """
        判断某个元素是否被选中了,一般用在下拉列表
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.CSS_SELECTOR, css_selector)))

    def until_element_to_be_selected_by_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素是否被选中了,一般用在下拉列表
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.LINK_TEXT, link_text)))

    def until_element_to_be_selected_by_partial_link_text(self, ele=None, timeout=10, link_text=''):
        """
        判断某个元素是否被选中了,一般用在下拉列表
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_to_be_selected((By.PARTIAL_LINK_TEXT, link_text)))

    def until_element_selection_state_to_be_by_id(self, ele=None, timeout=10, id='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param id:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.ID, id),status))

    def until_element_selection_state_to_be_by_css_selector(self, ele=None, timeout=10, css_selector='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.CSS_SELECTOR, css_selector),status))

    def until_element_selection_state_to_be_by_link_text(self, ele=None, timeout=10, link_text='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.LINK_TEXT, link_text),status))

    def until_element_selection_state_to_be_by_partial_link_text(self, ele=None, timeout=10, link_text='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_selection_state_to_be((By.PARTIAL_LINK_TEXT, link_text),status))

    def until_element_located_selection_state_to_be_by_id(self, ele=None, timeout=10, id='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param id:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not id:
            self.error_log(e='id为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.ID, id),status))

    def until_element_located_selection_state_to_be_by_css_selector(self, ele=None, timeout=10, css_selector='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param css_selector:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not css_selector:
            self.error_log(e='css_selector为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, css_selector),status))

    def until_element_located_selection_state_to_be_by_link_text(self, ele=None, timeout=10, link_text='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.LINK_TEXT, link_text),status))

    def until_element_located_selection_state_to_be_by_partial_link_text(self, ele=None, timeout=10, link_text='', status=True):
        """
        判断某个元素的选中状态是否符合预期
        :param ele:WebElement
        :param timeout:
        :param link_text:
        :param status:
        :return:
        """
        if not ele:
            ele = self.driver
        if not link_text:
            self.error_log(e='link_text为空!!!')
            return None
        return WebDriverWait(ele, timeout).until(EC.element_located_selection_state_to_be((By.PARTIAL_LINK_TEXT, link_text),
                                                                                          status))

    def until_alert_is_present(self, ele=None, timeout=10):
        """
        判断页面上是否存在alert,如果有就切换到alert并返回alert的句柄
        :param ele:WebElement
        :param timeout:
        :return:
        """
        if not ele:
            ele = self.driver
        return WebDriverWait(ele, timeout).until(EC.alert_is_present())

    def ismore_by_scroll_page_judge_by_len(self, css_selector, min_offset=1000, max_offset=5000, comment_len=0):
        """
        通过长度判断页面是否有更多
        :param css_selector:
        :param min_offset:
        :param max_offset:
        :param comment_len:
        :return:
        """
        self.info_log(data='...开始下拉页面...')
        while (True):
            list_len = self.until_get_elements_len_by_css_selector(
                css_selector=css_selector,timeout=1)
            self.ramdon_vertical_scroll_to(min_offset=min_offset,max_offset=max_offset)
            list_len2 = self.until_get_elements_len_by_css_selector(css_selector=css_selector,timeout=1)
            self.info_log(data='当前数量%s:' % list_len2)
            if list_len == list_len2:
                if comment_len:
                    if list_len2 >= comment_len:
                        break
                time.sleep(2)
                self.ramdon_vertical_scroll_to(min_offset=min_offset,max_offset=max_offset)
                list_len2 = self.until_get_elements_len_by_css_selector(css_selector=css_selector,timeout=1)
                if list_len == list_len2:
                    break
        self.logger.info('...结束下拉页面...')

    def until_ismore_by_send_key_arrow_down_judge_by_len(self, list_css_selector='', ele_css_selector='', min_frequency=100, max_frequency=300, comment_len=0, timeout=1):
        """
        通过长度判断页面是否有更多
        :param list_css_selector:列表的css样式
        :param ele_css_selector:发送向下指令的元素的css样式
        :param min_frequency:表示按向下键的次数
        :param max_frequency:
        :param comment_len:
        :param timeout:
        :return:
        """
        if not list_css_selector:
            self.error_log(e='list_css_selector不可以为空!!!')
            return None
        if not ele_css_selector:
            self.error_log(e='ele_css_selector不可以为空!!!')
            return None
        self.info_log(data='...开始下拉页面...')
        while (True):
            list_len = self.until_get_elements_len_by_css_selector(css_selector=list_css_selector,timeout=timeout)
            self.until_send_key_arrow_down_by_css_selector(css_selector=ele_css_selector,
                             min_frequency=min_frequency,max_frequency=max_frequency,timeout=timeout)
            list_len2 = self.until_get_elements_len_by_css_selector(css_selector=list_css_selector)
            self.info_log(data='当前数量%s:' % list_len2)
            if list_len == list_len2:
                if comment_len:
                    if list_len2 >= comment_len:
                        break
                time.sleep(2)
                self.until_send_key_arrow_down_by_css_selector(css_selector=ele_css_selector,
                                  min_frequency=min_frequency,max_frequency=max_frequency,timeout=timeout)
                list_len2 = self.until_get_elements_len_by_css_selector(css_selector=list_css_selector,timeout=timeout)
                if list_len == list_len2:
                    break
        self.logger.info('...结束下拉页面...')

    def until_click_by_vertical_scroll_page_down_by_css_selector(self, ele=None, css_selector='', offset=8, try_times=20):
        """

        :param ele:
        :param click_css_selector:
        :param offset:
        :param try_times:
        :return:
        """
        failed_times = 0
        click_ele = self.until_presence_of_element_located_by_css_selector(ele=ele, css_selector=css_selector)
        while(True):
            self.scroll_into_view(ele=click_ele)
            if failed_times > try_times:
                break
            try:
                click_ele.click()
                self.info_log(data='点击成功')
                break
            except Exception:
                failed_times += 1
                self.warning_log(e='...正在尝试第%s次点击...'%failed_times)
                self.vertical_scroll_by(offset=offset)

    def until_click_by_vertical_scroll_page_down(self, click_ele=None, offset=8, try_times=20):
        """

        :param ele:
        :param offset:
        :param try_times:
        :return:
        """
        failed_times = 0
        while(True):
            self.scroll_into_view(ele=click_ele)
            if failed_times > try_times:
                break
            try:
                click_ele.click()
                self.info_log(data='点击成功')
                break
            except Exception:
                failed_times += 1
                self.warning_log(e='...正在尝试第%s次点击...'%failed_times)
                self.vertical_scroll_by(offset=offset)

    def until_presence_by_vertical_scroll_page_down_by_css_selector(self, ele=None, css_selector='', offset=8, try_times=20, timeout=1):
        """

        :param ele:WebElement
        :param css_selector:
        :param offset:
        :param try_times:
        :param timeout:
        :return:
        """
        if not css_selector:
            self.error_log(e='css_selector不允许为空!!!')
            return None
        if not ele:
            ele = self.driver
        failed_times = 0
        while(True):
            if failed_times > try_times:
                break
            try:
                self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=css_selector,timeout=float(timeout)/10)
                self.info_log(data='元素存在,可以访问')
                break
            except Exception:
                failed_times += 1
                self.warning_log(e='...正在尝试第%s次下拉...'%failed_times)
                self.vertical_scroll_by(offset=offset)

    def until_refresh_by_css_selector(self, css_selector='', try_times=10):
        """

        :param css_selector:
        :param try_times:
        :return:
        """
        count = 0
        if not css_selector:
            self.error_log(e='css_selector不可以为空!!!')
            return None
        for i in range(try_times):
            try:
                self.until_presence_of_element_located_by_css_selector(css_selector=css_selector,timeout=1)
            except Exception as e:
                count += 1
                self.info_log(data='第%s次刷新!!!'%count)
                self.driver.refresh()

    def until_click_no_next_page_by_css_selector(self, func=None, css_selector='', timeout=1, pause_time=1, is_next=True, **kwargs):
        """
        根据css样式点击直到没有下一页
        :param func:
        :param css_selector:
        :param timeout:
        :param pause_time:
        :param is_next:专门用来测试的时候使用,表示是否点击下一页
        :param kwargs:
        :return:
        """
        def empty_func(**kwargs):
            pass
        if not css_selector:
            self.error_log(e='css_selector不可以为空!!!')
            raise ValueError
        if not func:
            func = empty_func
            self.warning_log(e='当前func为空,没有什么操作需要执行!!!')
        count = 0
        while(True):
            count += 1
            self.info_log(data='当前翻到第%s页...' % count)
            time.sleep(pause_time)
            try:
                func(**kwargs)
                if not is_next:#在调试的时候不需要下一页
                    break
                self.focus_on_element_by_css_selector(css_selector=css_selector)
                self.until_click_by_css_selector(css_selector=css_selector,timeout=timeout)
            except Exception as e:
                self.error_log(e=str(e)+'\n没有下一页了!!!',istraceback=False)
                break

    def until_click_no_next_page_by_partial_link_text(self, func=None, link_text='', timeout=1, pause_time=1, is_next=True, **kwargs):
        """
        根据链接文字点击直到没有下一页
        :param func:
        :param link_text:
        :param timeout:
        :param pause_time:
        :param is_next:
        :param kwargs:
        :return:
        """
        def empty_func(**kwargs):
            pass
        if not link_text:
            self.error_log(e='link_text不可以为空!!!')
            raise ValueError
        if not func:
            func = empty_func
            self.warning_log(e='当前func为空,没有什么操作需要执行!!!')
        count = 0
        while(True):
            count += 1
            self.info_log(data='当前翻到第%s页...' % count)
            time.sleep(pause_time)
            try:
                func(**kwargs)
                if not is_next:#在调试的时候不需要下一页
                    break
                self.focus_on_element_by_partial_link_text(link_text=link_text)
                self.until_click_by_partial_link_text(link_text=link_text,timeout=timeout)
            except Exception as e:
                self.error_log(e=str(e) + '\n没有下一页了!!!', istraceback=False)
                break

    def close_pre_page(self):
        """
        关闭先前的页面
        :return:
        """
        self.driver.switch_to.window(self.driver.window_handles[-2])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_window_by_index(self,index=None):
        """
        根据索引切换浏览器窗口
        :param index:
        :return:
        """
        if not index:
            self.error_log(e='index不可以为空!!!')
            return None
        self.driver.switch_to.window(self.driver.window_handles[index])

#######################################external function#####################################################

    def get_data_key(self):
        """
        获取数据关键字
        :return:
        """
        return self.data_key

    def get_current_data_list_from_mongodb(self, collection=None, *keys):
        """
        获取当前的爬虫数据,以列表形式返回
        :param collection:
        :param keys:表示要保留的关键字
        :return:
        """
        if not collection:
            self.error_log(e='目标数据库不可以为空!!!')
            return None
        if keys:
            data_list = []
            for data in collection.find(self.get_data_key()):
                data_tmp = {}
                for key in keys:
                    data_tmp.setdefault(key,data.get(key))
                data_list.append(data_tmp)
            return data_list
        else:
            return list(collection.find(self.get_data_key()))

    def get_current_data_from_mongodb(self, collection=None, other_key=None):
        """
        获取当前的爬虫数据,以字典形式返回
        :param collection:
        :param other_key:
        :return:
        """
        if not collection or not other_key:
            self.error_log(e='目标数据库或者关键字不可以为空!!!')
            return None
        key = self.merge_dict(other_key,self.get_data_key())
        return collection.find(key)[0]

    def save_data_list_to_mongodb(self, fieldlist=Fieldlist(), mongodb=Mongodb(), datalist=[]):
        """
        保存数据列表到mongodb
        :param fieldlist:
        :param mongodb:
        :param datalist:
        :return:
        """
        if fieldlist == None:
            self.error_log(e='fieldlist不可以为空!!!')
            raise ValueError
        if mongodb == None:
            self.error_log(e='mongodb不可以为空!!!')
            raise ValueError
        field_key = []
        for field in fieldlist:
            if field.fieldtype == FieldType.KEY_STR:
                field_key.append(field.fieldname)
        for data in datalist:
            key = self.merge_dict(self.get_data_key(),{fk: data.get(fk) for fk in field_key})
            data = self.merge_dict(self.get_data_key(),data)
            crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬虫的时间
            data.setdefault(FieldName.CRAWL_TIME,crawl_time)
            collection_curr = mongodb.get_collection()
            if len(list(collection_curr.find(key))) == 0:
                collection_curr.insert(data)
            else:
                collection_curr.update(key, {'$set': data})

    def save_data_to_mongodb(self, fieldlist=Fieldlist(), mongodb=Mongodb(), data={}):
        """
        通过爬虫单元将数据保存到mongodb
        :param fieldlist:
        :param mongodb:
        :param data:要保存的数据
        :return:
        """
        field_key = []
        for field in fieldlist:
            if field.fieldtype == FieldType.KEY_STR:
                field_key.append(field.fieldname)
        key = self.merge_dict(self.get_data_key(),{fk: data.get(fk) for fk in field_key})
        data = self.merge_dict(self.get_data_key(),data)
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 爬虫的时间
        data.setdefault(FieldName.CRAWL_TIME,crawl_time)
        collection_curr = mongodb.get_collection()
        if len(list(collection_curr.find(key))) == 0:
            collection_curr.insert(data)
        else:
            collection_curr.update(key, {'$set': data})

    def merge_dict(self,data1,data2):
        """
        合并字典
        :param data1:
        :param data2:
        :return:
        """
        return dict(data1, **data2)

    def filter_integer(self, str):
        """
        从字符串过滤整型数字
        :param str:
        :return:
        """
        return int(re.sub(r'[^\d]*','',str))

    def filter_float(self, str):
        """
        从字符串过滤浮点数
        :param str:
        :return:
        """
        return float(re.sub(r'[^\d.]*','',str))

    def filter_str(self, str):
        """
        过滤掉字符串的换行符
        :param str:
        :return:
        """
        return re.sub(r'[\n]*','',str).strip()

    def get_random_time(self, a=50000, b=150000):
        """

        :param a:
        :param b:
        :return:
        """
        if not isinstance(a,int) or not isinstance(b,int):
            self.error_log(e='类型错误!!!')
            raise ValueError
        c = b
        if a > b:
            b = a
        a = c
        pause_time = float(random.randint(a, b))
        for i in range(len(str(a))-1):
            pause_time /= 10
        self.debug_log(data='随机时间为:%s'%pause_time)
        return pause_time

    def get_key_str_field_by_css_selector(self, field=Field(), ele=None):
        """
        获得条目的关键字段
        :param field:
        :param ele:WebElement
        :return:
        """
        time.sleep(field.pause_time)
        try:
            if ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=field.css_selector,timeout=field.timeout)
            elif ele and not field.css_selector:
                ele = ele
            elif not ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=field.css_selector,timeout=field.timeout)
            else:
                self.error_log(name=field.fieldname,e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            self.focus_on_element(ele=ele)
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if field.attr:
                _str = ele.get_attribute(field.attr)
            else:
                _str = ele.text
            if field.is_debug:
                self.debug_log(name=field.fieldname,data=_str)
            _str = self.filter_str(_str)
            _str = re.sub(field.regex, field.repl, _str)
            if field.filter_func:
                _str = field.filter_func(self, _str)
        except Exception as e:
            self.error_log(name=field.fieldname, e=str(e))
            _str = ''
        self.info_log(name=field.fieldname, data=_str)
        return _str

    def get_str_field_by_css_selector(self, field=Field(), ele=None):
        """
        获取条目的字符串字段
        :param field:
        :param ele:WebElement
        :return:
        """
        time.sleep(field.pause_time)
        try:
            if ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=field.css_selector,timeout=field.timeout)
            elif ele and not field.css_selector:
                ele = ele
            elif not ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=field.css_selector,timeout=field.timeout)
            else:
                self.error_log(name=field.fieldname, e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            self.focus_on_element(ele=ele)
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if field.attr:
                _str = ele.get_attribute(field.attr)
            else:
                _str = ele.text
            if field.is_debug:
                self.debug_log(name=field.fieldname, data=_str)
            _str = self.filter_str(_str)
            _str = re.sub(field.regex, field.repl, _str)
            if field.filter_func:
                _str = field.filter_func(self, _str)
        except Exception as e:
            self.error_log(name=field.fieldname, e=str(e))
            _str = ''
        self.info_log(name=field.fieldname, data=_str)
        return _str

    def get_str_list_field_by_css_selector(self, field=Field(), ele=None):
        """
        获取条目的字符串列表字段
        :param field:
        :param ele:WebElement
        :return:
        """
        time.sleep(field.pause_time)
        _list = []
        try:
            list_ele = self.until_presence_of_element_located_by_css_selector(
                ele=ele,css_selector=field.list_css_selector,timeout=field.timeout)
            if not list_ele:
                self.warning_log(name=field.fieldname,e='该字段为空')
                return None
            for item in self.until_presence_of_all_elements_located_by_css_selector(
                    ele=list_ele,css_selector=field.item_css_selector,timeout=field.timeout):
                _str = self.get_str_field_by_css_selector(ele=item,field=field)
                if _str:
                    _list.append(_str)
        except Exception as e:
            self.error_log(name=field.fieldname,e=str(e))
        self.info_log(name=field.fieldname, data=json.dumps(_list))
        return _list

    def get_int_field_by_css_selector(self, field=Field(), ele=None):
        """
        获取整型的字段
        :param field:
        :param ele:WebElement
        :return:
        """
        time.sleep(field.pause_time)
        try:
            if ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=field.css_selector,timeout=field.timeout)
            elif ele and not field.css_selector:
                ele = ele
            elif not ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=field.css_selector,timeout=field.timeout)
            else:
                self.error_log(name=field.fieldname, e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            self.focus_on_element(ele=ele)
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if field.attr:
                _str = ele.get_attribute(field.attr)
            else:
                _str = ele.text
            if field.is_debug:
                self.debug_log(name=field.fieldname, data=_str)
            _str = self.filter_str(_str)
            _str = re.sub(field.regex, field.repl, _str)
            if field.filter_func:
                _str = field.filter_func(self, _str)
            _int = self.filter_integer(_str)
        except Exception as e:
            self.error_log(name=field.fieldname, e=str(e))
            _int = 0
        self.info_log(name=field.fieldname, data=str(_int))
        return _int

    def get_float_field_by_css_selector(self, field=Field(), ele=None):
        """
        获取浮点型的字段
        :param field:
        :param ele:WebElement
        :return:
        """
        time.sleep(field.pause_time)
        try:
            if ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    ele=ele,css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(ele=ele,css_selector=field.css_selector, timeout=field.timeout)
            elif ele and not field.css_selector:
                ele = ele
            elif not ele and field.css_selector:
                self.until_presence_by_vertical_scroll_page_down_by_css_selector(
                    css_selector=field.css_selector,offset=field.offset,timeout=field.timeout,try_times=field.try_times)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=field.css_selector, timeout=field.timeout)
            else:
                self.error_log(name=field.fieldname, e='未指定样式选择器和目标元素,无法取得该字段内容!!!')
                return
            self.focus_on_element(ele=ele)
            ActionChains(self.driver).move_to_element(ele).perform()
            self.vertical_scroll_by()
            if field.attr:
                _str = ele.get_attribute(field.attr)
            else:
                _str = ele.text
            if field.is_debug:
                self.debug_log(name=field.fieldname, data=_str)
            _str = self.filter_str(_str)
            _str = re.sub(field.regex, field.repl, _str)
            if field.filter_func:
                _str = field.filter_func(self, _str)
            _float = self.filter_float(_str)
        except Exception as e:
            self.error_log(name=field.fieldname, e=str(e))
            _float = 0.0
        self.info_log(name=field.fieldname, data=str(_float))
        return _float

    def run_new_tab_task(self, try_times=15, pause_time=1, name='', url='', func=None, **kwargs):
        """
        运行一个新建标签页的任务(默认根据url打开标签页)
        :param try_times:
        :param pause_time:暂停的时间
        :param name:页面名称
        :param url:标签页链接
        :param func:执行函数
        :param kwargs:执行函数参数
        :return:
        """
        def empty_func(**kwargs):
            return None
        if not func:
            func = empty_func
            self.warning_log(name=name, e='标签页任务里面没有具体要执行的内容!!!')
        if not url:
            self.error_log(name=name,e='标签页任务里面没有具体要打开的url!!!')
            raise ValueError
        if not self.fast_new_page(url,try_times=try_times):
            return None
        time.sleep(pause_time)
        data = func(**kwargs)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return data

    def run_click_tab_task(self, ele=None, try_times=15, pause_time=1, name='', click_css_selector='', func=None, page_func=None, **kwargs):
        """
        运行一个点击出来的标签页的任务(通过按钮点击打开标签页)
        :param ele:
        :param try_times:
        :param pause_time:
        :param name:页面名称
        :param click_css_selector:点击的元素css选择器
        :param func:执行函数
        :param kwargs:执行函数参数
        :return:
        """
        def empty_func(**kwargs):
            return None
        if not ele:
            ele = self.driver
        if not func:
            self.warning_log(name=name, e='标签页任务里面没有具体要执行的内容!!!')
            func = empty_func
        if not click_css_selector:
            self.error_log(name=name,e='click_css_selector不可以为空!!!')
            raise ValueError
        if not self.fast_click_page_by_css_selector(click_css_selector=click_css_selector, ele=ele, try_times=try_times):
            return None
        time.sleep(pause_time)
        if not page_func:
            page_func = empty_func
        page_func()
        data = func(**kwargs)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return data

    def select_Field_by_css_selector(self, field=Field(), ele=None):
        """
        根据css选择器来得到每个字段对应的值
        :param field:
        :param ele:WebElement
        :return:
        """
        if field == None:
            self.error_log(e='field不可以为空!!!')
            raise ValueError
        if field.fieldtype == FieldType.KEY_STR:
            return self.get_key_str_field_by_css_selector(ele=ele,field=field)
        elif field.fieldtype == FieldType.STR:
            return self.get_str_field_by_css_selector(ele=ele,field=field)
        elif field.fieldtype == FieldType.LIST_STR:
            return self.get_str_list_field_by_css_selector(ele=ele,field=field)
        elif field.fieldtype == FieldType.INT:
            return self.get_int_field_by_css_selector(ele=ele,field=field)
        elif field.fieldtype == FieldType.FLOAT:
            return self.get_float_field_by_css_selector(ele=ele,field=field)

    def from_page_get_data_list(self, page=Page()):
        """
        从页面爬取一个数据列表
        :param page:爬虫页面
        :return:
        """
        if page == None:
            self.error_log(e='page不可以为空!!!')
            raise ValueError
        self.info_log(data=page.name)
        data_list = list()
        if page.listcssselector == None:
            self.error_log(e='listcssselector不可以为空!!!')
            raise ValueError
        try:
            elements_list = self.until_presence_of_all_elements_located_by_css_selector(css_selector=page.listcssselector.list_css_selector)
            if page.listcssselector.item_end < 0 or page.listcssselector.item_end < 0:#如果end或start小于0
                self.error_log(e='item_end不可以小于0!!!')
                raise ValueError
            if page.listcssselector.item_end > 0 and page.listcssselector.item_end <= page.listcssselector.item_start:
                self.error_log(e='item_end在设置的情况下，不可以小于item_start!!!')
                raise ValueError
            if page.listcssselector.item_end == 0:#表示item_end未修改
                elements_list = elements_list[page.listcssselector.item_start:]
            else:
                elements_list = elements_list[page.listcssselector.item_start:page.listcssselector.item_end]
            for each in elements_list:
                item = each
                if page.listcssselector.item_css_selector:#如果不为空
                    item = self.until_presence_of_element_located_by_css_selector(ele=each,css_selector=page.listcssselector.item_css_selector)
                data = self.from_fieldlist_get_data(page=page, ele=item)
                if data:#如果因为关键字段数据不为空,则数据不为空
                    if page.is_save:
                        if page.mongodb == None:
                            self.error_log(e='无法确定数据保存位置!!!')
                            raise ValueError
                        else:
                            self.save_data_to_mongodb(fieldlist=page.fieldlist, mongodb=page.mongodb, data=data)
                    data_list.append(data)
        except Exception as e:
            self.error_log(e=str(e))
        return data_list

    def from_fieldlist_get_data(self, page=Page(), ele=None):
        """
        从字段列表获取数据
        :param page:爬虫页面
        :param ele:WebElement,当前条目所在的网页元素
        :return:
        """
        data = dict()
        internal_key = dict()
        for field in page.fieldlist:
            d = self.select_Field_by_css_selector(field=field, ele=ele)
            if not d and field.fieldtype == FieldType.KEY_STR:#如果默认的关键字为空,就不把数据加入数据库
                return None
            if field.fieldtype == FieldType.KEY_STR:
                internal_key.setdefault(field.fieldname, d)
            data.setdefault(field.fieldname, d)
        return data

    def from_page_add_data_to_data_list(self, page=Page(), data_list=list(), pre_page=Page(), page_func=None):
        """
        把当前页面的数据再次添加到之前的页面里面
        :param page:爬虫页面
        :param data_list:字典类型数据列表
        :param pre_page:先前的页面
        :param page_func:页面上面执行操作
        :return:
        """
        if page == None or pre_page == None:
            self.error_log(e='page或pre_page不可以为空!!!')
            raise ValueError
        #整合fieldlist
        fieldlist_merge = Fieldlist()
        for field in page.fieldlist:
            fieldlist_merge.append(field)
        for field in pre_page.fieldlist:
            fieldlist_merge.append(field)
        data_list_tmp = data_list
        for i in range(len(data_list)):
            if page.tabsetup.click_css_selector:
                #注意这里拼接出完整的css selector 是为了防止元素过期
                if pre_page.listcssselector.item_css_selector:
                    item_css_selector = '%s:nth-child(%s) > %s'%(pre_page.listcssselector.list_css_selector, i+1, pre_page.listcssselector.item_css_selector)
                else:
                    item_css_selector = '%s:nth-child(%s)' % (pre_page.listcssselector.list_css_selector, i+1)
                ele = self.until_presence_of_element_located_by_css_selector(css_selector=item_css_selector)
                add_data = self.run_click_tab_task(ele=ele, try_times=page.tabsetup.try_times, pause_time=page.tabsetup.pause_time, name=page.name, click_css_selector=page.tabsetup.click_css_selector, func=self.from_fieldlist_get_data, page_func=page_func, page=page)
            elif page.tabsetup.url_name:
                add_data = self.run_new_tab_task(try_times=page.tabsetup.try_times, pause_time=page.tabsetup.pause_time, name=page.name, url=data_list[i].get(page.tabsetup.url_name), func=self.from_fieldlist_get_data, page=page)
            else:
                self.error_log(e='不属于两种标签页类型!!!')
                raise ValueError
            if add_data and data_list_tmp[i]:#如果add_data不为空
                data_list_tmp[i].update(add_data)
                if page.is_save:
                    if len(data_list_tmp[i]) == len(fieldlist_merge):
                        self.save_data_to_mongodb(fieldlist=fieldlist_merge, mongodb=page.mongodb, data=data_list_tmp[i])#注意关键字段必定出现在前面一页
        return data_list_tmp

    def run_spider(self):
        """
        运行爬虫
        :return:
        """
        pass

    def start_session(self):
        self.driver.start_session(
            capabilities={'browserName': 'chrome',
                          'goog:chromeOptions': {'extensions': [], 'args': [self.curr_user_agent]}, 'platform': 'ANY',
                          'version': ''})

    def start_headless_session(self):
        self.driver.start_session(
            capabilities={'browserName': 'chrome',
                          'goog:chromeOptions': {'extensions': [], 'args': [self.curr_user_agent, '--headless']}, 'platform': 'ANY',
                          'version': ''})

    def fast_get_page(self, url:str, try_times=15, is_max=False):
        """
        打开网页快速加载页面,直到成功加载
        :param url:
        :param try_times:
        :param is_max:
        :return:
        """
        for i in range(1,try_times+1):
            try:
                if is_max:
                    self.driver.maximize_window()
                self.driver.get(url)
                self.vertical_scroll_to()  # 滚动到页面底部
                self.debug_log(data='经过%s次创建session和%s次关闭session,成功加载页面!!!'%(i,i-1))
                return True
            except Exception:
                self.error_log(e='第%s次加载页面失败!!!'%i, istraceback=False)
                self.driver.close()
                if self.isheadless:
                    self.start_headless_session()
                else:
                    self.start_session()
                time.sleep(1)
                self.driver.set_page_load_timeout(random.randint(5,15))
        self.exit_for_failing_to_load_page()
        return False

    def fast_new_page(self, url:str, try_times=15):
        """
        新建标签页码快速加载页面
        :param url:
        :param try_times:
        :return:
        """
        for i in range(1,try_times+1):
            try:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.set_page_load_timeout(random.randint(5,15))
                self.new_window(url)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.refresh()
                self.vertical_scroll_to()  # 滚动到页面底部
                self.debug_log(data='经过%s次创建标签页和%s次关闭标签页,成功加载页面!!!' % (i, i - 1))
                return True
            except Exception:
                self.error_log(e='第%s次加载页面失败!!!' % i, istraceback=False)
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])
        self.error_log(e='由于网络原因,无法加载页面,直接跳过!!!', istraceback=False)
        return False

    def fast_click_page_by_css_selector(self, click_css_selector:str, ele=None, try_times=15):
        """
        点击快速加载页面
        :param click_css_selector:
        :param ele:
        :param try_times:
        :return:
        """
        if not ele:
            ele = self.driver
        for i in range(1,try_times+1):
            try:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.set_page_load_timeout(random.randint(5,15))
                click_ele = self.until_presence_of_element_located_by_css_selector(ele=ele, css_selector=click_css_selector)
                self.focus_on_element(ele=click_ele)
                click_ele.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.refresh()
                self.vertical_scroll_to()  # 滚动到页面底部
                self.debug_log(data='经过%s次点击和%s次关闭标签页,成功加载页面!!!' % (i, i - 1))
                return True
            except Exception:
                self.error_log(e='第%s次加载页面失败!!!' % i, istraceback=False)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
        self.error_log(e='由于网络原因,无法加载页面,直接跳过!!!', istraceback=False)
        return False

    def fast_click_same_page_by_css_selector(self, click_css_selector:str, ele=None, try_times=15):
        """
        点击快速加载页面
        :param click_css_selector:
        :param ele:
        :param try_times:
        :return:
        """
        if not ele:
            ele = self.driver
        try:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.set_page_load_timeout(random.randint(5,15))
            click_ele = self.until_presence_of_element_located_by_css_selector(ele=ele, css_selector=click_css_selector)
            self.focus_on_element(ele=click_ele)
            click_ele.click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.refresh()
            self.vertical_scroll_to()  # 滚动到页面底部
            self.debug_log(data='经过%s次点击和%s次关闭标签页,成功加载页面!!!' % (1, 1 - 1))
            return True
        except Exception:
            self.error_log(e='第%s次加载页面失败!!!' % 1, istraceback=False)
            curr_url = self.driver.current_url
            self.debug_log(data=curr_url)
            if not self.fast_new_page(url=curr_url,try_times=try_times):
                self.exit_for_failing_to_load_page()
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def fast_click_first_item_page_by_partial_link_text(self, link_text:str, try_times=15):
        """
        点击列表第一个元素快速加载页面
        :param link_text:
        :param try_times:
        :return:
        """
        for i in range(1,try_times+1):
            try:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.set_page_load_timeout(random.randint(5,15))
                self.until_presence_of_all_elements_located_by_partial_link_text(link_text=link_text)[0].click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.refresh()
                self.vertical_scroll_to()  # 滚动到页面底部
                self.debug_log(data='经过%s次点击和%s次关闭标签页,成功加载页面!!!' % (i, i - 1))
                return True
            except Exception:
                self.error_log(e='第%s次加载页面失败!!!' % i, istraceback=False)
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])
        self.error_log(e='由于网络原因,无法加载页面,直接跳过!!!', istraceback=False)
        return False

    def fast_enter_page_by_partial_link_text(self, css_selector:str, try_times=15):
        """
        快速点击回车键加载页面
        :param css_selector:
        :param try_times:
        :return:
        """
        try:
            self.until_send_enter_by_css_selector(css_selector=css_selector)
        except Exception:
            self.fast_new_page(url=self.driver.current_url, try_times=try_times)
            self.driver.switch_to.window(self.driver.window_handles[-2])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def fast_click_first_item_same_page_by_partial_link_text(self, link_text:str, try_times=15):
        """
        快速点击链接在相同的页面加载页面
        :param link_text:
        :param try_times:
        :return:
        """
        curr_url = ''
        try:
            curr_url = self.until_presence_of_all_elements_located_by_partial_link_text(link_text=link_text)[0].get_attribute('href')
            self.until_presence_of_all_elements_located_by_partial_link_text(link_text=link_text)[0].click()
        except Exception:
            try:
                curr_url = self.driver.current_url
            except Exception:
                pass
            self.debug_log(data=curr_url)
            no_page = False
            if len(self.driver.window_handles) == 1:
                no_page = True
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
            if no_page:
                self.start_session()
                if not self.fast_get_page(url='https://www.baidu.com'):
                    self.exit_for_failing_to_load_page()
            else:
                self.driver.switch_to.window(self.driver.window_handles[-1])
            if not self.fast_new_page(url=curr_url, try_times=try_times):
                self.exit_for_failing_to_load_page()

    def exit_for_failing_to_load_page(self):
        self.error_log(e='由于网络原因,页面加载失败,退出爬虫程序,请稍后再试!!!')
        self.driver.quit()
        sys.exit(0)

    # def until_click_all_contains_partial_link_text_without_new_page(self, link_text):
    #     """
    #     直到点击包含...文字的链接,并且不打开新的页面(包括不新建页面的加载),仅仅是为了现实隐藏数据
    #     :param link_text:
    #     :return:
    #     """
    #     try:
    #         for ele in self.until_presence_of_all_elements_located_by_partial_link_text(link_text=link_text):
    #             self.until_click_by_vertical_scroll_page_down(click_ele=ele)
    #     except Exception as e:
    #         self.error_log(e=str(e))
