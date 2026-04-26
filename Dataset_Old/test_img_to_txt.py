import os
import random


def Img_to_txt(rate,
               img_path,
               img_save_path): # 图像路径txt生成器，输入训练集、验证集、测试集之比，以及图像路径、txt保存路径

    Total_xml = os.listdir(img_path)
    num = len(Total_xml)
    list = range(num)
    trainval = int(num * (rate[0]+rate[1]) / 10)
    train = int(num * rate[0] / 10)
    Index_trainval = random.sample(list, trainval)
    Index_train = random.sample(Index_trainval, train)

    path_front = os.getcwd()
    ftrainval = open(img_save_path + '/trainval.txt', 'w')
    ftrain = open(img_save_path + '/train.txt', 'w')
    fval = open(img_save_path + '/val.txt', 'w')
    ftest = open(img_save_path + '/test.txt', 'w')

    for i in list:
        name = path_front + '\\DataSet\\images\\' + Total_xml[i][:-4] + '.jpg\n'
        if i in Index_trainval:
            ftrainval.write(name)
            if i in Index_train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

if __name__ == '__main__':
    # 确定训练集、验证集、测试集比例
    rate = [7, 2, 1]
    xml_path = 'DataSet/Xml'
    img_save_path = 'DataSet/Img-txt'
    Img_to_txt(rate,
               xml_path,
               img_save_path)