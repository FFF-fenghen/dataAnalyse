import matplotlib.pyplot as plt
import pymysql

db = pymysql.connect(
    user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
    password="456789",
    host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
    database='top_movies_250',
    port=3306
)

cursor = db.cursor()

sql = '''
    drop table if exists movies;
    create table movies
    (id int primary key not null); //
    delimiter;
'''

cursor.execute(sql)

db.commit()
db.close()