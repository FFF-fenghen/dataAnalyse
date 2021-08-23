import json

from bs4 import BeautifulSoup  # 解析网页，获取数据
import re  # 正则表达式
import urllib.error  # 指定url，获取网页数据
import urllib.request
import xlwt  # 进行excel操作
import pymysql

table1 = 1
def main(baseurl):
    print('start crawling')
    datalist = getData(baseurl)
    savaData2DB(datalist)


# 爬取数据，获取电影名称
def getData(baseurl):
    datalist = []

    url = baseurl
    # 封装头部，防止被反爬虫
    html = askUrl(url)
    #  逐一解析数据
    soup = BeautifulSoup(html, 'html.parser')  # 将html整编成文档树

    items = soup.select("body > script", type="text/javascript")  # CSS 选择器，选取body里面script中的内容
    items = str(items)  # 将获取道德内容转换成string格式，才能够进行文字的提取
    items = re.findall(r'window.__SEARCH_RESULT__ = (.*?)</script>', items, re.S)  # 提取script中的内容格式

    string = ''.join(items)  # 这句话暂时不明白什么用途
    info_dict = json.loads(string)  # 将string转化成json格式
    dit_py = info_dict['engine_search_result']  # 利用字典提取的方式获取json中属性为为engine_search_result的内容值
    for i in dit_py:  # 获取到的 i 是一个字典组
        dit = {}
        if len(i['attribute_text']) > 2:
            dit['qualification'] = i['attribute_text'][2]
        else:
            dit['qualification'] = ''
        dit['work_experience'] = i['attribute_text'][1]
        dit['job_name'] = i['job_name']
        dit['company_name'] = i['company_name']
        dit['money'] = i['providesalary_text']
        dit['workarea'] = i['workarea_text']
        dit['companytype'] = i['companytype_text']
        dit['jobwelf'] = i['jobwelf']
        dit['companysize'] = i['companysize_text']
        datalist.append(dit)
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
        html = response.read().decode('gbk')  # 阅读返回的信息，并以utf-8的方式格式化html文件
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
    col = ['工作名称', '薪资', '工作地区', '工作经验', '学历', '公司名称', '公司规模', '福利']
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        data = datalist[i]
        sheet.write(i + 1, 0, data['job_name'])
        salary = getMonthSalary(data['money'])
        sheet.write(i + 1, 1, salary)
        sheet.write(i + 1, 2, data['workarea'])
        sheet.write(i + 1, 3, data['work_experience'])
        sheet.write(i + 1, 4, data['qualification'])
        sheet.write(i + 1, 5, data['company_name'])
        sheet.write(i + 1, 6, data['companysize'])
        sheet.write(i + 1, 7, data['jobwelf'])

    book.save(savepath)


def getMonthSalary(data):
    if data == '':
        return ''
    a = data
    b = a.split(r'/')
    salary_time = b[1]  # 获取年薪 或者 月薪 的单位
    unit = b[0][-1]  # 获取薪资单位
    salary_score = b[0][0:-1]  # 获取薪资值
    salary_separate = salary_score.split('-')
    if len(salary_separate) > 1:
        salary_low = float(salary_separate[0])
        salary_high = float(salary_separate[1])
        avarage = (salary_low + salary_high) / 2
    else:
        avarage = float(salary_separate[0])
    if salary_time == '年':
        if unit == '万':
            avarage = avarage * 10000 / 12
        elif unit == '千':
            avarage = avarage * 1000 / 12
    elif salary_time == '月':
        if unit == '万':
            avarage = avarage * 10000
        elif unit == '千':
            avarage = avarage * 1000
    return avarage


# 存储数据到数据库
def savaData2DB(datalist):
    # 连接数据库
    db = pymysql.connect(
        user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
        password="456789",
        host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
        database='51job',
        port=3306
    )
    cursor = db.cursor()

    # 开始存储数据到数据库
    print(' 开始存储数据到数据库*********************')
    for i in datalist:
        data = {}
        data[0] = i['job_name']
        money = getMonthSalary(i['money'])
        if money == '':
            data[1] = 0
        else:
            data[1] = money
        data[2] = i['workarea']
        data[3] = i['work_experience']
        data[4] = i['qualification']
        data[5] = i['company_name']
        data[6] = i['companysize']
        data[7] = i['jobwelf']
        sql = '''
               insert into job_ai
               (job_name, salary,workArea,work_exper,qualification,company_name,company_size,welfare)
               values('%s',%d,'%s','%s','%s','%s','%s','%s')
           ''' % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        cursor.execute(sql)
    # 数据存储完毕

    cursor.close()
    db.commit()
    db.close()

# 创建table
def create_table():
    db = pymysql.connect(
        user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
        password="456789",
        host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
        database='51job',
        port=3306
    )
    cursor = db.cursor()

    sql = '''
    create table job_ai
    (
    id integer primary key not null auto_increment,
    job_name varchar(100),
    salary FLOAT,
    workArea  varchar(25),
    work_exper varchar(25),
    qualification varchar(5),
    company_name varchar(100),
    company_size varchar(50),
    welfare text
    );
    '''
    cursor.execute(sql)


if __name__ == '__main__':
    # create_table()  # 第一次创建的时候根据需要创建数据table
    for i in range(17):
        i = str(i)
        baseurl = ''
        baseurl = 'https://search.51job.com/list/000000,000000,0000,00,9,99,ai,2,'+ i +'.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        # 爬取网页
        main(baseurl)
