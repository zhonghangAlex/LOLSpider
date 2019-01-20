#!/usr/bin/env python
# encoding: utf-8
'''
@author: ZhonghangAlex
@contact: 715608270@qq.com
@software: pycharm
@file: main.py
@time: 2019/1/20 17:59
@desc:
'''
# 入口文件
# 运行此py文件即可启动爬虫

import sys
import os

from scrapy.cmdline import execute

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "lol"])
