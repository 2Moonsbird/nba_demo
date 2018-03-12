# -*- coding: utf-8 -*-

import scrapy
from ..items import PlayerItem,PlayerDataItem

class PlayerSpider(scrapy.Spider):

    name = 'players'

    base_url = 'https://www.basketball-reference.com/players/'

    indexes = list('abcdefghijklmnopqrstuvwxyz')

    custom_settings = {'DOWNLOAD_DELAY': 0.2, 'CONCURRENT_REQUESTS_PER_IP': 4}

    def start_requests(self):
        for index in self.indexes:
            url = self.base_url + index
            yield scrapy.Request(url=url,callback=self.parse_player)

    def parse_player(self,response):
        for player in response.css('tbody tr'):
            item = PlayerItem()
            item['name'] = player.css('th a::text').extract_first()
            item['position'] = player.css('td.center::text').extract_first()
            item['birthday'] = player.css('td a::text').extract_first()
            yield item
            url = player.css('th a::attr(href)').extract_first()
            if url:
                url = response.urljoin(url)
                yield scrapy.Request(url=url,callback=self.parse_player_data)


    def parse_player_data(self, response):
        data = PlayerDataItem()
        data['name'] = response.css('p strong strong::text').extract_first()

        summary = response.css('div.stats_pullout p strong::text').extract()
        if len(summary) == 2:
            p1 = response.css('div.p1 p::text').extract()[1::2]
            p2 = response.css('div.p2 p::text').extract()[1::2]
            p3 = response.css('div.p3 p::text').extract()[1::2]
        else:
            p1 = response.css('div.p1 p::text').extract()
            p2 = response.css('div.p2 p::text').extract()
            p3 = response.css('div.p3 p::text').extract()

        data['g'] = p1[0]
        data['pts'] = p1[1]
        data['trb'] = p1[2]
        data['ast'] = p1[3]

        data['fg'] = p2[0]
        data['fg3'] = p2[1]
        if data['fg3'] == '-':
            data['fg3'] = 0
        data['ft'] = p2[2]
        data['efg'] = p2[3]

        data['per'] = p3[0]
        data['ws'] = p3[1]

        yield data