import jieba.posseg as pseg
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

txt = open(r'mytxt.txt', 'r', encoding='utf_8').read()
result = pseg.cut(txt)
stop_word = ['人']
m = {}
for word, flag in result:
    if flag.find('n') == -1:  # 如果不是名词，则直接跳过
        continue
    if word in m:
        m[word] += 1
    elif word not in stop_word:
        m[word] = 1

r = sorted(m.items(), key=lambda x: x[1], reverse=True)

for i in range(5):
    print(r[i][0], r[i][1])

# 开始绘图
name = [r[0][0], r[1][0], r[2][0], r[3][0], r[4][0]]
slices = [r[0][1], r[1][1], r[2][1], r[3][1], r[4][1]]
cls = ['c', 'k', 'g', 'b', 'r']

plt.pie(
    slices,
    labels=name,
    colors=cls,
    startangle=90,
    autopct='%1.1f%%',
    shadow=True,

)
plt.title('title')
plt.xlabel('xlabel')
plt.ylabel('ylabel')
fname = './'+'pie'+'.png'
plt.savefig(fname)

