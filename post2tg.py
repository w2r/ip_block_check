# -*- encoding: utf-8 -*-
"""
@Author  :   cherbim
@License :   清羽 (C) Copyright 2013-2019
@Contact :   qyu0615@gmail.com
@Software:   PyCharm
@Project ：  第13章
@File    :   post2tg.py
@Time    :   2019/10/5 5:10
@User    ：   wdl10
"""
import requests


def post(chat_id, text):
    post_url = 'https://api.telegram.org/bot981790366:AAHPBpLzVZXzvRiAV4jx7HHJ3**********/sendMessag' \
               'e?chat_id={0}&text={1}'.format(chat_id, text)
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}
    requests.get(post_url, headers=headers)
