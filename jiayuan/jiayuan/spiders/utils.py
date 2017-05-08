#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# author:Samray <samrayleung@gmail.com>
import http.cookiejar
from urllib import parse, request


# cookie = http.cookiejar.CookieJar()
# handler = request.HTTPCookieProcessor(cookie)
# opener = request.build_opener(handler)
# account_data = {"name": 15577262746, "password": "6uQs3z328rZFjdy4"}
# encoded_data = parse.urlencode(account_data).encode('utf-8')
# login_url = "http://www.jiayuan.com/login/dologin.php"
# opener.open(login_url, encoded_data)
# # response = request.urlopen(login_url, encoded_data)

# print(dict(cookie))


def get_cookie():
    account_data = {"name": 15577262746, "password": "6uQs3z328rZFjdy4"}
    encoded_data = parse.urlencode(account_data).encode('utf-8')
    login_url = "http://www.jiayuan.com/login/dologin.php"
    response = request.urlopen(login_url, encoded_data)
    return dict(response.getheader('Set-Cookie'))


if __name__ == "__main__":
    print(get_cookie())
