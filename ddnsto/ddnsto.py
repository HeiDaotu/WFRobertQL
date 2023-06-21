#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: ddnsto.py
Author: WFRobert
Date: 2023/2/16 10:01
cron: 19 47 7 1/6 * ?
new Env('ddnsto自动续费免费7天的脚本');
Description: 这是ddnsto自动续费免费7天的脚本,默认每过6天自动续费一次
Update: 2023/2/16 更新cron
"""
import os
import time
import uuid
import requests
import logging

import notify
from init_logger import init_logger

# 通知内容
message = []


def get_cookies():
    if os.environ.get("DDNSTO_COOKIE"):
        logging.info("🍪已获取并使用Env环境 Cookie")
        return os.environ.get("DDNSTO_COOKIE")
    return None


def select_list(cookie):
    global repose
    logging.info('🍕开始获取csrftoken')
    # 获取令牌
    csrftoken = {}
    for line in cookie.split(';'):
        key, value = line.split('=', 1)
        csrftoken[key] = value
    csrftoken = csrftoken.get(' csrftoken')
    if csrftoken is not None:
        print_message("csrftoken获取成功")

    # 获取user_agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'

    # url地址
    url = 'https://www.ddnsto.com/api/user/product/orders/'
    routers_url = 'https://www.ddnsto.com/api/user/routers/'
    body = {
        "product_id": 2,
        "uuid_from_client": ''.join(uuid.uuid1().__str__().split('-'))
    }

    # 创建会话对象
    session = requests.Session()
    # 设置通用的请求头
    session.headers.update({
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'User-Agent': user_agent,
        'Cookie': cookie,
        'Content-Type': 'application/json',
        'Referer': 'https://www.ddnsto.com/app/',
        'X-CSRFToken': csrftoken,
        'Connection': 'keep-alive',
        'Host': 'www.ddnsto.com'
    })

    logging.info('🍿开始调用接口地址')
    for i in range(3):
        logging.info(f'😎开始第{i + 1}次调用接口，最多调用3次')
        try:
            try:
                # 关闭SSL验证
                repose = session.post(url, json=body, verify=False, timeout=5)
            except Exception as exc:
                logging.error(f"😒cookie有问题，请使用新的cookie：{exc}")
            # 延迟2s
            time.sleep(2)
            text_id = repose.json()["id"]
            session.get(f"{url}{text_id}/", verify=False, timeout=5)
            # 延迟2s
            time.sleep(2)
            routers_repose = session.get(f"{routers_url}?limit=5&offset=0", verify=False, timeout=5)
            # 延迟2s
            time.sleep(2)
            routers_id = routers_repose.json()["results"][0]['id']

            body_routers = {
                "plan_ids_to_add": [text_id],
                "server": 1
            }
            # 延迟2s
            time.sleep(2)
            session.patch(f"{routers_url}{routers_id}/", json=body_routers, verify=False, timeout=5)
            status_code = repose.status_code

            # 判断
            if 201 == status_code:
                logging.info("😊您已成功续期")
                message.append("😊您已成功续期")
                return status_code
            else:
                logging.error("😒您续期失败,这错误可能是来自于ddnsto官方的错误,因此不重复调用了,失败原因为: ",
                              repose.text)
                message.append(
                    f"😒您续期失败,这错误可能是来自于ddnsto官方的错误,因此不重复调用了,失败原因为: {repose.text}")
                return status_code
        except Exception as e:
            if e.args[0] == 'id':
                logging.error("😒您续期失败,这错误可能是来自于ddnsto官方的错误,因此不重复调用了")
                message.append("😒您续期失败,这错误可能是来自于ddnsto官方的错误,因此不重复调用了")
            else:
                logging.error("😒您续期失败,请更换cookie重试,正在尝试重新续期", e)
                message.append(f"😒您续期失败,请更换cookie重试,正在尝试重新续期{e}")
                time.sleep(10)
                continue
        finally:
            session.close()


# 使用函数封装重复的代码
def print_message(re_message):
    logging.info(f'🍪{re_message}')


if __name__ == "__main__":
    # 日志格式化输出，不加  ql无法打出日志
    init_logger()
    # 使用format方法格式化字符串
    print_message('开始获取Cookie')
    cookies = get_cookies()
    print_message('获取Cookie成功')

    cookie = cookies.split(
        '&')
    for index, key in enumerate(cookie):
        logging.info("😊开始处理第" + str(index + 1) + "个用户")
        if key:
            status_code = select_list(key)
            if 201 == status_code:
                message.append(f'😊第{index + 1}个用户调用脚本成功')
            else:
                message.append(f'😢第{index + 1}个用户调用脚本失败')
        else:
            print_message('cookie为空，请查看您的配置文件。')
            message.append('cookie为空，请查看您的配置文件。')
        logging.info(f'\n')
        message.append(f'\n')

    # 发送通知
    msg = '\n'.join(message)
    notify.send("ddnsto", msg)
