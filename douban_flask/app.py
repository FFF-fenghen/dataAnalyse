import pymysql

from flask import Flask, render_template, request

app = Flask(__name__)  # 初始化一个对象叫app，将自身的框架导入到程序中


@app.route('/')  # 路由解析
def index():
    return render_template('index.html')


@app.route('/index')  # 路由解析
def home():
    return render_template('index.html')


@app.route('/movie')  # 路由解析
def movie():
    datalist = []
    db = pymysql.connect(
        user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
        password="456789",
        host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
        database='top_movies_250',
        port=3306
    )
    cursor = db.cursor()
    sql = '''
        select * from movie250
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    for item in data:
        datalist.append(item)
    cursor.close()
    db.close()
    return render_template('movie.html', movies=datalist)


@app.route('/team')  # 路由解析
def team():
    return render_template('team.html')


@app.route('/word')  # 路由解析
def word():
    return render_template('word.html')

@app.route('/score')  # 路由解析
def score():
    score=[]
    num=[]
    db = pymysql.connect(
        user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
        password="456789",
        host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
        database='top_movies_250',
        port=3306
    )
    cursor = db.cursor()
    sql = '''
          select score,count(score)  from movie250 group by score;
       '''
    cursor.execute(sql)
    data = cursor.fetchall()
    for item in data:
        score.append(item[0])
        num.append(item[1])


    cursor.close()
    db.close()
    return render_template('score.html', score=score, num=num)


if __name__ == '__main__':
    app.run(debug=True)  # 启动服务器， 并开启debug模式
