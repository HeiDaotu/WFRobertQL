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
    # cookies = get_cookies()
    # cookies = '__kp=b900a170-ef81-11ee-89aa-35cd9652859f;__kps=AAQLGV1MmJoU7Ml2Vhwgkz7K;__ktd=aDkqx6gnKbhlTE098t+khQ==;__uid=AAQLGV1MmJoU7Ml2Vhwgkz7K;tfstk=frQpzafrOR2HyhUK0gZG44fO1dNgmwCEW95jrLvnVOBOiOJkVHAHy36BIwxkRJ8JFd6rx2vk-aBOQOWht_bRb4CVawVerW8FTU87n-4Dy65ezCWWjzQp5CO51Q9WN3lw5MY7n-4g8yFe2Usl9cFBK19wwQ9WOTG_6QOWP2tSRcM6QQtuazgqaPuOBZAQ07Lc2OkBtBKpe4voyaQsohpfOd37hNdKPK1BB4gWLQaWq1C3pq5M8KBvi94sJtCCcTsfCP3pbM1Oyn7rd5TWVGjDvGeIydbhXNLhR8oVs1pBDFjgbJxkJ9I23HZaQTC9KT_pfvIyGZbYtJHDHQmL65nr4HOantv5rqJNc_d9n5An40-TbCp065nr4HOw6KViK0oyXl5..;__puus=a99d8fbba837266e6e67e98a4991f893AAQLf3M6ymccLmPMVCsha0vzLFfynu6AARAJZD0OC2MNFVm/GjhuXJvDkDKZerM2HIbT7UcAcRSPNpmRg+RgIPpCikME9IjDe/Hcp5MfHkiHbBmHWCejYNh9YNKluKO6IY7ciU4J7TUkmoj9r9oBli9hbfr2b98weEHYp6LceW13a+trn8SE1ofSMeF+Bvsy07l/QQ8H6vtbY2mq6cWDvssf;'
    cookies = '_UP_A4A_11_=wb9641b44041409d9b4516735ffc6ace; _UP_D_=pc; _UP_30C_6A_=st9646201bb9oe8oexf0wdmyu18c5gu0; _UP_TS_=sg119f22a588b62b4e8fda48715cb42a8be; _UP_E37_B7_=sg119f22a588b62b4e8fda48715cb42a8be; _UP_TG_=st9646201bb9oe8oexf0wdmyu18c5gu0; _UP_335_2B_=1; __pus=be7ff2425e37c120e7f69bfe26b145cbAARPH2aUr3nt33yc4GEb/ZUFsLNjV1uh7Y+xEAJe+er4lDwsKO6pfjlxzl7TcIvSX/Vnk8PSiVZlbhzafS0+E75W; __kp=b900a170-ef81-11ee-89aa-35cd9652859f; __kps=AAQLGV1MmJoU7Ml2Vhwgkz7K; __ktd=aDkqx6gnKbhlTE098t+khQ==; __uid=AAQLGV1MmJoU7Ml2Vhwgkz7K; tfstk=frQpzafrOR2HyhUK0gZG44fO1dNgmwCEW95jrLvnVOBOiOJkVHAHy36BIwxkRJ8JFd6rx2vk-aBOQOWht_bRb4CVawVerW8FTU87n-4Dy65ezCWWjzQp5CO51Q9WN3lw5MY7n-4g8yFe2Usl9cFBK19wwQ9WOTG_6QOWP2tSRcM6QQtuazgqaPuOBZAQ07Lc2OkBtBKpe4voyaQsohpfOd37hNdKPK1BB4gWLQaWq1C3pq5M8KBvi94sJtCCcTsfCP3pbM1Oyn7rd5TWVGjDvGeIydbhXNLhR8oVs1pBDFjgbJxkJ9I23HZaQTC9KT_pfvIyGZbYtJHDHQmL65nr4HOantv5rqJNc_d9n5An40-TbCp065nr4HOw6KViK0oyXl5..; __puus=0995550892dd0a45ff32b7c9fa2c6a89AAQLf3M6ymccLmPMVCsha0vzid0GDB6HUlLS9UAWKHNI/ryQTq7T2N0LCMO6yfKLpE5E/jFbT0TbgQst4/FxsO1+c0oYmGetBRJqsLtOi5N92sfjpzSDAvgqljCpbnmnE2nn/IeT3ZtqlUQxVFzHttKM7NmSeDVo+fNFcceI4mjaoQHP2eLFPi2jQ1vrAim3vAG39cS6exrjk5UPnFjNInDC'
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
