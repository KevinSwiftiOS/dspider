# -*- coding:utf-8 -*-

from spider.dianpinghotelspider import DianpingHotelSpider
import sys

if __name__ == '__main__':
    spider = DianpingHotelSpider(isheadless=True,ismobile=False,
                                id=sys.argv[1],
                                data_website=sys.argv[2],
                                data_region=sys.argv[3],
                                data_source=sys.argv[4])
    spider.run_spider()