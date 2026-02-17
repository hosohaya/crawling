
import scrapy
import json
import logging

from crawling.lib.local import Local
from crawling.view.local.result import ResultView

logging.basicConfig(filename='log/local.log', level=logging.ERROR)


class LocalSpider(scrapy.Spider):
    name = 'local'
    allowed_domains = ['keibaeye.com']
    local = Local()
    exec = 'result'
    first = False

    def start_requests(self):
        # yield scrapy.Request('https://www.keibaeye.com/KeibaWeb/TodayRaceInfo/RaceMarkTable?k_raceDate=2021%2f02%2f10&k_raceNo=6&k_babaCode=31')
        if self.first: # 過去データの取得
            crawl = json.load(open('json/local/result2021.json', 'r'))
            for i1, item1 in sorted(crawl.items()): # 開催地
                for i2, item2 in sorted(item1.items()): # 日付
                    for i3 in range(1, int(item2) + 1): # レース番号
                        request = scrapy.Request('https://www.keibaeye.com/KeibaWeb/TodayRaceInfo/RaceMarkTable?k_raceDate={}&k_raceNo={}&k_babaCode={}'
                            .format(str(i2), str(i3), str(i1)))
                        request.meta['race_date'] = str(i2)
                        request.meta['race_number'] = str(i3)
                        request.meta['race_base_code'] = str(i1)
                        yield request
        else: # 最新データの取得
            crawl = json.load(open('json/local/result.json', 'r'))
            for i1, item1 in sorted(crawl.items()): # 開催地
                for i2, item2 in sorted(item1.items()): # 日付
                    for i3 in range(1, int(item2) + 1): # レース番号
                        request = scrapy.Request('https://www.keibaeye.com/KeibaWeb/TodayRaceInfo/RaceMarkTable?k_raceDate={}&k_raceNo={}&k_babaCode={}'
                            .format(str(i2), str(i3), str(i1)))
                        request.meta['race_date'] = str(i2)
                        request.meta['race_number'] = str(i3)
                        request.meta['race_base_code'] = str(i1)
                        yield request

    def parse(self, response):
        try:
            resultView = ResultView()
            resultView.setLocalParam(response.meta['race_date'], response.meta['race_number'], response.meta['race_base_code'])
            if resultView.setValue(response) == False:
                return
            self.local.parse(resultView)
        except:
            logging.error('Parse function called on %s', response.url)
