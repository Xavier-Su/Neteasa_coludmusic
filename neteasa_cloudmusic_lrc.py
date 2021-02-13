

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


def main():
    print("开始爬取。。。")
    id_nums = input("请输入歌曲在网易云音乐的id号：")
    url_a = 'http://music.163.com/api/song/lyric?id='
    url_b = '&lv=1&kv=1&tv=-1'
    baseurl = url_a + id_nums + url_b

    print("提取歌曲名中。。。")
    get_songs(id_nums)
    print("歌曲名：", songname[0][0])
    #baseurl = "http://music.163.com/api/song/lyric?id=28793140&lv=1&kv=1&tv=-1"
    get_lrc(baseurl)

    id_num = "网易云" + songname[0][0]
    txt_name = "的歌曲歌词"
    txt2 = " " + txt
    print("歌词如下：")
    print(txt2)
    print("----------------------")
    print("正在保存歌词。。。")
    save(id_num, txt_name, txt2)
    print("保存成功。。。")


songname = []
lrc = []
txt = ""
findsongname = re.compile(r'<em class="f-ff2">(.*?)</em>')

def get_songs(id_nums):
    global songname
    url_song_a = 'https://music.163.com/song?id='
    url_song = url_song_a + id_nums
    html = ask_url(url_song)

    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    for song_name in soup.find_all('div', class_="tit"):
        song = re.findall(findsongname, str(song_name))
        songname.append(song)



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
    #print(txt)

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
    print("爬取完成！")