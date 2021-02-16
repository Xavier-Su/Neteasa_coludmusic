from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
import sys
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import re
import xlwt
import sqlite3
import requests
import os
count = 0
upage = 0

def main():

    baseurl = 'https://music.163.com/discover/toplist'
    askurl(baseurl)
    savepath = '歌曲.xls'
    print("开始爬取。。。")
    getlist(baseurl)
    #getsong(baseurl)
    #id(baseurl)
    #print(idlink, songname)
    #savedata2(idlink, songname, savepath)


findsong = re.compile(r'<meta content="title=(.*?)')


def askurl(url):
    head = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',

    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "response"):
            print(e.response)
    return html


idlink = []
songname = []


def getlist(baseurl):
    html = askurl(baseurl)

    tree = etree.HTML('html')
    print(tree)
    #id_num = tree.xpath('//ul[@class="f-hide"]/a')
    id_num = tree.xpath('//ul[@class="f-hide"]/li//text()')
    print(id_num)

def getsong(baseurl):
    global idlink
    global songname
    url = baseurl
    html = askurl(url)

    soup = BeautifulSoup(html, "html.parser")

    #item = '''<ul class="f-hide"><li><a href="/song?id=557584658">老古董</a></li><li><a href="/song?id=569213279">大千世界</a></li><li><a href="/song?id=865460477">艺术家们</a></li><li><a href="/song?id=865460478">九月清晨</a></li><li><a href="/song?id=865460479">浪</a></li><li><a href="/song?id=865460480">重复重复</a></li><li><a href="/song?id=862099032">明智之举</a></li><li><a href="/song?id=573384240">如约而至</a></li><li><a href="/song?id=865460483">柳成荫</a></li></ul>
  #'''

    for item in soup.find_all('ul', class_="f-hide"):
        res = r'<a .*?>(.*?)</a>'
        mm = re.findall(res, str(item), re.S | re.M)

        res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
        link = re.findall(res_url, str(item), re.I | re.S | re.M)

        for value in mm:
            songname.append(value)
            # print(songname[0])

        for url in link:
            add = 'https://music.163.com'
            urlall = add +url
            idlink.append(urlall)
            # print(idlink)


    # for item in soup.find_all('li'):
    #     print(item)
    #     song = re.findall(findsong, str(item))
    #     dataid.append(song)
    #
    # print(dataid)
    # print(idnum)


def savedata2(idlink, songname, savepath):
    print("保存中。。。")

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('歌曲', cell_overwrite_ok=True)
    col = ("歌曲名", "歌曲链接")
    for c in range(0, 2):
        sheet.write(0, c, col[c])
    for i in range(0, 9):
        sheet.write(i + 1, 0, songname[i])
        sheet.write(i + 1, 1, idlink[i])

    book.save(savepath)


if __name__ == '__main__':
    main()
    print('爬取完成')
    #os.system("pause")

