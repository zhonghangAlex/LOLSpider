#!/usr/bin/env python
# encoding: utf-8
'''
@author: ZhonghangAlex
@contact: 715608270@qq.com
@software: pycharm
@file: common.py
@time: 2019/1/20 18:04
@desc:
'''
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5("http://www.zhonghangalex.com".encode("utf-8")))