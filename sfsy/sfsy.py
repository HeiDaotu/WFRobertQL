#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: sfsy.py   v
Author: WFRobert
Date: 2023/5/5 14:54
cron: 5 6 6 * * ?
new Env('顺丰速运 v1.03');
Description: 顺丰速运做任务
Update: 2023/5/5 更新cron
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


if __name__ == "__main__":
    # 使用format方法格式化字符串
    cookie = get_cookies()
