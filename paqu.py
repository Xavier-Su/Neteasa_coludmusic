
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
songs = 0
upage = 0


def main():
    # print("网易云歌手专辑与发布时间爬取程序")
    # a = "https://music.163.com/artist/album?id="
    # print("请输入歌手在网易云的id号：")
    # b = input()
    # c = "&limit=12&offset=0"
    # baseurl = a + b + c
    baseurl = 'https://music.163.com/artist/album?id=5771&limit=12&offset=0'
    html = askurl(baseurl)
    print("开始爬取。。。")
    #id(baseurl)
    getp(baseurl, html)
    print("页数", upage)
    idnum = id(baseurl, html)
    print("专辑id：")
    print(idnum)

    getdata2(baseurl)
    print("专辑名称：")
    print(albumname)
    print("专辑链接：")
    print(albumnlink)
    print("发布时间：")
    print(albumtime)
    print("专辑数量：", count)

    getsong(idnum, count)
    print("歌曲名称：")
    print(songname)
    print("歌曲数量：", songs)
    print("歌曲链接：")
    print(idlink)

    getname(baseurl, html)
    print("音乐人名称：")
    print(artistname)


    # getp(baseurl)
    # dataname = getname(baseurl)
    # datalist = getdata2(baseurl)
    #
    # w = "网易云歌手"
    # x = "的专辑数据.xls"
    # savepath = w + str(dataname[0][0]) + x
    #
    # global count
    # global upage
    # savedata2(datalist, savepath, upage, dataname, count)


findname = re.compile(r'<meta content="(.*?)" name="keywords">')
findalbum = re.compile(r'<p class="dec dec-1 f-thide2 f-pre" title="(.*?)">')
findtime = re.compile(r'<span class="s-fc3">(.*?)</span>')
findid = re.compile(r'<a class="msk" href="(.*?)">')
findsong = re.compile(r'<meta content="title=(.*?)')


def getp(baseurl, html):
    # url = baseurl
    # html = askurl(url)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div',  class_="u-page"):
        for item2 in soup.find_all('a', class_="zpgi"):
            global upage
            upage = upage + 1


idnum = []

def id(baseurl, html):
    dataid = []
    global idnum
    for i in range(0, upage):
        url = baseurl + str(i * 12)
        html = askurl(url)
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('div', class_="u-cover u-cover-alb3"):
            #print(item)
            album_id = re.findall(findid, str(item))
            dataid.append(album_id)
            num = re.findall("[0-9]+", str(album_id))
            idnum.append(num)
    #print(dataid)
    #print(idnum)

    return idnum


artistname = []


def getname(baseurl, html):
    global artistname
    # url = baseurl
    # html = askurl(url)
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('head'):
        item = str(item)
        name = re.findall(findname, item)
        artistname.append(name)
    return artistname


albumname = []
albumnlink = []
albumtime = []

def getdata2(baseurl):
    #datalist = []
    global albumname
    global albumtime
    for i in range(0, upage):
        url = baseurl + str(i*12)
        html = askurl(url)
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('li'):
            #data = []
            item = str(item)

            album = re.findall(findalbum, item)
            albumname.append(album)

            time = re.findall(findtime, item)
            albumtime.append(time)

            #datalist.append(data)

        for item2 in soup.find_all('p', class_="dec dec-1 f-thide2 f-pre"):
            item2 = str(item2)

            global count
            count = count + 1

    #return datalist


idlink = []
songname = []


def getsong(idnum, count):
    global idlink
    global songname
    global albumnlink
    for n in range(0, count):
        num = ''.join(idnum[n])
        url = 'https://music.163.com/album?id='+num
        albumnlink.append(url)
        html = askurl(url)
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all('ul', class_="f-hide"):
            res = r'<a .*?>(.*?)</a>'
            mm = re.findall(res, str(item), re.S | re.M)

            res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
            link = re.findall(res_url, str(item), re.I | re.S | re.M)

            for value in mm:
                songname.append(value)
                global songs
                songs = songs + 1
                # print(songname[0])

            for url in link:
                add = 'https://music.163.com'
                urlall = add + url
                idlink.append(urlall)
                # print(idlink)
def askurl(url):
    head = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # soup = BeautifulSoup(html, "html.parser")
        # print(soup)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "response"):
            print(e.response)
    return html


def savedata2(datalist, savepath, upage, dataname, count):
    print("保存中。。。")

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('音乐专辑', cell_overwrite_ok=True)
    col = ("歌曲名", "音乐人", "歌曲链接", "所属专辑", "发布时间", "专辑链接")
    for c in range(0, 6):
        sheet.write(0, c, col[c])
    for i in range(0, upage):
        data = datalist[i*72 + 4]
        for m in range(0, 12):
            for j in range(0, 2):
                sheet.write(12 * i + m + 1, j, datalist[i*71 + 4 + m][j])
    for n in range(0, count):
        print("第%d条" % (n + 1))
        sheet.write(n + 1, 2, dataname[0])
    book.save(savepath)

if __name__ == '__main__':
    main()
    print('爬取完成')
    #os.system("pause")


