import matplotlib.pyplot as plt

name = ['A', 'B', 'C','D', 'E']
age = [18, 24, 12, 37, 34]
height = [170, 175, 175, 180, 179]

plt.plot(name, age, label='age')
plt.plot(name, height, label='height')

plt.xlabel('your_name')
plt.ylabel('values')
plt.title('age,name and height')
plt.legend()
plt.show()
