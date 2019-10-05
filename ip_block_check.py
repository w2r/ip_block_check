# -*- encoding: utf-8 -*-
import requests
import time
import db
import result
import post2tg


def run():

    # 从tg机器人获得信息
    html = f"https://api.telegram.org/bot981790366:AAHPBpLzVZXzvRiAV4jx7HHJ3**********/getUpdates"
    info1 = requests.get(html)
    info1.encoding = 'utf-8'
    info = info1.json()
    update_id = 184912313

    # 欢迎语
    text = "请务必阅读关于后输出正确指令，否则可能报错"
    post2tg.post(info["result"][-1]["message"]["from"]["id"], text)

    # 主程序
    while True:

        # 输出数据库中结果(每天十二点推送）
        if time.strftime("%T") == "12:00:00":
            for x in db.IP_Port.find():
                try:
                    result.check_result(x['chat_id'], x['ip_port'])
                except IndexError:
                    pass

        # 新数据入库
        for i in range(len(info["result"])):
            try:
                if "&ip_check" in info["result"][i]["message"]["text"]:
                    db.ip_saved(info, i)
                else:
                    pass
            # 解决发送后如果编辑信息造成的bug,懒得再判断了，直接默认忽视编辑过得信息
            except KeyError:
                pass

        # 查看已保存或者删除
        info1 = requests.get(html)
        info1.encoding = 'utf-8'
        info = info1.json()
        if info["result"][-1]["update_id"] != update_id:
            update_id = info["result"][-1]["update_id"]

            # 查看保存的ip/port
            if "&ip_saved" in info["result"][-1]["message"]["text"]:
                text = "你保存的ip记录为："
                post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                for x in db.IP_Port.find({"username": info["result"][-1]["message"]["from"]["username"]}):
                    if x["ip_port"] != "-1":
                        post2tg.post(info["result"][-1]["message"]["from"]["id"], x["ip_port"].replace("&ip_check ", ""))

            # 查看保存的ip/port
            if "&ip_delete" in info["result"][-1]["message"]["text"]:
                ip_delete = info["result"][-1]["message"]["text"].replace("&ip_delete ", "")
                for y in db.IP_Port.find({"ip_port": ip_delete}):
                    text = "已从数据库删除IP: " + "\n" + ip_delete
                    post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                    y_delete = {"ip_port": "-1"}
                    # 删除数据库保存的ip(将其值重置为-1)
                    db.IP_Port.update_one(y, {"$set": y_delete})
        time.sleep(3)


run()
