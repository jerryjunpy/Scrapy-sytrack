#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import re


class Orderno:
    def __init__(self):
        self.db = pymysql.connect(host='', user='', password='', port=3306, db='',
                                  charset='utf8')
        self.cursor = self.db.cursor()

        self.db_1 = pymysql.connect(host='', user='', password='', port=3306, db='',
                                    charset='utf8')

        self.cursor_1 = self.db_1.cursor()

    def repleni_orderno(self):
        """
        获取shippingorderno单列表
        :return:
        """
        sql = "SELECT c.shippingorderno from customerorder c LEFT JOIN allocationproductvoucher t ON c.customerorderno" \
              " = t.customerorderno where (c.shippingforwardermethod ='SYBAM' or c.shippingforwardermethod = " \
              "'SYBRAM' or c.shippingforwardermethod = 'SYBRPL' or c.shippingforwardermethod ='SYBPL') " \
              "and SUBDATE(NOW(), INTERVAL 7 DAY) <= t.delivertime " \
              "and c.shippingorderno is not null ORDER BY c.paidtime;"
        cursor = self.cursor
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            ls = []
            while result:
                ls.append(result)
                result = cursor.fetchone()
            syb_orderno = []
            for m in range(len(ls)):
                syb_orderno.append(ls[m][0])
            
            self.db.close()

            pms = set(syb_orderno)  # 设置集合去重

            sql_1 = "SELECT DISTINCT tracking_number from logistics_info WHERE (logistics_method='SYBAM' or " \
                    "logistics_method = 'SYBRAM' or logistics_method ='SYBRPL' or logistics_method ='SYBPL') and " \
                    "tracking_number not IN (SELECT DISTINCT tracking_number from logistics_info where " \
                    "(logistics_method='SYBAM' or logistics_method = 'SYBRAM' or logistics_method ='SYBRPL' or " \
                    "logistics_method ='SYBPL') and (tracking_status = 2 OR tracking_status = 3));"
            self.cursor_1.execute(sql_1)

            result_1 = self.cursor_1.fetchall()

            for a in result_1:
                for b in a:
                    pms.add(b)     # 将未完成妥投的加进去

            sql_2 = "SELECT DISTINCT tracking_number from logistics_info where (logistics_method='SYBAM' or " \
                    "logistics_method = 'SYBRAM' or logistics_method ='SYBRPL' or logistics_method ='SYBPL')" \
                    "and (tracking_status = 2 OR tracking_status = 3);"

            self.cursor_1.execute(sql_2)

            result_2 = self.cursor_1.fetchall()

            for a in result_2:
                for b in a:
                    pms.discard(b)   # 将已完成妥投的和不存在的删除
            return pms

        except:

            pass
