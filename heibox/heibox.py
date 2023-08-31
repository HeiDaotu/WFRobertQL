#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: heibox.py
Author: WFRobert
Date: 2023/5/19 10:32
cron: 0 15 6 * * ?
new Env('小黑盒签到脚本');
Description: 小黑盒脚本,实现每日自动完成小黑盒任务
Update: 2023/9/1 更新cron
"""
import base64
import os
import json
import logging
import random
import time
import requests

import notify
import initialize

# 通知内容
message = []


# 小黑盒签到
class XiaoHeiHe:
    def __init__(self, user) -> None:
        self.Xiaoheihe = user['cookie']
        self.imei = user['imei']
        self.heybox_id = user['heybox_id']
        self.version = user['version']
        self.n = self.get_nonce_str()
        self.t = int(time.time())
        # self.u = "/task/sign"

    def get_nonce_str(self, length: int = 32) -> str:
        """
        生成随机字符串
        参数:
            length: 密钥参数
        返回:
            str: 随机字符串
        """
        source = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        result = "".join(random.choice(source) for _ in range(length))
        return result

    def hkey(self, key):
        params = {"urlpath": key, "nonce": self.n, "timestamp": self.t}
        zz = requests.get("http://146.56.234.178:8077/encode", params=params).text
        return zz

    def params(self, key):
        p = {
            "_time": self.t,
            "hkey": self.hkey(key),
            "nonce": self.n,
            "imei": self.imei,
            "heybox_id": self.heybox_id,
            "version": self.version,
            "divice_info": "M2012K11AC",
            "x_app": "heybox",
            "channel": "heybox_xiaomi",
            "os_version": "13",
            "os_type": "Android"
        }
        return p

    def head(self):
        head = {
            "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36 ApiMaxJia/1.0",
            "cookie": self.Xiaoheihe,
            "Referer": "http://api.maxjia.com/"
        }
        return head

    def b64encode(self, data: str) -> str:
        result = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        return str(result)

    def getpost(self):
        req = requests.get(
            url="https://api.xiaoheihe.cn/bbs/app/feeds/news",
            params=self.params("/bbs/app/feeds/news"),
            headers=self.head()
        ).json()['result']['links'][1]['linkid']

        def click(link_id):
            head = self.params("/bbs/app/link/share/click")
            head['h_src'] = self.b64encode('news_feeds_-1')
            head['link_id'] = link_id
            head['index'] = 1
            req = requests.get(url="https://api.xiaoheihe.cn/bbs/app/link/share/click", params=head,
                               headers=self.head()).json()['status']
            if req == "ok":
                logging.info("分享成功")
                msg_req = "分享成功"
                message.append(f"😊分享成功")
            else:
                logging.info("分享失败")
                msg_req = "分享失败"
                message.append(f"😢分享失败")
            return msg_req

        def check():
            head = self.params("/task/shared/")
            head['h_src'] = self.b64encode('news_feeds_-1')
            head['shared_type'] = 'normal'
            req = requests.get(url="https://api.xiaoheihe.cn/task/shared/", params=head, headers=self.head()).json()[
                'status']
            if req == "ok":
                logging.info("检查分享成功")
                msg_req = "检查分享成功"
            else:
                logging.info("检查分享失败")
                msg_req = "检查分享失败"
            return msg_req

        return click(req) + "\n" + check()

    def heibox_sgin(self):
        if self.Xiaoheihe != "":
            try:
                req = requests.get(
                    url="https://api.xiaoheihe.cn/task/sign/",
                    params=self.params("/task/sign/"),
                    headers=self.head()
                ).json()
                fx = self.getpost()
                if req['status'] == "ok":
                    if req['msg'] == "":
                        logging.info("小黑盒:已经签到过了")
                        message.append(f"😢{self.heybox_id},小黑盒:已经签到过了")
                        return fx + "\n已经签到过了"
                    else:
                        logging.info(f"小黑盒:{req['msg']}")
                        message.append(f"😊{self.heybox_id},小黑盒:{req['msg']}")
                        return {fx} + "\n" + req['msg']
                else:
                    logging.info(f"小黑盒:签到失败 - {req['msg']}")
                    message.append(f"😢小黑盒:签到失败 - {req['msg']}")
                    return f"{fx}\n签到失败 - {req['msg']}"
            except Exception as e:
                logging.info(f"小黑盒:出现了错误,错误信息{e}")
                message.append(f"😢小黑盒:出现了错误,错误信息{e}")
                return f"出现了错误,错误信息{e}"
        else:
            logging.info("小黑盒:没有配置cookie")
            message.append(f"😢小黑盒:没有配置cookie")
            return "没有配置cookie"


def main():
    logging.info("第一次会生成heiboxConfig.json文件，请在文件中填写对应的值，将switch改为true才会运行")
    initialize.init()  # 初始化日志系统
    # 判断是否存在文件
    if not os.path.exists('heiboxConfig.json'):
        base = [{"switch": False, "cookie": "用户1cookie", "imei": "用户1imei", "heybox_id": "用户1heybox_id",
                 "version": "1.3.229"},
                {"switch": False, "cookie": "用户2cookie", "imei": "用户2imei", "heybox_id": "用户2heybox_id",
                 "version": "1.3.229"}]
        with open('heiboxConfig.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(base, indent=4, ensure_ascii=False))
    with open('heiboxConfig.json', 'r', encoding="utf-8") as f:
        config = json.load(f)
    num = 0
    for user in config:
        num += 1
        if not user['switch']:
            logging.info(f'😢第{num}个 switch值为False, 不进行任务')
            message.append(f'😢第{num}个 switch值为False, 不进行任务')
            continue
        else:
            body = XiaoHeiHe(user)
            body.heibox_sgin()


if __name__ == '__main__':
    main()
    # 发送通知
    msg = '\n'.join(message)
    notify.send("小黑盒", msg)
