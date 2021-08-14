import matplotlib.pyplot as plt

activity = ['eat', 'sleep', 'work', 'play']
slices = [7, 2, 2, 13]
cols = ['c', 'm', 'y', 'b']

plt.pie(
    slices,  # 饼图内各种活动的时间片
    labels=activity, # 饼图外侧的文字说明
    colors=cols,  # 已经设计好的色彩
    startangle=90,
    shadow=True,
    explode=(0, 0.1, 0, 0),  # 饼装外溢显示的程度
    autopct='%1.1f%%'  # 饼图内百分比的数量
)
plt.title('title')
plt.show()
