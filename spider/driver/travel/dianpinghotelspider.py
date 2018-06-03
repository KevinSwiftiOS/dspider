# -*- coding:utf-8 -*-

from .traveldriver import *
from .params import *
from .fields import *

class DianpingHotelSpider(TravelDriver):
    def getCommentInfo2(self, shop_id, shop_name, comment_list_url, page):
        self.logger.info('commentinfo2')
        item_count = 0
        # 点击展开评论
        for each in self.driver.find_elements_by_css_selector(
                '#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li > div > div.review-truncated-words > div > a'):
            self.logger.info('正在展开评论...')
            each.click()

        for each in self.driver.find_elements_by_css_selector(
                '#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'):
            item_count += 1
            try:
                comment_user_name = each.find_element_by_css_selector('div > div.dper-info > a').text
            except Exception as e:
                self.error_log(field='comment_user_name',e=e)
                continue
            self.InfoLog(field='comment_user_name', data=comment_user_name)
            try:
                comment_user_url = each.find_element_by_css_selector('div > div.dper-info > a').get_attribute('href')
            except Exception as e:
                self.ErrorLog(field='comment_user_url', e=e)
                comment_user_url = ''
            try:
                comment_user_pic = each.find_element_by_css_selector('a > img').get_attribute('src')
            except Exception as e:
                self.ErrorLog(field='comment_user_pic', e=e)
                comment_user_pic = ''
            try:
                comment_time = each.find_element_by_css_selector('div > div.misc-info.clearfix > span.time').text
            except Exception as e:
                self.ErrorLog(field='comment_time', e=e)
                comment_time = ''
            self.InfoLog(field='comment_time', data=comment_time)
            try:
                comment_star = each.find_element_by_css_selector('div > div.review-rank > span').get_attribute('class')
                comment_star = float(re.sub(r'[^\d]*', r'', comment_star)) / 10
            except Exception as e:
                self.ErrorLog(field='comment_star', e=e)
                comment_star = 0
            try:
                comment_content = each.find_element_by_css_selector('div > div.review-words').text
                comment_content = re.sub(r'[\n]*', r'', comment_content).replace('收起评论', '')
            except Exception as e:
                self.ErrorLog(field='comment_content', e=e)
                comment_content = ''
            comment_img = list()
            try:
                review_pic = each.find_element_by_css_selector('div > div.review-pictures')
                for each1 in review_pic.find_elements_by_css_selector('ul > li'):
                    comment_img.append(each1.find_element_by_css_selector('a > img').get_attribute('data-lazyload'))
            except Exception as e:
                self.ErrorLog(field='comment_img', e=e)
            try:
                comment_like_replay = each.find_element_by_css_selector('div > div.misc-info.clearfix > span.actions').text
            except Exception as e:
                self.ErrorLog(field='comment_like_replay', e=e)
                comment_like_replay = ''
            try:
                comment_like = int(re.sub(r'[^\d]*', r'', comment_like_replay.split('回应')[0]))
            except Exception as e:
                self.ErrorLog(field='comment_like', e=e)
                comment_like = 0
            try:
                comment_replay = int(re.sub(r'[^\d]*', r'', comment_like_replay.split('回应')[1]))
            except Exception as e:
                self.ErrorLog(field='comment_replay', e=e)
                comment_replay = 0
            comment_data = {
                'shop_id': shop_id,
                'shop_name': shop_name,
                'comment_list_url': comment_list_url,
                'comment_user_name': comment_user_name,
                'comment_user_url': comment_user_url,
                'comment_user_pic': comment_user_pic,
                'comment_time': comment_time,
                'comment_star': comment_star,
                'comment_content': comment_content,
                'comment_img': comment_img,
                'comment_like': comment_like,
                'comment_replay': comment_replay,
                'page': page,
                'item_count': item_count,
            }
            key = {
                'shop_id': shop_id,
                'shop_name': shop_name,
                'comment_user_name': comment_user_name,
                'comment_time': comment_time,
            }
            self.SaveData(target=self.comments, key=key, data=comment_data)

    def getCommentInfo(self, shop_id, shop_name, comment_url):
        self.logger.info('commentinfo')
        page = 1
        while(True):  # 加载全部评论
            self.logger.info('*************************正在浏览 {} 评论页面的第 {} 页*************************'.format(shop_name, page))
            self.getCommentInfo2(shop_id, shop_name, comment_url, page)
            try:
                self.driver.find_element_by_partial_link_text(u'下一页').click()
                self.logger.info('*************************即将浏览 {} 评论页面的第 {} 页*************************'.format(shop_name, page + 1))
                # 产生随机暂停时间
                pause_time = (lambda x: 10 if x < 10 else x)(random.random() * random.randint(9999, 99999) / 222)
                self.logger.info('...随机暂停:{}s...'.format(pause_time))
                time.sleep(pause_time)
                page += 1
            except Exception as e:
                self.ErrorLog(field='评论下一页', e=e)
                pause_time = (lambda x: 10 if x < 10 else x)(random.random() * random.randint(9999, 99999) / 222)
                self.logger.info('...随机暂停:{}s...'.format(pause_time))
                time.sleep(pause_time)
                break
        try:
            shop_statistics = self.driver.find_element_by_css_selector(
                '#summaryfilter-wrapper > div.comment-condition.J-comment-condition.Fix > div.content').text
        except Exception as e:
            self.logger.error(e)
            shop_statistics = ''
        self.logger.info('################################结束浏览 {} 评论页面的共 {} 页############################'.format(shop_name, page))
        return shop_statistics

    def getShopInfo2(self, shop_id, shop_name):
        self.logger.info('shopinfo2')
        time.sleep(1)
        try:
            shop_address = self.driver.find_element_by_css_selector('#main > div > div.shop-brief > div').text
        except Exception as e:
            self.ErrorLog(field='shop_address', e=e)
            shop_address = ''
        self.InfoLog(field='shop_address', data=shop_address)
        self.driver.find_element_by_css_selector('#main > div > div.shop-brief > a').click()
        # try:
        #     shop_phone = driver.find_element_by_css_selector('body > div.J_phone').text
        # except Exception:
        #     shop_phone = ''
        # print 'shop_phone:{}'.format(shop_phone)
        try:
            shop_time = self.driver.find_element_by_css_selector(
                '#main > section.info-block.introduce > div.hotel-info > div:nth-child(2)').text.replace('\n', '')
        except Exception as e:
            self.ErrorLog(field='shop_time', e=e)
            shop_time = ''
        self.InfoLog(field='shop_time', data=shop_time)
        try:
            shop_info = self.driver.find_element_by_css_selector(
                '#main > section.info-block.introduce > div.hotel-info').text.replace('\n', '')
        except Exception as e:
            self.ErrorLog(field='shop_info', e=e)
            shop_info = ''
        self.driver.back()
        comment_url = 'https://www.dianping.com/shop/{}/review_all'.format(shop_id)
        self.NewWindow(comment_url)
        self.driver.switch_to_window(self.driver.window_handles[2])
        time.sleep(1)
        shop_statistics = self.getCommentInfo(shop_id, shop_name, comment_url)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[1])
        shop_data = {
            'shop_address': shop_address,
            'shop_info': shop_info,
            'shop_time': shop_time,
            'shop_statistics': shop_statistics
        }
        return shop_data

    def getShopInfo(self):
        self.logger.info('shopinfo')
        item_count = 0
        for each in self.driver.find_elements_by_css_selector('#app > div > div.J_searchList > ul > li'):
            item_count += 1
            self.logger.info('...正在查看第{}个酒店...'.format(item_count))
            item = each.find_element_by_css_selector('a')
            try:
                shop_name = item.find_element_by_css_selector('div.item-content > div.item-title > h3').text
            except Exception as e:
                self.ErrorLog(field='shop_name', e=e)
                shop_name = ''
            self.InfoLog(field='shop_name', data=shop_name)
            try:
                shop_url = item.get_attribute('href').split('?')[0]
            except Exception as e:
                self.ErrorLog(field='shop_url', e=e)
                continue
            self.InfoLog(field='shop_url', data=shop_url)
            try:
                shop_id = shop_url.split('/')[-1]
            except Exception as e:
                self.ErrorLog(field='shop_id', e=e)
                continue
            self.InfoLog(field='shop_id', data=shop_id)
            try:
                shop_img = item.find_element_by_css_selector('div.item-pic').get_attribute('style').split('\"')[1]
            except Exception as e:
                self.ErrorLog(field='shop_img', e=e)
                shop_img = ''
            shop_price = 0
            shop_comment = 0
            try:
                div_item_count = each.find_element_by_css_selector('div.item-content > div.item-comment')
                for each1 in div_item_count.find_elements_by_css_selector(
                        'span.item-comment-price'):
                    if '￥' in each1.text:
                        shop_price = float(re.sub(r'[^\d.]*', r'', item.find_element_by_css_selector(
                            'div.item-content > div.item-comment > span:nth-child(3)').text))
                    elif '条' in each1.text:
                        shop_comment = int(re.sub(r'[^\d]*', r'', item.find_element_by_css_selector(
                            'div.item-content > div.item-comment > span:nth-child(2)').text))
            except Exception as e:
                self.ErrorLog(field='shop_comment+price', e=e)
            self.InfoLog(field='shop_price', data=shop_price)
            self.InfoLog(field='shop_comment', data=shop_comment)
            try:
                shop_grade = float(item.find_element_by_css_selector('div.item-content > div.item-comment > span').get_attribute('class').split('-')[-1])/10
            except Exception as e:
                self.ErrorLog(field='shop_grade', e=e)
                shop_grade = 0
            try:
                shop_feature = item.find_element_by_css_selector('div.item-content > div.item-info > div.item-info-left').text.replace('\n','')
            except Exception as e:
                self.ErrorLog(field='shop_feature', e=e)
                shop_feature = ''
            try:
                shop_distance = re.sub(r'[^\d.km]*',r'',item.find_element_by_css_selector('div.item-content > div.item-info > div.item-info-right > span > span').text)
            except Exception as e:
                self.ErrorLog(field='shop_distance', e=e)
                shop_distance = ''
            self.InfoLog(field='shop_distance',data=shop_distance)
            if '暂停营业' in item.text:
                self.logger.info('暂停营业')
                return
            self.NewWindow(shop_url)
            self.driver.switch_to_window(self.driver.window_handles[1])
            shop_data = self.getShopInfo2(shop_id,shop_name)
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
            shop_data = self.MergeData(shop_data,{
                'shop_url' : shop_url,
                'shop_id':shop_id,
                'shop_img' : shop_img,
                'shop_name' : shop_name,
                'shop_price': shop_price,
                'shop_grade' : shop_grade,
                'shop_comment' : shop_comment,
                'shop_feature': shop_feature,
                'shop_distance':shop_distance,
                'item_count':item_count
            })
            key = {'shop_id': shop_id,}
            self.SaveData(target=self.shops, key=key, data=shop_data)
    def Run(self):
        self.logger.info('进入%s移动版主页...'%(self.data_website))
        self.driver.get('https://m.dianping.com/')
        time.sleep(1)
        self.driver.find_element_by_css_selector('body > div.J_header > header > div.search.J_search_trigger').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector(
            'body > div.J_search_container.search_container > form > div.head_cnt > div > input.J_search_input').send_keys(u''+self.data_region)
        self.logger.info('输入%s...'%(self.data_region))
        self.driver.find_element_by_css_selector(
            'body > div.J_search_container.search_container > form > div.head_cnt > div > input.J_search_input').send_keys(Keys.ENTER)
        self.logger.info('搜索千岛湖...')
        self.driver.find_element_by_css_selector('#app > div > div.J_searchList > nav > div > a:nth-child(2)').click()
        self.driver.find_element_by_css_selector(
            '#app > div > div.J_searchList > nav > section:nth-child(3) > div.menu.main > div:nth-child(1) > div:nth-child(5)').click()
        self.logger.info('选择%s...'%(self.data_source))
        self.driver.find_element_by_link_text(u'全部%s'%(self.data_source)).click()
        self.logger.info('选择全部%s...'%(self.data_source))
        time.sleep(1)
        while (True):
            try:
                self.driver.find_element_by_css_selector('#app > div > div.J_footer')
                break
            except Exception as e:
                self.ErrorLog(field='下拉店铺页面', e=e)
                self.DropDown(height=100000)
        self.getShopInfo()

    def run_spider(self):
        self.info_log(data='进入%s主页'%self.data_website)
        self.driver.get('https://www.baidu.com')
        self.until_presence_of_element_located_by_css_selector(css_selector='#kw').clear()
        self.until_send_text_by_css_selector(css_selector='#kw',text=self.data_website)
        self.until_send_enter_by_css_selector(css_selector='#kw')
        self.until_presence_of_all_elements_located_by_partial_link_text(link_text=self.data_website)[0].click()

