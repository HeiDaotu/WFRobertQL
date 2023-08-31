#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: haoyoukuaibao.py
Author: WFRobert
Date: 2023/5/24 9:27
cron: 0 30 6 * * ?
new Env('好游快报');
Description: 好游快报脚本，每日爆米花浇水
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
    Url = 'https://huodong3.3839.com/n/hykb/grow/ajax.php'
    head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; Meizu S6 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36Androidkb/1.5.5.305(android;Meizu S6;7.0;720x1374;4G);@4399_sykb_android_activity@",
        "Origin": "https://huodong3.3839.com",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://huodong3.3839.com/n/hykb/grow/index.php",
    }
    cookies = ""
    if cookies == "":
        if os.environ.get("HAOYOUKUAIBAO_COOKIE"):
            cookies = os.environ.get("HAOYOUKUAIBAO_COOKIE")
        else:
            logging.info("😢请在环境变量填写HAOYOUKUAIBAO_COOKIE的值")
            message.append("😢请在环境变量填写HAOYOUKUAIBAO_COOKIE的值")
            sys.exit()
    for idx, cookie in enumerate(cookies.split("&")):
        zz = requests.post(url=Url, data=cookie, headers=head).json()
        if zz['key'] == 'ok':
            if zz['csd_jdt'] == "100%":
                cookie1 = cookie.replace("Watering", "PlantRipe")
                SowRes = requests.post(url=Url, data=cookie1, headers=head).json()
                if SowRes['key'] == 513:
                    cookie1 = cookie.replace("Watering", "PlantSow")
                    SowRes = requests.post(url=Url, data=cookie1, headers=head).json()
                    if SowRes['key'] == "ok":
                        logging.info("好游快报:收获，重新播种完成")
                        message.append(f"😊第{idx}个账号，收获，重新播种完成")
                        return "收获，重新播种完成"
                    else:
                        logging.info("好游快报:收获完成，重新播种失败")
                        message.append(f"😢第{idx}个账号，收获完成，重新播种失败")
                        return "收获完成，重新播种失败"
                else:
                    logging.info("好游快报:收获，重新播种完成")
                    message.append(f"😊第{idx}个账号，收获，重新播种完成")
                    return "收获，重新播种完成"
            else:
                logging.info("好游快报:浇水完成")
                message.append(f"😊第{idx}个账号，浇水完成")
                return "浇水完成"
        elif zz['key'] == '502':
            cookie1 = cookie.replace("Watering", "PlantRipe")
            SowRes = requests.post(url=Url, data=cookie1, headers=head).json()
            if SowRes['key'] == 513:
                cookie1 = cookie.replace("Watering", "PlantSow")
                SowRes = requests.post(url=Url, data=cookie1, headers=head).json()
                if SowRes['key'] == "ok":
                    logging.info("好游快报:收获，重新播种完成")
                    message.append(f"😊第{idx}个账号，收获，重新播种完成")
                    return "收获，重新播种完成"
                else:
                    logging.info("好游快报:收获，重新播种失败")
                    message.append(f"😢第{idx}个账号，收获，重新播种失败")
                    return "收获，重新播种失败"
            else:
                logging.info("好游快报:收获失败，请手动收获")
                message.append(f"😢第{idx}个账号，收获失败，请手动收获")
                return "收获失败，请手动收获"
        elif zz['key'] == '501':
            cookie1 = cookie.replace("Watering", "PlantSow")
            SowRes = requests.post(url=Url, data=cookie1, headers=head).json()
            if SowRes['key'] == "ok":
                logging.info("好游快报:收获，重新播种完成")
                message.append(f"😊第{idx}个账号，收获，重新播种完成")
                return "收获，重新播种完成"
            else:
                logging.info("好游快报:收获完成，重新播种失败")
                message.append(f"😢第{idx}个账号，收获完成，重新播种失败")
                return "收获完成，重新播种失败"
        else:
            logging.info(f"好游快爆:{zz['info']}")
            message.append(f"😢第{idx}个账号，{zz['info']}")
            return zz['info']


if __name__ == '__main__':
    # 初始化日志系统
    initialize.init()
    main()
    # 发送通知
    msg = '\n'.join(message)
    notify.send("好游快报", msg)
