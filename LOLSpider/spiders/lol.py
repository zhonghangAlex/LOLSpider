# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from LOLSpider.utils.common import get_md5
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from LOLSpider.items import LolItem, LolItemLoader


class LolSpider(scrapy.Spider):
    name = 'lol'
    # allowed_domains = ['www.zuhaowan.com']
    start_urls = ['https://www.zuhaowan.com/zuhao-17']

    headers = {
        "HOST": "www.baidu.com",
        "Referer": "https://www.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/64.0"
    }

    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        web_nodes = response.css("#AccountList tr td:nth-child(1) a")
        for web_node in web_nodes:
            image_url = web_node.css("img::attr(src)").extract_first("")
            web_url = web_node.css("::attr(href)").extract_first("")
            title = web_node.css("::attr(title)").extract_first("")
            yield Request(url=parse.urljoin(response.url, web_url), meta={"front_image_url": image_url, "no_title": title}, callback=self.parse_detail)

        next_url = response.css(".goods_wrap .Main_left_bottom .od_page .pages .next::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        lolno_item = LolItem()

        front_image_url = response.meta.get("front_image_url", "")
        no_title = response.meta.get("no_title", "")
        item_loader = LolItemLoader(item=LolItem(), response=response)

        item_loader.add_value("no_title", no_title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("play_area", ".hm_right .title_a p::text")
        item_loader.add_css("total_times", ".hm_right .p_txt font:nth-child(1)::text")
        item_loader.add_css("total_hours", ".hm_right .p_txt font:nth-child(2)::text")
        item_loader.add_css("seller_level", ".hm_right .title_b .u_txt1 img::attr(alt)")

        item_loader.add_css("phone_reco", ".hm_right .title_b .d_txt1 span::text")
        item_loader.add_css("identity_reco", ".hm_right .title_b .d_txt1 span::text")

        item_loader.add_css("hour_price", ".lib_Menubox1 ul li:nth-child(1) .txt_li2::text")
        item_loader.add_css("day_price", ".lib_Menubox1 ul li:nth-child(2) .txt_li2::text")
        item_loader.add_css("morning_price", ".lib_Menubox1 ul li:nth-child(3) .txt_li2::text")
        item_loader.add_css("evening_price", ".lib_Menubox1 ul li:nth-child(4) .txt_li2::text")
        item_loader.add_css("ten_price", ".lib_Menubox1 ul li:nth-child(5) .txt_li2::text")
        item_loader.add_css("week_price", ".lib_Menubox1 ul li:nth-child(6) .txt_li2::text")

        item_loader.add_css("deposit", ".zuhao_right .lib_Contentbox ul li:nth-child(3) ul li:nth-child(3)::text")
        item_loader.add_css("collect_num", ".hm_left div:nth-child(5) span:nth-child(2) i::text")

        item_loader.add_css("no_name", ".zuhao_right .lib_Contentbox ul li:nth-child(1) ul li:nth-child(1)::text")
        item_loader.add_css("no_hero", ".zuhao_right .lib_Contentbox ul li:nth-child(1) ul li:nth-child(2)::text")
        item_loader.add_css("no_skin", ".zuhao_right .lib_Contentbox ul li:nth-child(1) ul li:nth-child(3)::text")
        item_loader.add_css("no_level", ".zuhao_right .lib_Contentbox ul li:nth-child(2) ul li:nth-child(1)::text")
        item_loader.add_css("no_rank", ".zuhao_right .lib_Contentbox ul li:nth-child(2) ul li:nth-child(1)::text")
        item_loader.add_css("no_rank_etc", ".zuhao_right .lib_Contentbox ul li:nth-child(3) ul li:nth-child(1)::text")
        item_loader.add_css("no_time_range", ".zuhao_right .lib_Contentbox ul li:nth-child(3) ul li:nth-child(2)::text")
        item_loader.add_css("no_if_rank", ".zuhao_right .lib_Contentbox ul li:nth-child(4) ul li:nth-child(1)::text")
        item_loader.add_css("no_min_time", ".zuhao_right .lib_Contentbox ul li:nth-child(4) ul li:nth-child(2)::text")
        item_loader.add_css("no_result", ".zuhao_right .lib_Contentbox ul li:nth-child(4) ul li:nth-child(3)::text")

        item_loader.add_css("no_desc", ".miaoshu::text")

        lolno_item = item_loader.load_item()
        yield lolno_item
