import os
import random
import shutil

def copy(rate,
           label_path,
           img_path):

    total_label = os.listdir(label_path)
    num = len(total_label)
    list = range(num)
    trainval = int(num * (rate[0] + rate[1]) / 10)
    train = int(num * rate[0] / 10)
    Index_trainval = random.sample(list, trainval)
    Index_train = random.sample(Index_trainval, train)

    for i in list:
        name_label = '/' + total_label[i][:-4] + '.txt'
        name_img = '/' + total_label[i][:-4] + '.jpg'
        if i in Index_trainval:
            if i in Index_train:
                shutil.copy(label_path + name_label, 'DataSet/train')
                shutil.copy(img_path + name_img, 'DataSet/train')
            else:
                shutil.copy(label_path + name_label, 'DataSet/val')
                shutil.copy(img_path + name_img, 'DataSet/val')
        else:
            shutil.copy(label_path + name_label, 'DataSet/test')
            shutil.copy(img_path + name_img, 'DataSet/test')


if __name__ == '__main__':
    # 确定训练集、验证集、测试集比例
    rate = [7, 2, 1]
    label_path = 'DataSet/Labels'
    img_path = 'DataSet/Images'
    copy(rate,
         label_path,
         img_path)