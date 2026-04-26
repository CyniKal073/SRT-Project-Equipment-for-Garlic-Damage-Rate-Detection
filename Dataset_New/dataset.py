import os
import divide
import yaml_generate as yaml

'''
新的数据集存储格式
-DataSet
    -train
        -image.jpg
         ...
        -label.txt
         ...
    -test
        -同上
         ...
    -val
        -同上
         ...
    -Images
        -存全部图像
    -Labels
        -存全部标签
    dataset.yaml
        待生成的数据集配置文件
    class.txt
        标签种类
    
'''
try:
    os.mkdir('DataSet')
except FileExistsError:
    try:
        os.mkdir('DataSet/Images')
        os.mkdir('DataSet/Labels')
    except FileExistsError:
        try:
            os.mkdir('DataSet/train')
            os.mkdir('DataSet/val')
            os.mkdir('DataSet/test')
        except FileExistsError:
            pass
    except FileExistsError:
        pass
    pass


image_sets = ['train', 'val', 'test']
# 确定训练集、验证集、测试集比例
rate = [7, 2, 1]
img_path = 'DataSet/Images'
label_path = 'DataSet/Labels'

path = os.getcwd()
classes = open('DataSet/classes.txt', 'r')
class_list = classes.readlines()
num = len(class_list)
list = range(num)
for i in list:
    class_list[i] = class_list[i][:-1]

# 图像标签分类器，输入训练集、验证集、测试集之比，以及标签、图像路径
divide.copy(rate,
            label_path,
            img_path)

# 生成配置文件，输入图像绝对路径的txt文件路径、classes、分类数目
yaml.yaml_generate(path,
                   class_list,
                   num)