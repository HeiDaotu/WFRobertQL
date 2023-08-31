#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: wangyiyungame.py
Author: WFRobert
Date: 2023/5/24 10:50
cron: 0 45 6 * * ?
new Env('网易云游戏');
Description: 网易云游戏，每日签到获取使用时间和成长值
Update: 2023/9/1 更新cron
"""
import os
import logging
import sys
import requests
import notify
import initialize

# 通知内容
message = []


def main():
    cookies = ""
    if cookies == "":
        if os.environ.get("WANGYIYUNGAME_COOKIE"):
            cookies = os.environ.get("WANGYIYUNGAME_COOKIE")
        else:
            logging.info("😢请在环境变量填写WANGYIYUNGAME_COOKIE的值")
            message.append("😢请在环境变量填写WANGYIYUNGAME_COOKIE的值")
            sys.exit()
    for idx, cookie in enumerate(cookies.split("&")):
        url = 'https://n.cg.163.com/api/v2/sign-today'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
            'Authorization': cookie,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'n.cg.163.com',
            'Origin': 'https://cg.163.com',
            'Referer': 'https://cg.163.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Platform': '0'
        }
        res = requests.post(url=url, headers=header).status_code
        if res == 200:
            logging.info("网易云游戏:签到成功")
            message.append(f"😊第{idx}个账号，签到成功")
            return "签到成功"
        else:
            logging.info("网易云游戏:签到失败或已签到")
            message.append(f"😢第{idx}个账号，签到失败或已签到")
            return "签到失败或已签到"


if __name__ == '__main__':
    # 初始化日志系统
    initialize.init()
    main()
    # 发送通知
    msg = '\n'.join(message)
    notify.send("网易云游戏", msg)
