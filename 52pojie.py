#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: 52pojie.py
Author: WFRobert
Date: 2023/3/9 15:01
cron: 0 25 6 * * ?
new Env('52pojie自动签到脚本');
Description: 52pojie自动签到,实现每日自动签到52pojie
Update: 2023/9/1 更新cron
"""
import logging
import os
import sys
import urllib.parse
import requests
from bs4 import BeautifulSoup
import initialize

# 初始化日志系统
initialize.init()

# 多cookie使用&分割
logging.info("开始签到")
cookies = ""
if cookies == "":
    if os.environ.get("PJ52_COOKIE"):
        cookies = os.environ.get("PJ52_COOKIE")
    else:
        logging.info("😢请在环境变量填写PJ52_COOKIE的值")
        sys.exit()
n = 1
for cookie in cookies.split("&"):
    url1 = "https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA=="
    url2 = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F'
    url3 = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
    cookie = urllib.parse.unquote(cookie)
    cookie_list = cookie.split(";")
    cookie = ''
    for i in cookie_list:
        key = i.split("=")[0]
        if "htVC_2132_saltkey" in key:
            cookie += "htVC_2132_saltkey=" + urllib.parse.quote(i.split("=")[1]) + "; "
        if "htVC_2132_auth" in key:
            cookie += "htVC_2132_auth=" + urllib.parse.quote(i.split("=")[1]) + ";"
    if not ('htVC_2132_saltkey' in cookie or 'htVC_2132_auth' in cookie):
        initialize.error_message(f"第{n}cookie中未包含htVC_2132_saltkey或htVC_2132_auth字段，请检查cookie")
        sys.exit()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36",
    }
    r = requests.get(url1, headers=headers, allow_redirects=False)
    s_cookie = r.headers['Set-Cookie']
    cookie = cookie + s_cookie
    headers['Cookie'] = cookie
    r = requests.get(url2, headers=headers, allow_redirects=False)
    s_cookie = r.headers['Set-Cookie']
    cookie = cookie + s_cookie
    headers['Cookie'] = cookie
    r = requests.get(url3, headers=headers)
    r_data = BeautifulSoup(r.text, "html.parser")
    jx_data = r_data.find("div", id="messagetext").find("p").text
    if "您需要先登录才能继续本操作" in jx_data:
        initialize.error_message(f"第{n}个账号Cookie 失效\n")
    elif "恭喜" in jx_data:
        initialize.info_message(f"第{n}个账号签到成功\n")
    elif "不是进行中的任务" in jx_data:
        initialize.info_message(f"第{n}个账号今日已签到\n")
    else:
        initialize.error_message(f"第{n}个账号签到失败\n")
    n += 1

initialize.send_notify("吾爱破解")  # 发送通知
