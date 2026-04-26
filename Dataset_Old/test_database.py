import os
import random
import xml.etree.ElementTree as ET
import test_img_to_txt as img
import test_xml_to_txt as xml
import yaml_generate as yaml

'''
数据集存放格式如下：
-DataSet
    -Image      
        存照片
    -Img-txt    
        存照片绝对路径的txt文件
    -Xml        
        存打标签的xml文件
    -Xml-txt    
        存图像标签种类和坐标信息的txt文件
    class.txt
        标签种类
    test.yaml
        待生成的数据集配置文件
    一堆脚本.py
    
'''

image_sets = ['train', 'val', 'test']
# 确定训练集、验证集、测试集比例
rate = [7, 2, 1]
img_path = 'DataSet/images'
img_save_path = 'DataSet/Img-txt'

path = os.getcwd()
classes = open('DataSet/classes.txt', 'r')
class_list = classes.readlines()
num = len(class_list)
list = range(num)
for i in list:
    class_list[i] = class_list[i][:-1]

# 图像路径txt生成器，输入训练集、验证集、测试集之比，以及图像路径、txt保存路径
img.Img_to_txt(rate,
               img_path,
               img_save_path)

# 生成配置文件，输入图像绝对路径的txt文件路径、classes、class的数目
yaml.yaml_generate(path,
                   class_list,
                   num)

''' # 处理xml文件，暂时用不到

    for image_set in image_sets:
        image_ids = open('DataSet/Img-txt/%s.txt' %(image_set)).read().strip().split()
        for image_id in image_ids:
            xml.convert_annotation(image_id)
            
'''

