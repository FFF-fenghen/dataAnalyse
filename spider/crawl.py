from bs4 import BeautifulSoup  # 解析网页，获取数据
import re  # 正则表达式
import urllib.error  # 指定url，获取网页数据
import urllib.request
import xlwt  # 进行excel操作
import pymysql


# 影片链接
findLink = re.compile(r'<a href="(.*?)">')
# 寻找图片地址
findImaSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 是忽略换行
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
    print('start crawling')
    baseurl = 'https://movie.douban.com/top250'

    # 爬取网页
    datalist = getData(baseurl)
    savepath = 'movie250.xls'
    # 保存数据
    # saveData(datalist, savepath)  # 保存数据到excel表格
    savaData2DB(datalist)

# 爬取数据，获取电影名称
def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + '?start=' + str(i * 25)
        html = askUrl(url)
        #  逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')  # 将html整编成文档树
        items = soup.find_all('div', class_='item')
        for item in items:
            data = []
            item = str(item)
            link = re.findall(findLink, item)[0]
            data.append(link)

            img = re.findall(findImaSrc, item)[0]
            data.append(img)

            title = re.findall(findTitle, item)
            if len(title) >= 2:
                data.append(title[0])
                data.append(title[1].replace('/', ''))
            else:
                data.append(title[0])
                data.append('  ')

            rate = re.findall(findRating, item)[0]
            data.append(rate)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)
            if len(inq) > 0:
                data.append(inq[0].replace('。', ''))
            else:
                data.append(' ')

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉br
            bd = re.sub('/', ' ', bd)
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)

    return datalist

# 封装浏览的头部信息，模拟浏览器访问豆瓣网
def askUrl(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=header)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')  # 阅读返回的信息，并以utf-8的方式格式化html文件
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print(e.reason)
        if hasattr(e, 'code'):
            print(e.code)
    return html

# 存储到excel
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('TopMovies250', cell_overwrite_ok=True)
    col = ['电影详情链接', '图片链接', '中文名', '影片外国名', '评分', '评分人数', '概况', '相关信息']
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)

# 存储数据到数据库
def savaData2DB(datalist):
    # 连接数据库
    db = pymysql.connect(
        user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
        password="456789",
        host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
        database='top_movies_250',
        port=3306
    )

    cursor = db.cursor()
    # 创建表格
    create_table(cursor)

    # 开始存储数据到数据库
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250 
            (info_link, pic_link,cname,name2,score,rated,introduction,info)
            values(%s)
        ''' % ",".join(data)  # % 是占位符，’,‘表示各个词组之间使用“,”连接
        cursor.execute(sql)
    # 数据存储完毕
    cursor.close()
    db.commit()
    db.close()

# 创建table
def create_table(cursor):
    sql = '''
    create table movie250
    (
    id integer primary key not null auto_increment,
    info_link text,
    pic_link text,
    cname varchar(250),
    name2 varchar(250),
    score numeric,
    rated numeric,
    introduction text,
    info text     
    ); 
    '''
    cursor.execute(sql)


if __name__ == '__main__':
    main()

