import matplotlib.pyplot as plt
import pymysql

db = pymysql.connect(
    user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
    password="456789",
    host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
    database='sakila',
    port=3306
)

# 获取数据库的操作
cursor = db.cursor()

#  执行mysql语句
cursor.execute(
    'select count(*) from actor where actor_id>100'
)
#  获取数据库的全部查询结果
data = cursor.fetchall()

actor_100 = data[0][0]

cursor.execute(
    'select count(*) from actor where first_name like "%e"'
)
#  获取数据库的全部查询结果
data = cursor.fetchall()

actor_e = data[0][0]

cursor.execute(
    'select count(*) from actor where first_name like "%a"'
)
#  获取数据库的全部查询结果
data = cursor.fetchall()

actor_a = data[0][0]

# 绘制饼图

slices = [actor_a,actor_e,actor_100]
activity = ['actor_a', 'actor_e', 'actor_100']
cls = ['y', 'b', 'g']
plt.pie(
    slices,
    labels=activity,
    colors=cls,
    startangle=90,
    shadow=True,
    autopct='%1.1f%%'
)
plt.title('title')
plt.show()

db.close()