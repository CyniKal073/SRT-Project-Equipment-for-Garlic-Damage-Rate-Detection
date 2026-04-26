import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk

global label_status
global label_time
global label_detect
global label_contor_sum
global label_all
global mass_all
global mass_Healthy
global mass_Breakage
global mass_Others
global label_Healthy
global label_Breakage
global label_Others
global label_rate
global mass_rate
global show_status  # 识别线显示/隐藏
global detect_status  # 保存当前连通域识别情况
global status_to_clear  # 保存上一次连通域识别情况

threshold_value = 60


label_status = "......"
label_time = 0
label_detect = '不存在'
label_contor_sum = 0
label_all = label_Healthy = label_Breakage = label_Others = 0
mass_all = mass_Healthy = mass_Breakage = mass_Others = 0
mass_rate = label_rate = "...%"
show_status = False  # 默认不显示识别线
detect_status = False  # 默认连通域不存在
status_to_clear = False  # 默认上一次连通域不存在



# 主页面
root_window = tkinter.Tk()
root_window.title('大蒜破损率检测系统')
root_window.geometry('1024x600')
root_window.resizable(False,False)
root_window['background'] = '#808080'
#root_window.attributes('-fullscreen', True)  # 设置全屏模式
canvas = tkinter.Canvas(root_window, bg="#CAD0DA", bd="0")  # 设置画布背景颜色
canvas.place(x=0, y=0, width=1024, height=600)  # 设置画布位置和大小

# 页面顶部主题
frame = canvas.create_rectangle(0, 0, 1024, 33, fill='#87CEEB', outline='black')  # 边框
imagename = tkinter.Label(root_window, text='大 蒜 破 损 率 鉴 定 系 统', font='微软雅黑 14', bg='#87CEEB')  # 标题
imagename.place(x=404, y=2)  # 标题位置

# 图像检测处
frame = canvas.create_rectangle(15, 50, 348, 307, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='实时图像界面', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=30, y=35)  # 标题位置
image = tkinter.Label(root_window, text='等待图像传入...')  # 图像
image.place(x=25, y=62, width=313, height=235)  # 图像位置

# 边缘检测处
frame = canvas.create_rectangle(363, 50, 685, 307, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='边缘检测界面', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=378, y=35)  # 标题位置
image = tkinter.Label(root_window, text='等待图像传入...')  # 图像
image.place(x=373, y=62, width=303, height=235)  # 图像位置

# 实时数据

# 表头
frame = canvas.create_rectangle(15, 330, 348, 440, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='实时数据面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=25, y=315)  # 标题位置

# 当前大蒜种粒检测结果
frame = canvas.create_rectangle(35, 354, 328, 380, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='当前大蒜种粒检测结果：', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=40, y=355)  # 提示位置
label_status_Label = tkinter.Label(root_window, text=label_status, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_status_Label.place(x=180, y=355)  # 内容位置

# 当前图像推理时间
frame = canvas.create_rectangle(35, 394, 328, 420, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='当前图像推理时间(s)：', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=40, y=395)  # 提示位置
label_status_Label = tkinter.Label(root_window, text=label_time, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_status_Label.place(x=170, y=395)  # 内容位置

# 实时边缘检测面板

# 表头
frame = canvas.create_rectangle(363, 330, 685, 440, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='实时连通域识别面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=373, y=315)  # 标题位置

# 当前连通域识别情况
frame = canvas.create_rectangle(383, 354, 665, 380, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='当前连通域识别情况：', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=355)  # 提示位置
label_status_Label = tkinter.Label(root_window, text=label_detect, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_status_Label.place(x=515, y=355)  # 内容位置

# 当前连通域数量
frame = canvas.create_rectangle(383, 394, 665, 420, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='当前连通域数量(个)：', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=395)  # 提示位置
label_status_Label = tkinter.Label(root_window, text=label_contor_sum, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_status_Label.place(x=510, y=395)  # 内容位置

# 统计数据面板

# 表头
frame = canvas.create_rectangle(700, 50, 1009, 275, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='统计数据面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=710, y=35)  # 标题位置

# 信息边框
frame = canvas.create_rectangle(720, 74, 989, 100, fill="", outline='black')  # 边框1
frame = canvas.create_rectangle(720, 114, 989, 140, fill="", outline='black')  # 边框2
frame = canvas.create_rectangle(720, 154, 989, 180, fill="", outline='black')  # 边框3
frame = canvas.create_rectangle(720, 194, 989, 220, fill="", outline='black')  # 边框4
frame = canvas.create_rectangle(720, 234, 989, 260, fill="", outline='black')  # 边框5

'''
# 创建大蒜的总数标签
imagename = tkinter.Label(root_window, text='大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=75)  # 提示位置
label_all_Label = tkinter.Label(root_window, text=label_all, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_all_Label.place(x=820, y=75)  # 内容位置


# 创建完整大蒜的总数标签
imagename = tkinter.Label(root_window, text='完整大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=115)  # 提示位置
label_all_Label = tkinter.Label(root_window, text=label_Healthy, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_all_Label.place(x=845, y=115)  # 内容位置


# 创建破损大蒜的总数标签
imagename = tkinter.Label(root_window, text='破损大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=155)  # 提示位置
label_all_Label = tkinter.Label(root_window, text=label_Breakage, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_all_Label.place(x=845, y=155)  # 内容位置

# 创建破损大蒜的总质量标签
imagename = tkinter.Label(root_window, text='破损大蒜的总质量(克):', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=305)  # 提示位置
label_all_Label = tkinter.Label(root_window, text=mass_Breakage, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_all_Label.place(x=858, y=305)  # 内容位置

# 创建其他大蒜的总数标签
imagename = tkinter.Label(root_window, text='其他大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=360)  # 提示位置
label_all_Label = tkinter.Label(root_window, text=label_Others, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_all_Label.place(x=845, y=360)  # 内容位置

# 创建其他大蒜的总质量标签
imagename = tkinter.Label(root_window, text='其他大蒜的总质量(克):', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=400)  # 提示位置
label_all_Label = tkinter.Label(root_window, text=mass_Others, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_all_Label.place(x=858, y=400)  # 内容位置

# 创建破损占比标签
imagename = tkinter.Label(root_window, text='破损占比(破损总数/总数)X100%:', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=455)  # 提示位置
label_rate_Label = tkinter.Label(root_window, text=label_rate, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_rate_Label.place(x=920, y=455)  # 内容位置

# 创建破损率标签
imagename = tkinter.Label(root_window, text='破损率(破损总质量/总质量)X100%:', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=495)  # 提示位置
mass_rate_Label = tkinter.Label(root_window, text=mass_rate, font='微软雅黑 10', bg="#CAD0DA")  # 内容
mass_rate_Label.place(x=935, y=495)  # 内容位置
'''
# 创建操作控制面板
# 表头
frame = canvas.create_rectangle(15, 460, 685, 584, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='操作控制面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=25, y=445)  # 标题位置


# 设计进度条滑块

def set_threshold_value(value):
    threshold_value = value
    print(threshold_value)

frame = canvas.create_rectangle(700, 300, 1009, 500, fill="", outline='black')  # 边框
imagename = tkinter.Label(root_window, text='操作控制面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=725, y=285)  # 标题位置

frame = canvas.create_rectangle(712, 317, 998, 378, fill="", outline='black')  # 边框
scale = tkinter.Scale(root_window,
             bg = "#CAD0DA",
             orient=tkinter.HORIZONTAL,
             #label='当前二值化阈值（1-255，值越小画面越亮）',
             from_=0,
             to= 255,
             length=265,
             tickinterval=255,       # 设置刻度滑动条的间隔
             command=set_threshold_value,
             show=0)
scale.set(value=60)
scale.place(x=720, y=325)
def button_click1():
    """显示/隐藏按钮"""

def button_click2():
    """摄像头切换按钮"""

def button_click3():
    """启动按钮"""

def button_click4():
    """停止按钮"""

def button_click5():
    """导出按钮"""

def button_click6():
    """退出按钮"""
    # 回收主窗口
    root_window.destroy()

# 创建显示按钮
button1 = tkinter.Button(root_window, text="显示 / 隐藏", bg="#FF68B4", font='18', relief=tkinter.SOLID,
                         command=button_click1)
button1.place(x=26, y=485, width=140, height=80)

# 创建隐藏按钮
button2 = tkinter.Button(root_window, text="切换摄像头", bg="#FFFF00", font='12', relief=tkinter.SOLID,
                         command=button_click2)
button2.place(x=196, y=485, width=140, height=80)

# 创建启动按钮
button3 = tkinter.Button(root_window, text="  启 动  ", bg="#0000FF", font='12', relief=tkinter.SOLID,
                         command=button_click3)
button3.place(x=366, y=485, width=140, height=80)

# 创建停止按钮
button4 = tkinter.Button(root_window, text="  停 止  ", bg="#FF0000", font='12', relief=tkinter.SOLID,
                         command=button_click4)
button4.place(x=536, y=485, width=140, height=80)

# 创建导出按钮
button5 = tkinter.Button(root_window, text="≡ 导出数据", bg='#CAE1EE', relief=tkinter.SOLID,
                         command=button_click5)
button5.place(x=0, y=0, width=90, height=33)

# 创建退出按钮
exit_button = tkinter.Button(root_window, text="X", bg="#FC9D9A", relief=tkinter.SOLID,
                             command=button_click6)
exit_button.place(x=991, y=0, width=33, height=33)

def button_click():
    """ 点击"开始"按钮. """
    global flag_start
    flag_start = True
    # 回收启动界面背景图片和启动界面两个按钮
    imagestart.destroy()
    buttonstart.destroy()
    buttonexit.destroy()

photo = Image.open("start.jpg")
photo = ImageTk.PhotoImage(photo)
imagestart = tkinter.Label(root_window, text='等待图像传入...', image=photo)
imagestart.place(x=0, y=0, width=1024, height=600)

# 创建“开始”按钮
buttonstart = tkinter.Button(root_window, text="开 始", font='微软雅黑 19', bg="#7FFFD4", borderwidth=1,
                                 relief=tkinter.SOLID, command=button_click)
buttonstart.place(x=312, y=420, width=115, height=65)

# 创建“退出”按钮
buttonexit = tkinter.Button(root_window, text="退 出", font='微软雅黑 19', bg="#FF7777", borderwidth=1,
                                relief=tkinter.SOLID, command=root_window.destroy)
buttonexit.place(x=592, y=420, width=115, height=65)



root_window.mainloop()