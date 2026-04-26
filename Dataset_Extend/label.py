import os

filename = os.listdir('normal')
for file in filename:
    label = open('normal_lable/' + file[:-4] + '.txt', mode='w')
    label.close()