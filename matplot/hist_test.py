import matplotlib.pyplot as plt

ages = [22, 23, 24, 25, 26, 27, 28, 29, 25, 25, 36, 36, 36, 56, 56, 15, 56, 45, 13, 60, 56, 65, 62,90]
bins = [20, 30, 40, 50, 60, 70, 80, 90, 100]

plt.hist(
    ages,
    bins=bins,
    color='blue',
    edgecolor='k',
    density=False,  # 是否将结果转换成概率
    weights=None,
    cumulative=False,  # 是否将数据累次叠加
    histtype='bar',
    align='mid',
    orientation='vertical'
)
plt.xlabel('age score')
plt.ylabel('number')
plt.legend(['what2'])
plt.title('this is a title')
plt.show()
