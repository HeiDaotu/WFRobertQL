#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/16 10:01
# @Author  : WFRobert
# @File    : ddnsto-renewal.py
# 这是ddnsto自动续费免费7天的脚本

import json
import os
import uuid

import requests
from fake_useragent import UserAgent


def get_cookies():
    Cookies = []
    if os.environ.get("DDNSTO_COOKIE"):
        print("🍪已获取并使用Env环境 Cookie")
        Cookies = os.environ.get("DDNSTO_COOKIE")
    return Cookies


def select_list(cookies):
    # 获取令牌
    print('🍕开始获取csrftoken')
    csrftoken = {}
    for line in cookies.split(';'):
        key, value = line.split('=', 1)
        csrftoken[key] = value
    csrftoken = csrftoken.get(' csrftoken')
    if csrftoken is not None:
        print("🍕csrftoken获取成功")

    # 获取user_agent
    print('🍟开始获取获取user_agent')
    try:
        fake_ua = UserAgent()
        user_agent = fake_ua.random
        print('🍟获取user_agent成功')
    except Exception as e:
        print('🍟获取user_agent失败了，失败原因是：', e.__str__())
        print('🍟由于user_agent获取失败，因此自定义一个user_agent')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'

    # url地址
    url = 'https://www.ddnsto.com/api/user/product/orders/'
    body = json.dumps({
        "product_id": 2,
        "uuid_from_client": ''.join(uuid.uuid1().__str__().split('-'))
    })

    # 请求头
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'User-Agent': user_agent,
        'Cookie': cookies,
        'Content-Length': '70',
        'Content-Type': 'application/json',
        'Referer': 'https://www.ddnsto.com/app/',
        'X-CSRFToken': csrftoken,
        'Connection': 'keep-alive',
        'Host': 'www.ddnsto.com'
    }

    try:
        # 关闭SSL验证
        print('🍿开始调用接口地址')
        repose = requests.post(url, body, headers=headers, verify=False, timeout=40)
        status_code = repose.status_code
        if 200 is status_code:
            print("您已成功续期")
        else:
            print("您续期失败,失败原因为")
            print(repose.text)
    except Exception as e:
        print("续期未知错误,错误原因：", e)


if __name__ == "__main__":
    print('🍪开始获取Cookies')
    cookies = get_cookies()
    print('🍪获取Cookies成功')
    if cookies is not None:
        print('🍕开始调用脚本')
        select_list(cookies)
    else:
        print("cookie为空，请查看您的配置文件。")
