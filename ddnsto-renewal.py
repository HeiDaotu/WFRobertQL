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
        print("已获取并使用Env环境 Cookie")
        Cookies = os.environ.get("DDNSTO_COOKIE")
    return Cookies


def select_list(cookies):
    # 获取令牌
    csrftoken = {}
    for line in cookies.split(';'):
        key, value = line.split('=', 1)
        csrftoken[key] = value
    csrftoken = csrftoken.get(' csrftoken')

    # 获取user_agent
    fake_ua = UserAgent()
    user_agent = fake_ua.random

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
        repose = requests.post(url, body, headers=headers, verify=False, timeout=40)
        status_code = repose.status_code
        if 200 in status_code:
            print("您已成功续期")
        else:
            print("您续期失败,失败原因为")
            print(repose.text)
    except Exception as e:
        print("续期未知错误,错误原因：", e)


if __name__ == "__main__":
    cookies = get_cookies()
    if cookies is not None:
        select_list(cookies)
    else:
        print("cookie为空，请查看您的配置文件。")
