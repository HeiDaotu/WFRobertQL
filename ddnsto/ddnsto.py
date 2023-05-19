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


def get_cookies():
    if os.environ.get("DDNSTO_COOKIE"):
        print("🍪已获取并使用Env环境 Cookie")
        return os.environ.get("DDNSTO_COOKIE")
    return None


def select_list(cookie):
    global repose
    print('🍕开始获取csrftoken')
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

    print('🍿开始调用接口地址')
    for i in range(3):
        print(f'😎开始第{i + 1}次调用接口，最多调用3次')
        try:
            try:
                # 关闭SSL验证
                repose = session.post(url, json=body, verify=False, timeout=5)
            except Exception as exc:
                print(f"😒cookie有问题，请使用新的cookie：{exc}")
            text_id = repose.json()["id"]
            session.get(f"{url}{text_id}/", verify=False, timeout=5)
            routers_repose = session.get(f"{routers_url}?limit=5&offset=0", verify=False, timeout=5)
            routers_id = routers_repose.json()["results"][0]['id']

            body_routers = {
                "plan_ids_to_add": [text_id],
                "server": 1
            }
            session.patch(f"{routers_url}{routers_id}/", json=body_routers, verify=False, timeout=5)
            status_code = repose.status_code

            # 判断
            if 201 == status_code:
                print("😊您已成功续期")
                break
            else:
                print("😒您续期失败,这错误可能是来自于ddnsto官方的错误,因此不重复调用了,失败原因为: ", repose.text)
                break
        except Exception as e:
            if e.args[0] == 'id':
                print("😒您续期失败,这错误可能是来自于ddnsto官方的错误,因此不重复调用了")
                break
            else:
                print("😒您续期失败,正在尝试重新续期", e)
                time.sleep(60)
        finally:
            session.close()


# 使用函数封装重复的代码
def print_message(pr_message):
    print(f'🍪{pr_message}')


if __name__ == "__main__":
    # 使用format方法格式化字符串
    print_message('开始获取Cookie')
    # cookie = get_cookies()
    cookie = "ksuser=e7b78477-c932-474a-b602-1a2f0366b151; csrftoken=oscIeEzs3BhuFz1q7A4UGCcUhAbOAZLVfwh1ucVbaCq1AclZW4EmzdGQlJ5WjFoE; sessionid=4w6etq5btpjhnx9ncjb545w8yode7amf; Hm_lvt_5f1bc900ab954d0d1e03eb7f29aba601=1683679274; Hm_lpvt_5f1bc900ab954d0d1e03eb7f29aba601=1683679274"
    print_message('获取Cookie成功')
    if cookie:
        # 使用三元表达式简化条件判断
        message = '开始调用脚本' if select_list(cookie) else '调用脚本失败'
        print_message(message)
    else:
        print_message('cookie为空，请查看您的配置文件。')
