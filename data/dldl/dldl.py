#! python3
# -*- coding: utf-8 -*-

import requests
import json
import urllib.parse
from bs4 import BeautifulSoup

session = requests.Session()

url_home = input("输入微信分享链接：\n")

if len(url_home) == 0:
    url_home = "http://mp.weixin.qq.com/mp/homepage?__biz=MzIwMTg2NzU4Mw==&hid=12&sn=1cb2b9a74e73dd01951f7e67853209af&scene=18#wechat_redirect"
    print("使用默认链接：" + url_home + "\n\n")

ads = [
    " ", '点击上方"蓝字"关注唐门大小事儿实时知！', "戳“阅读原文”火速进入下一章", "目前100000+人已关注加入我们",
    "点下広吿再走丨助小视能量满满~"
]

title = "斗罗大陆"
s = session.get(url_home)
title = BeautifulSoup(s.text, features="lxml").select(
    'body > div > div > div > h2')[0].get_text().strip().replace("\n", "")
print(title + "\n\n")

query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url_home).query))

__biz = query["__biz"]
hid = query["hid"]
sn = query["sn"]
scene = query["scene"]

cids = 6
with open(title + ".txt", "w+") as file:

    for cid in range(cids):
        data = {
            "__biz": __biz,
            "hid": hid,
            "sn": sn,
            "scene": scene,
            "cid": cid,
            "begin": 0,
            "count": 20,
            "action": "appmsg_list",
            "f": "json",
            "r": 0.27656332194465394
        }

        url = "https://mp.weixin.qq.com/mp/homepage"
        res = session.post(url, data=data)
        json1 = json.loads(res.content)

        for zhangjie in json1["appmsg_list"]:
            chapter = zhangjie["title"]
            content = ""
            try:
                words = BeautifulSoup(session.get(zhangjie["link"]).text,
                                      features="lxml").select(
                                          "#js_content")[0].get_text().strip()
                # content = content + soup0.select("#js_content")[0].get_text(
                # ).replace('点击上方"蓝字"关注唐门大小事儿实时知！', "").replace("   ", "。\n\n")
                for ad in ads:
                    words = words.replace(ad, "")

                n = 0
                word_n = len(words)

                # 是不是一句话
                one = False

                for i in range(word_n):
                    word = words[i]
                    content += word

                    if (word == "“"):
                        one = True
                    elif (word == "”"):
                        one = False

                    if (word == "。" and ((n > 200 and not one) or (n > 500))):
                        content += "\n\n"
                        n = 0
                        one = False

                    n += 1
                print(chapter + "：\n        " +
                      content.replace("\n", "").strip()[0:50] + "……\n")

            except IOError:
                content = "本章节抓取错误，无内容"
                print(chapter + "：\n        " + content)

            file.write(chapter + "\n\n" + content + "\n\n")
