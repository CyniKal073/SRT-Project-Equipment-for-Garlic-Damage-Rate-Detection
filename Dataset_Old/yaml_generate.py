import os

def yaml_generate(path,
                  class_list,
                  num):  # 生成配置文件，输入图像绝对路径的txt文件路径、classes、class的数目
    yaml = open('DataSet/test.yaml', 'w')
    yaml.write('train: %s\\DataSet\\Img-txt\\train.txt\n'
               'val: %s\\DataSet\\Img-txt\\val.txt\n'
               'test: %s\\DataSet\\Img-txt\\test.txt\n'
               '\n# number of classes\n'
               'nc: %d\n'
               '\n# class names\n'
               'names: %s'
               % (path, path, path, num, class_list))


if __name__ == '__main__':
    path = os.getcwd()
    classes = open('DataSet/classes.txt', 'r')
    class_list = classes.readlines()
    num = len(class_list)
    list = range(num)
    for i in list:
        class_list[i] = class_list[i][:-1]
    yaml_generate(path,
                  class_list)