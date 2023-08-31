#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: kxdao.py
Author: WFRobert
Date: 2023/9/1 2:49
cron: 0 55 6 * * ?
new Env('科学刀论坛打卡签到');
Description: 科学刀论坛打卡签到
Update: 2023/9/1 更新cron
"""
import os
import sys
import initialize
import requests
from bs4 import BeautifulSoup
import re


def main():
    initialize.info_message("开始获取Cookie\n")
    if os.environ.get("KXDAO_COOKIE"):
        cookies = os.environ.get("KXDAO_COOKIE")
    else:
        initialize.error_message("请在环境变量填写KXDAO_COOKIE的值")
        sys.exit()  # 未获取到cookie，退出系统

    for number, cookie in enumerate(cookies.split("&")):
        initialize.info_message(f"开始执行第{number + 1}个账号")
        url = "https://www.kxdao.net/plugin.php?id=dsu_amupper&ppersubmit=true&formhash=689dbd52&infloat=yes&handlekey=dsu_amupper&inajax=1&ajaxtarget=fwin_content_dsu_amupper"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
            "Cookie": cookie
        }
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
            pattern = r"if\(typeof errorhandle_dsu_amupper=='function'\) {errorhandle_dsu_amupper\('([^']*)', {}\);}"
            match = re.search(pattern, soup.text)  # 获取签到信息
            if match:
                value = match.group(1)
                initialize.info_message(f"第{number + 1}个账户:{value}")
            else:
                print("未找到目标值")
                initialize.error_message(f"第{number + 1}个账号可能cookie过期了")
        else:
            initialize.error_message(f"第{number + 1}个账号可能cookie过期了")


if __name__ == '__main__':
    initialize.init()  # 初始化日志
    main()  # 主方法
    initialize.send_notify("科学刀论坛")  # 发送消息
