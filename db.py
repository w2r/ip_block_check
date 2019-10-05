# -*- encoding: utf-8 -*-

import requests
import pymongo
import result

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["CHERBIM"]
IP_Port = my_db["IP_Port"]


# 数据库保存,查询和删除
def ip_saved(info_json, i):
    _id = info_json["result"][i]["update_id"]
    chat_id = info_json["result"][i]["message"]["from"]["id"]
    username = info_json["result"][i]["message"]["from"]["username"]
    ip_port = info_json["result"][i]["message"]["text"].replace("&ip_check ", "")
    data = {"_id": _id, "chat_id": chat_id, "username": username, "ip_port": ip_port}
    try:
        IP_Port.insert_one(data, bypass_document_validation=True)
        try:
            result.check_result(chat_id, ip_port)
        except IndexError:
            pass

    except pymongo.errors.DuplicateKeyError:
        pass


def ip_check():
    pass


def ip_delete():
    pass
