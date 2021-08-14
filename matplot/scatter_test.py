import matplotlib.pyplot as plt
import numpy as np

click = np.random.randint(1000, size=300)
income = np.random.randint(1000, size=300)

plt.scatter(
    click, income, label='as income', s=25, marker='o'
)
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(['legend'])
plt.title('title')
plt.show()
