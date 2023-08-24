import logging
from typing import NoReturn
import time
import random


def init_logger() -> NoReturn:
    """
    初始化日志系统

    :return:
    """
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log_format = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
    )

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(log_format)
    log.addHandler(ch)


def random_delay():
    # 生成10秒到10分钟之间的随机延迟时间
    delay = random.uniform(10, 600)
    time.sleep(delay)


if __name__ == '__main__':
    # 随机延迟
    random_delay()
    # 初始化日志
    init_logger()
