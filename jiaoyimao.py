#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: jiaoyimao.py
Author: WFRobert
Date: 2023/5/24 8:57
cron: 0 35 6 * * ?
new Env('交易猫签到');
Description: 交易猫脚本,实现每日自动签到
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
        if os.environ.get("JIAOYIMAO_COOKIE"):
            cookies = os.environ.get("JIAOYIMAO_COOKIE")
        else:
            logging.info("😢请在环境变量填写JIAOYIMAO_COOKIE的值")
            message.append("😢请在环境变量填写JIAOYIMAO_COOKIE的值")
            sys.exit()
    for idx, cookie in enumerate(cookies.split("&")):
        head = {
            "user-agent": "jym_mobile (Linux; U; Android12; zh_CN; M2012K11AC; Build/SKQ1.220213.001; fca7d8fc-03b5-4fea-97e6-94173844b374; 1080x2400) com.jym.mall/206/JYN_548/7.0.2 AliApp(JYM/7.0.2) UT4Aplus/0.2.29; density/2.7; app_id/23072786;  WindVane/8.5.0; utdid/YH2ygxDifiEDAA6wMV75K10e; umid_token/7+9LGztLOiq8MTWA+l8fZZQW+RjvBE56; oaid/9933af2363237087;",
            "referer": "https://m.jiaoyimao.com/account/integration/center?spm=gcmall.home2022.topshortcut.0",
            "x-csrf-token": "HT-x5YUi3IF7iyVDXY6FBc6g",
            "x-requested-with": "com.jym.mall",
            "cookie": cookie
        }
        try:
            zz = requests.get(url="https://m.jiaoyimao.com/api2/account/integration/signin", headers=head).json()
            if zz['success']:
                rep = requests.get(url="https://m.jiaoyimao.com/api2/account/integration/getMyIntegration",
                                   headers=head).json()
                if rep['stateCode'] == 200:
                    Integral = rep['data']['amountLeft']
                else:
                    Integral = "获取积分失败"

                logging.info(f"交易猫:签到成功 - 现有积分{Integral}")
                message.append(f"😊第{idx}个账户，签到成功 - 现有积分{Integral}")
                return f"签到成功 - 现有积分{Integral}"
            else:

                logging.info(f"交易猫:签到失败 - 已经签到了")
                message.append(f"😢第{idx}个账户，签到失败 - 已经签到了")
                return f"签到失败 - 已经签到了"
        except Exception as e:
            logging.info("交易猫:cookie可能已过期，或出现了错误")
            message.append(f"😢第{idx}个账户，cookie可能已过期，或出现了错误")
            return "cookie可能已过期，或出现了错误"


if __name__ == '__main__':
    # 初始化日志系统
    initialize.init()
    main()
    # 发送通知
    msg = '\n'.join(message)
    notify.send("交易猫", msg)
