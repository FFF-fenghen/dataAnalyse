from pprint import pprint

from wordcloud import WordCloud
from PIL import Image
import numpy as np
import pymysql
import jieba
from matplotlib import pyplot as plt

text = ''
db = pymysql.connect(
    user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
    password="456789",
    host='127.0.0.1',  # mysql 服务端的IP， 一般是127.0.0.1
    database='top_movies_250',
    port=3306
)
cursor = db.cursor()
sql = '''
       select introduction from movie250;
    '''
cursor.execute(sql)
data = cursor.fetchall()
# print(data)
for item in data:
    text =text + item[0]
cursor.close()
db.close()

wd = jieba.cut(text)
string = ' '.join(wd)

img = Image.open('./static/assets/img/tree.png')
img_array = np.array(img)

wc = WordCloud(
     background_color='white',
    mask = img_array,
    font_path='msyh.ttc'
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
# plt.show()
# 输出词云图片
plt.savefig('./static/assets/img/word.png', dpi=500)

