# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from player_data.items import PlayerItem,PlayerDataItem

host = '127.0.0.1'
user = 'root'
passwd = 'zxp12345'
db = 'nba'
port = 3306


class PlayerPipeline(object):

    def open_spider(self,spider):
        self.db_conn = MySQLdb.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()
        self.db_cur.execute("DELETE FROM players")
        self.db_cur.execute("DELETE FROM players_data")
        self.db_conn.commit()

    def close_spider(self,spider):
        self.db_conn.close()

    def process_item(self, item, spider):
        if isinstance(item,PlayerItem):
            self.insert_player(item)
        else:
            self.insert_player_data(item)
        return item

    def insert_player(self,item):
        values = (item['name'],item['position'],item['birthday'])

        sql = 'INSERT INTO players (name,position,birthday) VALUES (%s,%s,%s)'
        self.db_cur.execute(sql,values)
        self.db_conn.commit()

    def insert_player_data(self, item):
        values = (item['name'], item['g'], item['pts'],item['trb'],item['ast'],item['fg'],item['fg3'],item['ft'],item['efg'],item['per'],item['ws'])

        sql = 'INSERT INTO players_data (name,g,pts,trb,ast,fg,fg3,ft,efg,per,ws) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)
        self.db_conn.commit()
