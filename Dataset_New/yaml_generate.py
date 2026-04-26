import os

def yaml_generate(path,
                  class_list,
                  num):  # 生成配置文件，输入分类的绝对路径、classes、分类数目
    yaml = open('DataSet/data.yaml', 'w')
    yaml.write('train: %s\\DataSet\\train\n'
               'val: %s\\DataSet\\val\n'
               'test: %s\\DataSet\\test\n'
               '\n# classes\n'
               'names:\n'
               % (path, path, path))
    list = range(num)
    for i in list:
        yaml.seek(0,2)
        yaml.write('  %d: %s\n' % (i, class_list[i]))


if __name__ == '__main__':
    path = os.getcwd()
    classes = open('DataSet/classes.txt', 'r')
    class_list = classes.readlines()
    num = len(class_list)
    list = range(num)
    for i in list:
        class_list[i] = class_list[i][:-1]
    yaml_generate(path,
                  class_list,
                  num)