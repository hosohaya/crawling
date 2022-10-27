
import scrapy
import json
import os
import logging

from crawling.lib.jra import Jra
from crawling.view.jra.race import RaceView
from crawling.view.jra.result import ResultView

logging.basicConfig(filename='log/jra.log', level=logging.ERROR)


class JraSpider(scrapy.Spider):
    name = 'jra'
    allowed_domains = ['race.netkeiba.com']
    jra = Jra()
    exec = 'race' # race,result,list,2016,2017,2018,2019,2020,2021
    all_update = False

    def start_requests(self):
        # yield scrapy.Request('https://race.netkeiba.com/race/result.html?race_id=202104050405&rf=race_list')
        if self.exec == 'race': # 最新出馬表の取得
            crawl = json.load(open('json/jra/race.json', 'r'))
            for year, item1 in sorted(crawl.items()): # 年度
                for venue_id, item2 in sorted(item1.items()): # 開催地
                    for times, item3 in sorted(item2.items()): # 回数
                        for days in item3['days']: # 何日目
                            for number in range(1, 13): # レース番号
                                request = scrapy.Request('https://race.netkeiba.com/race/shutuba.html?race_id={}{}{}{}{}&rf=race_list'
                                    .format(str(year).zfill(4), str(venue_id).zfill(2), str(times).zfill(2), str(days).zfill(2), str(number).zfill(2)))
                                request.meta['exec'] = self.exec
                                request.meta['all_update'] = self.all_update
                                yield request
        elif self.exec == 'race_list': # 最新出馬表の取得
            dir = os.path.dirname(__file__)
            crawl = json.load(open(dir + '/../../task/race_list.json', 'r'))
            # os.remove(dir + '/../../task/race_list.json')
            for item1 in crawl: # URLキーリスト
                request = scrapy.Request('https://race.netkeiba.com/race/shutuba.html?race_id={}&rf=race_list'.format(item1['url_key']))
                request.meta['exec'] = self.exec
                request.meta['all_update'] = self.all_update
                yield request
        elif self.exec == 'result': # 最新結果の取得
            crawl = json.load(open('json/jra/result.json', 'r'))
            for year, item1 in sorted(crawl.items()): # 年度
                for venue_id, item2 in sorted(item1.items()): # 開催地
                    for times, item3 in sorted(item2.items()): # 回数
                        for days in item3['days']: # 何日目
                            for number in range(1, 13): # レース番号
                                request = scrapy.Request('https://race.netkeiba.com/race/result.html?race_id={}{}{}{}{}&rf=race_list'
                                    .format(str(year).zfill(4), str(venue_id).zfill(2), str(times).zfill(2), str(days).zfill(2), str(number).zfill(2)))
                                request.meta['exec'] = self.exec
                                request.meta['all_update'] = self.all_update
                                yield request
        elif self.exec == 'list': # 最新結果の取得
            dir = os.path.dirname(__file__)
            crawl = json.load(open(dir + '/../../task/list.json', 'r'))
            os.remove(dir + '/../../task/list.json')
            for item1 in crawl: # URLキーリスト
                request = scrapy.Request('https://race.netkeiba.com/race/result.html?race_id={}&rf=race_list'.format(item1['url_key']))
                request.meta['exec'] = self.exec
                request.meta['all_update'] = self.all_update
                yield request
        else: # 過去結果の取得
            crawl = json.load(open('json/jra/result{}.json'.format(self.exec), 'r'))
            for year, item1 in sorted(crawl.items()): # 年度
                for venue_id, item2 in sorted(item1.items()): # 開催地
                    for times, item3 in sorted(item2.items()): # 回数
                        for days in range(1, int(item3['days']) + 1): # 何日目
                            for number in range(1, 13): # レース番号
                                request = scrapy.Request('https://race.netkeiba.com/race/result.html?race_id={}{}{}{}{}&rf=race_list'
                                    .format(str(year).zfill(4), str(venue_id).zfill(2), str(times).zfill(2), str(days).zfill(2), str(number).zfill(2)))
                                request.meta['exec'] = self.exec
                                request.meta['all_update'] = self.all_update
                                yield request

    def parse(self, response):
        try:
            if 'exec' in response.meta and response.meta['exec'] == 'race':
                view = RaceView()
            elif 'exec' in response.meta and response.meta['exec'] == 'race_list':
                view = RaceView()
            else:
                view = ResultView()
            if view.setValue(response) == False:
                return
            if 'all_update' in response.meta and response.meta['all_update'] == True:
                self.jra.only_null = False
            self.jra.parse(view)
        except:
            logging.error('Parse function called on %s', response.url)
