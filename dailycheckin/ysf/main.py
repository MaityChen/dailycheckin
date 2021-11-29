# -*- coding: utf-8 -*-
import json
import os
import re

import requests
import urllib3

from dailycheckin import CheckIn

urllib3.disable_warnings()


class YSF(CheckIn):
    name = "云闪付"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(session):
        tokenResponse = session.get(url="https://youhui.95516.com/newsign/unionpay/config?reLogin=false&path=/")
        if tokenResponse.ok:
            token = "Bearer " + re.findall(r'token":"(.*?)"', tokenResponse.text)[0]
        else:
            return [{"name": "签到信息", "value": "Token获取现问题"}][0]

        session.headers.update(
            {
                "Origin": "https://youhui.95516.com",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/sa-sdk-ios  (com.unionpay.chsp) (cordova 4.5.4) (updebug 0) (version 905) (UnionPay/1.0 CloudPay) (clientVersion 167) (language zh_CN) (upHtml)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Referer": "https://youhui.95516.com/newsign/public/app/index.html",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Authorization": token,
            }
        )

        response = session.post(url="https://youhui.95516.com/newsign/api/daily_sign_in", verify=False)
        msg = response
        if msg.ok:
            msg = [
                {"name": "签到信息", "value": "云闪付签到完成"}
            ]
        else:
            msg = [
                {"name": "签到信息", "value": "签到出现问题"}
            ]
        return msg

    def main(self):
        ysf_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.check_item.get("cookie").split("; ")}
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, ysf_cookie)
        session.headers.update(
            {
                "Host": "youhui.95516.com",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/sa-sdk-ios  (com.unionpay.chsp) (cordova 4.5.4) (updebug 0) (version 905) (UnionPay/1.0 CloudPay) (clientVersion 167) (language zh_CN) (upHtml)",
                "Referer": "https://youhui.95516.com/newsign/public/app/index.html",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br"
            }
        )
        msg = self.sign(session=session)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    _check_item = datas.get("YSF", [])[0]
    print(YSF(check_item=_check_item).main())
