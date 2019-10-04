# -*- encoding: utf-8 -*-
"""
@Author  :   cherbim
@License :   清羽 (C) Copyright 2013-2019
@Contact :   qyu0615@gmail.com
@Software:   PyCharm
@Project ：  第13章
@File    :   result.py
@Time    :   2019/10/4 22:38
@User    ：   wdl10
"""
import requests
from torequests.utils import curlparse
import json
import post2tg


# 查询结果并推送到机器人
def check_result(id_number, id_port):
    x = {"chat_id": id_number, "ip_port": id_port}
    site = x["ip_port"].split("/", 1)[0]
    port = int(x["ip_port"].split("/", 1)[1])

    # 国内检测
    curl_1 = r'''curl "https://www.toolsdaquan.com/toolapi/public/ipchecking/{0}/{1}" -H "Accept: application/json, text/javascript, */*; q=0.01" -H "Referer: https://www.toolsdaquan.com/ipcheck/" -H "X-Requested-With: XMLHttpRequest" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36" -H "Sec-Fetch-Mode: cors" --compressed'''.format(
        site, port)
    # 国外检测
    curl_2 = r'''curl 'https://www.toolsdaquan.com/toolapi/public/ipchecking2/{0}/{1}' -H 'sec-fetch-mode: cors' -H 'cookie: _ga=GA1.2.1001757648.1569229274; _gid=GA1.2.979977111.1570047939' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H 'accept: application/json, text/javascript, */*; q=0.01' -H 'referer: https://www.toolsdaquan.com/ipcheck/' -H 'authority: www.toolsdaquan.com' -H 'x-requested-with: XMLHttpRequest' -H 'sec-fetch-site: same-origin' --compressed'''.format(
        site, port)
    requests_1 = curlparse(curl_1)
    requests_2 = curlparse(curl_2)
    t1 = requests.request(**requests_1)
    t2 = requests.request(**requests_2)
    t_1 = json.loads(t1.text)
    t_2 = json.loads(t2.text)

    # 结果推送到tg机器人，请修改为botapi和用户id,具体获得方式google搜索
    result_1 = ["国内检测结果：ICMP可用；TCP可用", "国内检测结果：ICMP可用；TCP不可用", "国内检测结果：ICMP不可用；TCP可用", "国内检测结果：ICMP不可用；TCP不可用"]
    result_2 = ["国外检测结果：ICMP可用；TCP可用", "国外检测结果：ICMP可用；TCP不可用", "国外检测结果：ICMP不可用；TCP可用", "国外检测结果：ICMP不可用；TCP不可用"]
    if t_1["icmp"] == "success":
        if t_1["tcp"] == "success":
            text_1 = result_1[0]
        else:
            text_1 = result_1[1]
    else:
        if t_1["tcp"] == "success":
            text_1 = result_1[2]
        else:
            text_1 = result_1[3]

    if t_2["outside_icmp"] == "success":
        if t_2["outside_tcp"] == "success":
            text_2 = result_2[0]
        else:
            text_2 = result_2[1]
    else:
        if t_2["outside_tcp"] == "success":
            text_2 = result_2[2]
        else:
            text_2 = result_2[3]
    text_content = "{0}/{1}的检测结果为：".format(site, port) + "\n" + text_1 + '\n' + text_2
    post2tg.post(id_number, text_content)

