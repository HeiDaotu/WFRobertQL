#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: enshan.py
Author: WFRobert
Date: 2023/9/1 1:09
cron: 0 50 6 * * ?
new Env('恩山论坛模拟登录脚本');
Description: 恩山论坛模拟登录,每日登录获得+1恩山币
Update: 2023/9/1 更新cron
"""
import datetime
import os
import sys
import urllib.parse

import initialize
import requests
from bs4 import BeautifulSoup


def user_data(cookie):
    """
    获取用户信息

    :param cookie:
    :return:
    """
    url = 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&op=base'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        'Referer': 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1',
        'Cookie': cookie
    }
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code == 200:
        soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
        user_name = soup.find('a', attrs={'title': '访问我的空间'}).text  # 用户名
        points = soup.find('a', attrs={'id': 'extcreditmenu'}).text  # 目前积分
        user_group = soup.find('a', attrs={'id': 'g_upmine'}).text  # 用户组
        initialize.info_message(f"模拟登录成功---{user_name}---{points}---{user_group}")
    else:
        initialize.error_message(f"账号可能cookie过期了")


def sign_in(number, cookie):
    """
    开启模拟登录

    :param number:
    :param cookie:
    :return:
    """
    cookie = urllib.parse.unquote(cookie)
    cookie_list = cookie.split(";")
    cookie = ''
    for i in cookie_list:
        key = i.split("=")[0]
        if "TWcq_2132_saltkey" in key:
            cookie += "TWcq_2132_saltkey=" + urllib.parse.quote(i.split("=")[1]) + "; "
        if "TWcq_2132_auth" in key:
            cookie += "TWcq_2132_auth=" + urllib.parse.quote(i.split("=")[1]) + ";"
    if not ('TWcq_2132_saltkey' in cookie or 'TWcq_2132_auth' in cookie):
        initialize.error_message(f"第{number}cookie中未包含TWcq_2132_saltkey或TWcq_2132_auth字段，请检查cookie")
        sys.exit()
    url = "https://www.right.com.cn/forum/home.php?mod=spacecp&ac=credit&op=log&suboperation=creditrulelog"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.right.com.cn",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.find("table", summary="积分获得历史").find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) == 0:
                continue
            if tds[0].text == "每天登录" and tds[5].text[:10] == datetime.datetime.now().strftime("%Y-%m-%d"):
                initialize.info_message("模拟登录成功")
                user_data(cookie)  # 获取用户信息
                break
        else:
            initialize.error_message("模拟登录失败")
    else:
        initialize.error_message("账号可能cookie过期")


def main():
    """
    主方法，开始模拟登录

    :return:
    """
    initialize.info_message("开始获取Cookie\n")
    if os.environ.get("ENSHAN_COOKIE"):
        cookies = os.environ.get("ENSHAN_COOKIE")
    else:
        initialize.error_message("请在环境变量填写ENSHAN_COOKIE的值")
        sys.exit()  # 未获取到cookie，退出系统
    for number, cookie in enumerate(cookies.split("&")):
        initialize.info_message(f"开始执行第{number + 1}个账号")
        sign_in(number + 1, cookie)  # 模拟登录


if __name__ == '__main__':
    initialize.init()  # 初始化日志
    main()  # 主方法
    initialize.send_notify("恩山论坛")  # 发送消息
