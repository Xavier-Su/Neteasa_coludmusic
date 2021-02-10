

import sys
import json
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import re
import xlwt
import xlrd
import sqlite3
import requests
import os
count = 0
songs = 0
upage = 0

find_lrc = re.compile(r'\[.*\]')

ldaj
def main():
    print("开始爬取。。。")
    baseurl = "http://music.163.com/api/song/lyric?id=167882&lv=1&kv=1&tv=-1"
    get_lrc(baseurl)

    id_num = "网易云某首歌"
    txt_name = "的歌曲歌词"
    save(id_num, txt_name,txt)

lrc = []
txt = ""


def get_lrc(baseurl):
    global lrc
    global txt
    url = baseurl
    html = ask_url(url)
    soup = BeautifulSoup(html, "html.parser")
    json_obj = json.loads(html)
    final_lyric = ""
    if ("lrc" in json_obj):
        inital_lyric = json_obj['lrc']['lyric']
        regex = re.compile(r'\[.*\]')
        final_lyric = re.sub(regex, '', inital_lyric).strip()
        lrc.append(final_lyric)
        txt = str(lrc[0])
    #txt = txt.replace("\n", "\n")
    # txt = txt.replace(" ", "\n")
    print(txt)

    return lrc


def ask_url(url):
    head = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63',
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #soup = BeautifulSoup(html, "html.parser")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "response"):
            print(e.response)
    return html


def save(id_num, txt_name, txt):
    if txt == "":
        return
    with open(id_num + "" + txt_name+".txt", "w")as f:
        f.write(txt)



if __name__ =="__main__":
    main()