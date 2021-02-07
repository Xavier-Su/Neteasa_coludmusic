
import sys
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


def main():
    print("网易云歌手歌曲爬取程序-by筱风制作")
    a = "https://music.163.com/artist/album?id="
    print("请输入歌手在网易云的id号：")
    b = input()
    c = "&limit=12&offset=0"
    baseurl = a + b + c
    #baseurl = 'https://music.163.com/artist/album?id=5771&limit=12&offset=0'
    html = askurl(baseurl)
    print("开始爬取。。。")

    print("获取歌手信息中。。。")
    getname(baseurl, html)
    print("音乐人名称：", artistname[0][0])

    getp(baseurl, html)
    print("专辑网页页数:", upage)
    print("获取专辑id中。。。")
    idnum = id(baseurl, html)
    print("专辑id：")
    print(idnum)

    print("获取专辑和歌曲信息中。。。")
    print("此阶段所需时间略长（所需时间与歌曲数量成正比），请稍等。。。")
    getdata2(baseurl)
    getsong(idnum, count)
    print("专辑名称：")
    print(albumname)

    print("发布时间：")
    print(albumtime)
    print("专辑数量：", count)
    print("专辑链接：")
    print(albumnlink)

    print("每张专辑里面歌曲数量：", albumsongs)

    print("歌曲名称：")
    print(songname)
    print("歌曲数量：", songs)
    print("歌曲链接：")
    print(idlink)


    w = "网易云歌手"
    x = "的歌曲数据.xls"
    savepath = w + str(artistname[0][0]) + x
    w = "网易云歌手"
    x = "的歌曲数据.db"
    dbpath = w + str(artistname[0][0]) + x
    print("将爬取信息保存在表格中。。。")
    savedata2(savepath)
    print("装入数据库中。。。")
    savedb(savepath, dbpath)


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

    if upage == 0:
            url = baseurl
            html = askurl(url)
            soup = BeautifulSoup(html, "html.parser")

            for item in soup.find_all('div', class_="u-cover u-cover-alb3"):
                # print(item)
                album_id = re.findall(findid, str(item))
                dataid.append(album_id)
                num = re.findall("[0-9]+", str(album_id))
                idnum.append(num)
        # print(dataid)
        # print(idnum)

    else:
        for i in range(0, upage):
            url = baseurl + str(i * 12)
            html = askurl(url)
            soup = BeautifulSoup(html, "html.parser")

            for item in soup.find_all('div', class_="u-cover u-cover-alb3"):
                # print(item)
                album_id = re.findall(findid, str(item))
                dataid.append(album_id)
                num = re.findall("[0-9]+", str(album_id))
                idnum.append(num)
        # print(dataid)
        # print(idnum)





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
    global count
    if upage == 0:
        #for i in range(0, upage):
            url = baseurl
            html = askurl(url)
            soup = BeautifulSoup(html, "html.parser")

            for item in soup.find_all('p', class_="dec dec-1 f-thide2 f-pre"):
                # data = []
                item = str(item)

                album = re.findall(findalbum, item)
                albumname.append(album)

            for item in soup.find_all('span', class_="s-fc3"):
                # data = []
                item = str(item)

                time = re.findall(findtime, item)
                if not time:
                    break
                albumtime.append(time)

                # datalist.append(data)

            for item2 in soup.find_all('p', class_="dec dec-1 f-thide2 f-pre"):
                item2 = str(item2)


                count = count + 1

    else:
        for i in range(0, upage):
            url = baseurl + str(i * 12)
            html = askurl(url)
            soup = BeautifulSoup(html, "html.parser")

            for item in soup.find_all('p', class_="dec dec-1 f-thide2 f-pre"):
                # data = []
                item = str(item)

                album = re.findall(findalbum, item)
                albumname.append(album)
                albums = 1
            for item in soup.find_all('span', class_="s-fc3"):
                # data = []
                item = str(item)
                if albums > 12:
                    break
                time = re.findall(findtime, item)
                if not time:
                    break
                albumtime.append(time)
                albums = albums + 1

                # datalist.append(data)

            for item2 in soup.find_all('p', class_="dec dec-1 f-thide2 f-pre"):
                item2 = str(item2)

                #global count
                count = count + 1




    #return datalist


idlink = []
songname = []
albumsongs = []


def getsong(idnum, count):
    global idlink
    global songname
    global albumnlink
    global albumsongs
    for n in range(0, count):
        num = ''.join(idnum[n])
        url = 'https://music.163.com/album?id='+num
        albumnlink.append(url)
        html = askurl(url)
        soup = BeautifulSoup(html, "html.parser")
        songnumber = 0
        for item in soup.find_all('ul', class_="f-hide"):
            res = r'<a .*?>(.*?)</a>'
            mm = re.findall(res, str(item), re.S | re.M)

            res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
            link = re.findall(res_url, str(item), re.I | re.S | re.M)

            for value in mm:
                songname.append(value)
                songnumber = songnumber + 1

                global songs
                songs = songs + 1
                # print(songname[0])

            for url in link:
                add = 'https://music.163.com'
                urlall = add + url
                idlink.append(urlall)
                # print(idlink)
        albumsongs.append(songnumber)
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


def savedata2(savepath):
    print("正在保存。。。")
    place = 1
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('音乐', cell_overwrite_ok=True)
    col = ("歌曲名", "音乐人", "歌曲链接", "所属专辑", "发布时间", "专辑链接")
    for c in range(0, 6):
        sheet.write(0, c, col[c])
    for num in range(0, songs):
        sheet.write(num + 1, 0, songname[num])
        sheet.write(num + 1, 1, artistname[0][0])
        sheet.write(num + 1, 2, idlink[num])

    for i in range(0, count):
        for j in range(0, albumsongs[i]):
            sheet.write(place, 3, albumname[i][0])
            sheet.write(place, 4, albumtime[i][0])
            sheet.write(place, 5, albumnlink[i])
            place = place + 1

    book.save(savepath)


database = []


def savedb(savepath, dbpath):
    global database
    global count

    excel = xlrd.open_workbook(savepath)
    sheet1 = excel.sheet_by_name("音乐")
    for i in range(1, songs + 1):
        base = sheet1.row_values(i)
        database.append(base)
        #print(base)
    #print(database)

    db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for ind in range(len(database)):
        database[ind][0] = database[ind][0].replace(u'\xa0', u' ')
        database[ind][3] = database[ind][3].replace(u'\xa0', u' ')
    for data in database:

        for index in range(len(data)):
            # data[index] = str(data[index])
            data[index] = '"'+data[index]+'"'

        sql = '''
            replace into music(song, artist, song_link, album, time, album_link)
            values(%s)
        ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

    return database


def db(dbpath):
    sql = '''
        create table music(
        song text primary key ,
        artist text,
        song_link text,
        album text,
        time text,
        album_link text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    #conn.close()


if __name__ == '__main__':
    main()

    print('搞定！')
    os.system("pause")


