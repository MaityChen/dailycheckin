# -*- coding: utf-8 -*-
import json
import os
import re

import requests
import urllib3
from requests import utils

from dailycheckin import CheckIn

urllib3.disable_warnings()


class HLDC(CheckIn):
    name = "哈啰单车"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(session, data):
        response = session.post(url="https://api.hellobike.com/api?common.welfare.signAndRecommend", data=json.dumps(data)).json()
        msg = response
        try:

            if msg.get("data").get("didSignToday"):
                msg = [
                    {"name": "今日签到福利金：", "value": msg.get("data").get("bountyCountToday")}
                ]
            else:
                msg = [
                    {"name": "签到信息", "value": "签到出现问题"}
                ]
            return msg
        except Exception as e:
            print(f"错误信息: {e}")
            return [{"name": "签到信息", "value": "签到出现问题"}]

    def main(self):
        token = self.check_item.get("token")
        session = requests.session()
        session.headers.update(
            {
                "Host": "api.hellobike.com",
                "Content-Type": "application/json",
                "Origin": "https://m.hellobike.com",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "requestId": "37KHhXGikoCFe99",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148; app=easybike; version=6.3.0",
                "Referer": "https://m.hellobike.com/",
                "Content-Length": "146",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",

            }
        )
        data = {
                  "platform": 4,
                  "version": "6.3.0",
                  "action": "common.welfare.signAndRecommend",
                  "systemCode": 61,
                  "token": token,
                  "from": "h5"
                }
        msg = self.sign(session=session, data=data)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("HLDC", [])[0]
    print(HLDC(check_item=_check_item).main())
