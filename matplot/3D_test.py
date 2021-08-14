import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x=[1,1,2,2]
y=[3,4,4,3]
z=[1,2,1,1]

ax.scatter(x,y,z)

ax.plot_trisurf(x,y,z)  # 这个代码指的是绘制曲面图

plt.show()
