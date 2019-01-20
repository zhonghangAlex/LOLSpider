# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


# 获取账号所在的大区方法，并且进行数据格式化
def get_play_area(value):
    list_area = value.split("/")
    return list_area[1] + "-" + list_area[2]


# 抽取一个字符串中的整型数字
def get_nums_int(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


# 抽取一个字符串中的浮点型数字
def get_nums_float(value):
    match_re = re.match(".*?(\d+)[.](\d+).*", value)
    if match_re:
        nums = float(match_re.group(1))
    else:
        nums = 0.00
    return nums


# 分段获取后半部分
def get_back(value):
    str_no_blank = value.replace(' ', '')
    list_back = str_no_blank.split("：")[1]
    return list_back


# 整型化
def get_int(value):
    return int(value)


# 浮点化
def get_float(value):
    return float(value)


# 获取账号等级
def get_level(value):
    return value.split("级")[0]


# 获取账号的单排段位
def get_rank(value):
    return value.split("级")[1]


def return_value(value):
    return value


class LolItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LolItem(scrapy.Item):
    no_title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    play_area = scrapy.Field(
        input_processor=MapCompose(get_play_area)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    total_times = scrapy.Field(
        input_processor=MapCompose(get_nums_int)
    )
    total_hours = scrapy.Field(
        input_processor=MapCompose(get_nums_int)
    )
    seller_level = scrapy.Field(
        input_processor=MapCompose(get_nums_int)
    )

    phone_reco = scrapy.Field()
    identity_reco = scrapy.Field()

    hour_price = scrapy.Field(
        input_processor=MapCompose(get_nums_float)
    )
    day_price = scrapy.Field(
        input_processor=MapCompose(get_nums_float)
    )
    morning_price = scrapy.Field(
        input_processor=MapCompose(get_nums_float)
    )
    evening_price = scrapy.Field(
        input_processor=MapCompose(get_nums_float)
    )
    ten_price = scrapy.Field(
        input_processor=MapCompose(get_nums_float)
    )
    week_price = scrapy.Field(
        input_processor=MapCompose(get_nums_float)
    )

    deposit = scrapy.Field(
        input_processor=MapCompose(get_back, get_nums_int)
    )
    collect_num = scrapy.Field(
        input_processor=MapCompose(get_nums_int)
    )

    no_name = scrapy.Field(
        input_processor=MapCompose(get_back)
    )
    no_hero = scrapy.Field(
        input_processor=MapCompose(get_back, get_int)
    )
    no_skin = scrapy.Field(
        input_processor=MapCompose(get_back, get_int)
    )
    no_level = scrapy.Field(
        input_processor=MapCompose(get_back, get_level)
    )
    no_rank = scrapy.Field(
        input_processor=MapCompose(get_back, get_rank)
    )
    no_rank_etc = scrapy.Field(
        input_processor=MapCompose(get_back)
    )
    no_time_range = scrapy.Field(
        input_processor=MapCompose(get_back)
    )
    no_if_rank = scrapy.Field(
        input_processor=MapCompose(get_back)
    )
    no_min_time = scrapy.Field(
        input_processor=MapCompose(get_back)
    )
    no_result = scrapy.Field(
        input_processor=MapCompose(get_back)
    )

    no_desc = scrapy.Field()

    # 写入数据库，进行参数设置
    def get_insert_sql(self):
        insert_sql = """
            insert into no_info(no_title, url, url_object_id, play_area, total_times, total_hours,
            seller_level, phone_reco, identity_reco, hour_price, day_price, morning_price, evening_price,
            ten_price, week_price, deposit, collect_num, no_name, no_hero, no_skin, no_level, no_rank,
            no_rank_etc, no_time_range, no_if_rank, no_min_time, no_result, no_desc) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self["no_title"],
            self["url"],
            self["url_object_id"],
            self["play_area"],
            self["total_times"],
            self["total_hours"],
            self["seller_level"],
            self["phone_reco"],
            self["identity_reco"],
            self["hour_price"],
            self["day_price"],
            self["morning_price"],
            self["evening_price"],
            self["ten_price"],
            self["week_price"],
            self["deposit"],
            self["collect_num"],
            self["no_name"],
            self["no_hero"],
            self["no_skin"],
            self["no_level"],
            self["no_rank"],
            self["no_rank_etc"],
            self["no_time_range"],
            self["no_if_rank"],
            self["no_min_time"],
            self["no_result"],
            self["no_desc"],
        )

        # 交给pipline进行处理，此处只要传递参数过去即可
        return insert_sql, params
