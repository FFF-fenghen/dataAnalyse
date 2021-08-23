import pymysql

from flask import Flask, render_template, request

app = Flask(__name__)  # 初始化一个对象叫app，将自身的框架导入到程序中


@app.route('/')  # 路由解析
def score():
    work_area = []
    db = pymysql.connect(
        user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
        password="456789",
        host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
        database='51job',
        port=3306
    )
    cursor = db.cursor()
    sql = '''
         SELECT count(*) FROM 51job.job_ai
         where workArea like "上海%"
            or workArea like '浦东%'
            or workArea like '徐汇%'
            or workArea like '静安%'
            or workArea like '浦西%'
            or workArea like '闵行%'
            ;
       '''
    cursor.execute(sql)
    data = cursor.fetchall()
    work_area.append(data[0][0])
    sql = '''
             SELECT count(*) FROM 51job.job_ai
             where workArea like "北京%";
           '''
    cursor.execute(sql)
    data = cursor.fetchall()
    work_area.append(data[0][0])
    sql = '''
                 SELECT count(*) FROM 51job.job_ai
                 where workArea like "广州%"
                  or workArea like "深圳%"
                  or workArea like "佛山%"
                  or workArea like "广东%"


                  ;
               '''
    cursor.execute(sql)
    data = cursor.fetchall()
    work_area.append(data[0][0])
    sql = '''
                    SELECT count(*) FROM 51job.job_ai
                        where workArea like "%南京%" 
                        or workArea like '浙江%'
                        or workArea like '杭州%'
                        or workArea like '江苏%'
                        or workArea like '安徽%'
                        or workArea like '合肥%'
                        or workArea like '苏州%'
                        ;
                  '''
    cursor.execute(sql)
    data = cursor.fetchall()
    work_area.append(data[0][0])
    print(work_area)

    #  分许薪酬数据
    salary = []
    sql = '''
                       SELECT count(*) FROM 51job.job_ai
                           where salary < 8000
                           ;
                     '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])

    sql = '''
                          SELECT count(*) FROM 51job.job_ai
                              where salary between 8000 and 12000
                              ;
                        '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])

    sql = '''
                              SELECT count(*) FROM 51job.job_ai
                                  where salary between 12000 and 15000
                                  ;
                            '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])

    sql = '''
                                SELECT count(*) FROM 51job.job_ai
                                    where salary between 15000 and 20000
                                    ;
                              '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])

    sql = '''
                                SELECT count(*) FROM 51job.job_ai
                                    where salary between 20000 and 25000
                                    ;
                              '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])

    sql = '''
                                   SELECT count(*) FROM 51job.job_ai
                                       where salary between 25000 and 30000
                                       ;
                                 '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])

    sql = '''
                                      SELECT count(*) FROM 51job.job_ai
                                          where salary > 30000
                                          ;
                                    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    salary.append(data[0][0])
    print(salary)

    cursor.close()
    db.close()

    return render_template('index.html', work_area = work_area,  salary= salary)


if __name__ == '__main__':
    app.run(debug=True)  # 启动服务器， 并开启debug模式
