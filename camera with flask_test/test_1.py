import os
import random

files = os.listdir('D:/PyCharm/untitled')
print(files)

num = len(files)
index = range(num)
print(index)


trainval = random.sample(index, 9)
print(trainval)

print(files[1])

for i in index:
    name = files[i] + '\n'
    print(name)