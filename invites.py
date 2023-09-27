#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: invites.py
Author: WFRobert
Date: 2023/8/30 15:39
cron: 0 0 6 * * ?
new Env('邀玩（药丸）自动签到');
Description: 邀玩（药丸）自动签到
Update: 2023/9/1 更新cron
"""
import os
import sys
from bs4 import BeautifulSoup
import json
import requests
import logging
import initialize


def sign_in(user_session):
    user_id = user_session['userId']  # 获取"userId"数据
    csrf_token = user_session['csrfToken']  # 获取"csrfToken"数据
    if user_id is None:
        initialize.error_message("获取不到用户id，可能是cookie问题，请更新cookie")
        return None
    initialize.info_message(f"用户id：{user_id} 开始签到")

    url = f"https://invites.fun/api/users/{user_id}"

    headers = {
        "Host": "invites.fun",
        "Connection": "keep-alive",
        "Content-Length": "98",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        "X-CSRF-Token": csrf_token,
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "X-HTTP-Method-Override": "PATCH",
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://invites.fun",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://invites.fun/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookie
    }

    data = {
        "data": {
            "type": "users",
            "attributes": {
                "canCheckin": False,
                "totalContinuousCheckIn": 1
            },
            "id": user_id
        }
    }

    response = requests.post(url, headers=headers, json=data)
    status_code = response.status_code
    if 200 == status_code:
        res_parsed_data = json.loads(response.text)  # 将返回值JSON字符串解析为Python对象
        attributes = res_parsed_data["data"]["attributes"]
        username = attributes["username"]
        total_continuous_check_in = attributes["totalContinuousCheckIn"]
        initialize.info_message(f"用户名字：{username} 签到成功，已经签到了:{total_continuous_check_in} 天了")


def get_user_id(user_cookie):
    url = 'https://invites.fun/'  # url地址
    # 请求头
    headers = {
        'Host': 'invites.fun',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': user_cookie
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    soup_data = soup.find('script', attrs={'id': 'flarum-json-payload'}).text
    parsed_data = json.loads(soup_data)  # 将JSON字符串解析为Python对象
    session_data = parsed_data["session"]  # 获取"session"数据
    return session_data


if __name__ == "__main__":
    initialize.init()  # 日志格式化输出，不加  ql无法打出日志
    initialize.info_message("开始获取Cookie\n")
    if os.environ.get("INVITES_COOKIE"):
        cookies = os.environ.get("INVITES_COOKIE")
    else:
        initialize.error_message("在环境变量填写INVITES_COOKIE的值")
        sys.exit()  # 未获取到cookie，退出系统
    for cookie in cookies.split("&"):
        logging.info("🙂开始获取用户id")
        session = get_user_id(cookie)  # 获取用户session
        if session is not None:
            sign_in(session)
        else:
            initialize.error_message("获取不到用户id，可能是cookie问题，请更新cookie")
        logging.info('\n')
        initialize.message('\n')

    # 发送通知
    initialize.send_notify("邀玩（药丸）")
