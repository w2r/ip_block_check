# -*- encoding: utf-8 -*-

import requests
from torequests.utils import curlparse
import json
import post2tg


# 查询结果并推送到机器人
def check_result(id_number, id_port):
    if id_port != -1:
        x = {"chat_id": id_number, "ip_port": id_port}
        site = x["ip_port"].split("/", 1)[0]
        port = int(x["ip_port"].split("/", 1)[1])

        curl_3 = """curl 'http://www.cherbim.com/check.php' -H 'Accept: */*' -H 'Referer: http://api.qingyushop.ml/' -H 'Origin: http://api.qingyushop.ml' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' --data 'ip={0}&port={1}' --compressed --insecure""".format(
            site, port)
        curl_4 = r"""curl 'http://api.qingyushop.ml/check.php' -H 'Cookie: __cfduid=dcda57671c2ae2a72ce54d68367ec16001565742656' -H 'Origin: http://api.qingyushop.ml' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://api.qingyushop.ml/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'ip={0}&port={1}' --compressed --insecure""".format(
            site, port)

        requests_3 = curlparse(curl_3)
        requests_4 = curlparse(curl_4)
        try:
            t3 = requests.request(**requests_3)
            t4 = requests.request(**requests_4)
            t_1 = json.loads(t3.text)
            t_2 = json.loads(t4.text)

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

            if t_2["icmp"] == "success":
                if t_2["tcp"] == "success":
                    text_2 = result_2[0]
                else:
                    text_2 = result_2[1]
            else:
                if t_2["tcp"] == "success":
                    text_2 = result_2[2]
                else:
                    text_2 = result_2[3]
            text_content = "{0}/{1}的检测结果为：".format(site, port) + "\n" + text_1 + '\n' + text_2
            post2tg.post(id_number, text_content)
        except Exception:
            pass
    else:
        pass
