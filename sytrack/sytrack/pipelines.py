# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
import time


class SytrackPipeline(object):

    def __init__(self):

        self.db = pymysql.connect(host='', user='', password='', port=3306, db='',
                                    charset='utf8')
        self.cursor = self.db.cursor()

        self.db_1 = pymysql.connect(host='', user='', password='', port=3306, db='',
                               charset='utf8')
        self.cursor_1 = self.db_1.cursor()

    def process_item(self, item, spider):

        if item['j'] != None:
            j = item['j']
            tracking_number = j['data'][0]['orderNo']

            if j['data'][0]['displayStatus'] == 4:  # 已签收 取第二条为上网时间
                try:
                    for i in j['data'][0]['result']['origin']['items'][-1:]:  # 妥投信息
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date, tracking_status='2')

                    for i in j['data'][0]['result']['origin']['items'][1:2]:  # 上网时间
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date, tracking_status='1')

                    for i in j['data'][0]['result']['origin']['items'][2:-1]:  # 中间数据
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date)

                except:
                    for i in j['data'][0]['result']['transfer']['items'][-1:]:
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date, tracking_status='2')

                    for i in j['data'][0]['result']['transfer']['items'][1:2]:
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date, tracking_status='1')

                    for i in j['data'][0]['result']['transfer']['items'][2:-1]:
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date)

            elif j['data'][0]['displayStatus'] != 4:  # 未妥投 取第一条为上网时间
                try:
                    for i in j['data'][0]['result']['origin']['items'][1:2]:  # 上网时间
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date, tracking_status='1')

                    for i in j['data'][0]['result']['origin']['items'][2:]:  # 后面的数据
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date)
                except:
                    for i in j['data'][0]['result']['transfer']['items'][1:2]:
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date, tracking_status='1')

                    for i in j['data'][0]['result']['transfer']['items'][2:]:
                        info_content = i['content']
                        time_stamp = str(i['createTime'])[0:10]
                        time_array = time.localtime(int(time_stamp))
                        info_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                        self.process_save(tracking_number, info_content, info_date)

        else:

            tracking_number = item['tracking_number']
            info_content = '无法识别的物流单号'
            info_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.process_save(tracking_number, info_content, info_date, tracking_status='3')

    def process_save(self, tracking_number, info_content, info_date, tracking_status=''):

        creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql_1 = "SELECT customerorderno pmsorder, ebayorderid salechannelorderid, shippingforwardermethod, salechannel " \
                "FROM customerorder where shippingorderno ='{}';".format(tracking_number)
        self.cursor_1.execute(sql_1)
        result = self.cursor_1.fetchone()

        pms_order_id = result[0]
        sale_channel_order_id = result[1]
        logistics_method = result[2]
        sale_channel = result[3]

        if tracking_status:
            data = {
                'tracking_number': tracking_number,
                'info_content': info_content,
                'creation_date': creation_date,
                'info_date': info_date,
                'tracking_status': tracking_status,
                'pms_order_id': pms_order_id,
                'sale_channel_order_id': sale_channel_order_id,
                'logistics_method': logistics_method,
                'sale_channel': sale_channel,
            }
        else:
            data = {
                'tracking_number': tracking_number,
                'info_content': info_content,
                'creation_date': creation_date,
                'info_date': info_date,
                'pms_order_id': pms_order_id,
                'sale_channel_order_id': sale_channel_order_id,
                'logistics_method': logistics_method,
                'sale_channel': sale_channel,
            }
        table = 'logistics_info'

        keys = ', '.join(data.keys())

        values = ', '.join(['%s'] * len(data))

        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)

        # 已存在的数据不再存入
        sql_2 = "select * from logistics_info WHERE tracking_number='{}' and info_content='{}' and info_date='{}';".format(tracking_number, info_content, info_date)

        self.cursor.execute(sql_2)

        isExists = self.cursor.rowcount

        if not isExists:
            try:
                self.cursor.execute(sql, tuple(data.values()))
                print('%s:%s save successful' % (tracking_number, info_content))
                self.db.commit()
            except:
                print('Failed')
                self.db.rollback()
        else:
            print('%s:%s 已经存在' % (tracking_number, info_content))

