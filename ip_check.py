import requests
import time
import db
import result
import post2tg

# 从tg机器人获得信息
html = f"https://api.telegram.org/bot981790366:AAHPBpLzVZXzvRiAV4jx7HHJ3ZAdSVRB0SI/getUpdates"
info1 = requests.get(html)
info1.encoding = 'utf-8'
info = info1.json()

# 输出数据库中结果(每天十二点推送）
if time.strftime("%T") == "12:00:00":
    for x in db.IP_Port.find():
        try:
            result.check_result(x['chat_id'], x['ip_port'])
        except IndexError:
            pass


def run():
    text = "请务必阅读关于后输出正确指令，否则可能报错"
    post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
    update_id = 184912313

    # 数据入库
    while True:
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
        if info["result"][-1]["update_id"] != update_id:
            update_id = info["result"][-1]["update_id"]
            if "&ip_saved" in info["result"][-1]["message"]["text"]:
                text = "你保存的ip记录为："
                post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                for x in db.IP_Port.find({"username": info["result"][-1]["message"]["from"]["username"]}):
                    post2tg.post(info["result"][-1]["message"]["from"]["id"], x["ip_port"].replace("&ip_check ", ""))
            if "&ip_delete" in info["result"][-1]["message"]["text"]:
                ip_delete = info["result"][-1]["message"]["text"].replace("&ip_delete ", "")
                for y in db.IP_Port.find({"ip_port": ip_delete}):
                    text = "已从数据库删除IP: " + "\n" + ip_delete
                    post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                    db.IP_Port.delete_one(y)
        time.sleep(60)


run()
