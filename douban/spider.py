# -*- codeing =utf-8 -*-
#@Time: 2020/6/13 11:31
#@Author :cz
#@File : spider.py
#@Software: PyCharm

# import bs4 #网页解析，获取数据
from bs4 import BeautifulSoup #网页解析，获取数据
import re  #正则表达式，进行文字匹配
import urllib.request    #指定url，获取网页数据
import xlwt  #进行excel操作
import sqlite3      #进行sqlite数据库操作

def main():
#1.爬取网页
#2.逐一解析数据
#3.保存数据
    baseurl="https://movie.douban.com/top250?start="
    datalist =getData(baseurl)
    # savepath="豆瓣电影Top250.xls"
    dapath="movie.db"
    # saveData(datalist,savepath)
    savaData2DB(datalist,dapath)
    # askURL("https://movie.douban.com/top250?start=")
    # getData(baseurl)



#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')
#影片图片
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)
#影片片名
findTitle=re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge=re.compile(r'<span>(\d*)人评价</span>')
#找到概识
findInq=re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)


#爬取网页
def getData(baseurl):
    datalist =[]
    for i in range(0,10): #调用获取页面信息的函数，10次
        url = baseurl +str(i*25)
        html = askURL(url)  #保存获取到的网页源码
        # 2.逐一解析数据
        soup =BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            # print(item)
            data=[]
            item=str(item)
            #影片详情的链接
            link=re.findall(findLink,item)[0]
            data.append(link)
            imgSrc=re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle=titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')

            rating = re.findall(findRating,item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',"",bd)
            bd = re.sub('/',"",bd)
            data.append(bd.strip())

            datalist.append(data)
    # print(datalist)
    return datalist

#得到指定一个URL的网页内容
def askURL(url):
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    request = urllib.request.Request(url,headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLRrror as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

#保存数据
def saveData(datalist,savepath):
    print("save......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True) #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概识","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])#列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data =datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j]) #数据
    book.save(savepath)

def savaData2DB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index ==4 or index ==5:
                continue
            data[index] = '"' +data[index] +'"'
        sq l = '''
                insert into movie250 (
                info_link,pic_link,cname,ename,score,rated,instroduction,info)
                values(%s)''' %",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.commit()

def init_db(dbpath):
    sql = '''
        create tab le movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''

    #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ =="__main__":   #当程序执行时
    main()
    print("爬取完毕")

