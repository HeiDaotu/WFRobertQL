#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: kuakepan.py
Author: WFRobert
Date: 2024/4/1 1:13
cron: 0 28 6 * * ?
new Env('夸克盘每日签到');
Description: 每日自动签到夸克网盘，领取永久免费空间容量
Update: 2024/4/1 立项
"""
import os
import requests
import logging

import initialize

# 通知内容
message = []


def get_cookies():
    if os.environ.get("KUAKE_COOKIE"):
        logging.info("🍪已获取夸克网盘Cookie")
        return os.environ.get("KUAKE_COOKIE")
    return None


def kuake_login(cookie):
    # url地址
    url = 'https://pan.quark.cn/account/info'

    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "application/json",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36",
    }

    logging.info('🍿开始登录账号')
    try:
        status_code = 201
        repose = requests.get(url=url, headers=headers)

        nickname = repose.json()['data']['nickname']
        logging.info(f'账户: {nickname} 登录成功')

        # 查看当前签到状态，如果签到过不再执行。
        logging.info('开始获取签到状态')
        stateUrl = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info?pr=ucpro&fr=pc&uc_param_str="
        sign_repose = requests.get(url=stateUrl, headers=headers)
        sign_cap_sign = sign_repose.json()['data']['cap_sign']
        is_sign = sign_cap_sign['sign_daily']
        if is_sign:
            number = sign_cap_sign['sign_daily_reward'] / 1024 / 1024
            logging.info(f'今日已签到获取{number}MB')
        else:
            # 执行签到
            signUrl = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign?pr=ucpro&fr=pc&uc_param_str=";
            body = {
                "sign_cyclic": True
            }
            sign_repose = requests.post(url=signUrl, headers=headers, json=body)
            # number = sign_repose.json()['data']['sign_daily_reward'] / 2048
            logging.info(f"签到成功!")
    except Exception as exc:
        logging.error(f"😒cookie有问题，请使用新的cookie：{exc}")
        status_code = -1
    return status_code


if __name__ == "__main__":
    # 日志格式化输出，不加  ql无法打出日志
    initialize.init()
    # 使用format方法格式化字符串
    logging.info(f'🍪开始获取Cookie')
    cookies = get_cookies()
    cookie = cookies.split(
        '&')
    for index, key in enumerate(cookie):
        initialize.info_message("开始处理第" + str(index + 1) + "个用户")
        if key:
            try:
                status_code = kuake_login(key)
                if 201 == status_code:
                    initialize.info_message(f'第{index + 1}个用户调用脚本成功')
                else:
                    initialize.error_message(f'第{index + 1}个用户调用脚本失败')
            except Exception as exc:
                initialize.error_message(f'第{index + 1}个用户调用脚本失败')
        else:
            initialize.error_message("cookie为空，请查看您的配置文件。")
        logging.info(f'\n')
        message.append(f'\n')

    # 发送通知
    initialize.send_notify("夸克网盘")
