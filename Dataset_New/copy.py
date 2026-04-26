import shutil
import os

img_names = os.listdir('DataSet/Images')
lab_dir = 'D:\\PyCharm\\Dataset_Extend\\test_label_enhance'
save_dir = 'DataSet/Labels'
lab_names = os.listdir(lab_dir)
for i in range(len(img_names)):
    img_names[i] = img_names[i][:-4]
for lab_name in lab_names:
    if lab_name[:-4] in img_names:
        shutil.copy(lab_dir + '/' + lab_name, save_dir)