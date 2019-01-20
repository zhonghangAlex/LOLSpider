#!/usr/bin/env python
# encoding: utf-8
'''
@author: ZhonghangAlex
@contact: 715608270@qq.com
@software: pycharm
@file: crawl_xici.py
@time: 2019/1/20 18:31
@desc:
'''
# 此文件是用来爬取西刺网站的高匿代理，用来随机更换request的IP地址，防止网站的反爬措施
# 同时将西刺的高匿IP存储到数据库中，可以提供让爬虫随机获取IP的方法

import requests
from scrapy.selector import Selector
import pymysql

# 此处链接数据库，按需更改即可
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="woaini123", db="lol_no_info", charset="utf8")
cursor = conn.cursor()


# 爬取西刺的免费ip代理
def crawl_ips():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(1568):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            try:
                cursor.execute(
                    "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
                        ip_info[0], ip_info[1], ip_info[3]
                    )
                )
            except Exception as e:
                print(e)

            conn.commit()


# 从数据库中删除无效的ip
class GetIP(object):
    def delete_ip(self, ip):
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    # 判断ip是否可用
    def judge_ip(self, ip, port):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=10)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    # 从数据库中随机获取一个可用的ip
    def get_random_ip(self):

        random_sql = """
              SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    # 第一步：调用下面的方法先进行数据爬取，然后将IP存储到数据库中
    # crawl_ips()

    # 第二步：在spider的主文件中调用随机选择的方法，进行IP的获取
    get_ip = GetIP()
    get_ip.get_random_ip()