import tkinter
from tkinter import messagebox
from multiprocessing import Process, Value, Lock
import numpy as np
from PIL import Image, ImageTk


global flag_det  # 启用识别的标志
global flag_set  # 麦粒通过的标志
global flag_start  # 系统启动的标志
global flag_runStop  # 传送带运行和停止的标志

global label_status  # 当前通过麦粒的鉴定结果
global mass_now  # 当前通过麦粒的质量
global label_time  # 当前图像的推理时间
global label_detect  # 连通域的识别情况
global label_all  # 麦粒的总数
global mass_all  # 麦粒的总质量
global label_Healthy  # 完整的麦粒总数
global mass_Healthy  # 完整的麦粒总质量
global label_Breakage  # 破损的麦粒总数
global mass_Breakage  # 破损的麦粒总质量
global label_rate  # 破损占比
global mass_rate  # 破损率
global matrix_data  # 系统运行数据

global show_status  # 识别线显示/隐藏
global detect_status  # 保存当前连通域识别情况
global status_to_clear  # 保存上一次连通域识别情况

# 变量初始化
flag_det = False  # 默认不启用模型识别
flag_set = False  # 默认麦粒不通过
flag_start = False  # 初始系统不启动，等待“开始”按钮按下
flag_runStop = False  # 默认传送带静止

show_status = False  # 默认不显示识别线
detect_status = False  # 默认连通域不存在
status_to_clear = False  # 默认上一次连通域不存在

label_detect = "不存在"
label_status = "......"
label_rate = mass_rate = "...%"
mass_all = mass_Breakage = mass_Healthy = mass_now = 0
label_all = label_Healthy = label_Breakage = label_time = 0

# 保存顺序为 : 当前麦粒结果，当前麦粒质量，完整麦粒数目，完整麦粒质量，破损麦粒数目，破损麦粒质量，总数目，总质量，破损占比，破损率
matrix_data = np.array(
    [["Result", "C_Mass", "H_Num", "H_Mass", "B_Num", "B_Mass", "A_Num", "A_Mass", "N_Rate", "M_Rate"]])

# 创建共享内存对象（光照）和锁
light_val = Value('i', 0)
lock = Lock()

# ========================================创建一个TK界面========================================
root = tkinter.Tk()
root.geometry("1024x600")  # 设置窗口大小
root["background"] = "#E6EFF9"  # 设置背景颜色
root.resizable(False, False)  # 禁止调整窗口大小
root.title('麦粒破损率鉴定系统')  # 设置窗口标题
#root.attributes('-fullscreen', True)  # 设置全屏模式
canvas = tkinter.Canvas(root, bg="#CAD0DA", bd="0")  # 设置画布背景颜色
canvas.place(x=0, y=0, width=1024, height=600)  # 设置画布位置和大小

# ========================================创建标题栏标签========================================
frame = canvas.create_rectangle(0, 0, 1024, 30, fill='#CAE1FF', outline='black')  # 边框
imagename = tkinter.Label(root, text='麦 粒 破 损 率 鉴 定 系 统', font='微软雅黑 14', bg='#CAE1FF')  # 标题
imagename.place(x=404, y=1)  # 标题位置

# ======================================创建实时图像界面标签======================================
frame = canvas.create_rectangle(15, 50, 348, 307, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='实时图像界面', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=30, y=35)  # 标题位置
image = tkinter.Label(root, text='等待图像传入...')  # 图像
image.place(x=25, y=62, width=313, height=235)  # 图像位置

# ======================================创建分选图像界面标签======================================
frame = canvas.create_rectangle(15, 327, 348, 584, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='分选图像界面', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=30, y=312)  # 标题位置
images = tkinter.Label(root, text='等待图像传入...')  # 图像
images.place(x=25, y=339, width=313, height=235)  # 图像位置

# ======================================创建边缘检测界面标签======================================
frame = canvas.create_rectangle(363, 50, 685, 307, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='边缘检测界面', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=373, y=35)  # 标题位置
image_con = tkinter.Label(root, text='等待图像传入...')  # 图像
image_con.place(x=373, y=62, width=303, height=235)  # 图像位置

# ======================================创建实时数据面板标签======================================
frame = canvas.create_rectangle(363, 327, 685, 584, fill="", outline='black')  # 边框
frame = canvas.create_rectangle(363, 480, 685, 584, fill="", outline='black')  # 分割边框
imagename = tkinter.Label(root, text='实时数据面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=373, y=312)  # 标题位置

# 创建当前通过麦粒的鉴定结果标签
frame = canvas.create_rectangle(383, 355, 665, 380, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='当前通过麦粒的鉴定结果:', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=356)  # 提示位置
label_status_Label = tkinter.Label(root, text=label_status, font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_status_Label.place(x=566, y=356)  # 内容位置

# 创建当前通过麦粒的质量标签
frame = canvas.create_rectangle(383, 395, 665, 420, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='当前通过麦粒的质量(克):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=396)  # 提示位置
mass_now_Label = tkinter.Label(root, text=mass_now, font='微软雅黑 11', bg="#CAD0DA")  # 内容
mass_now_Label.place(x=560, y=396)  # 内容位置

# 创建当前图像的推理时间标签
frame = canvas.create_rectangle(383, 435, 665, 460, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='当前图像的推理时间(s):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=436)  # 提示位置
label_time_Label = tkinter.Label(root, text=label_time, font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_time_Label.place(x=555, y=436)  # 内容位置

# 创建当前连通域的识别情况标签
frame = canvas.create_rectangle(383, 500, 665, 525, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='当前连通域的识别情况:', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=501)  # 提示位置
label_detect_Label = tkinter.Label(root, text=label_detect, font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_detect_Label.place(x=550, y=501)  # 内容位置

# 创建当前连通域的数量标签
frame = canvas.create_rectangle(383, 540, 665, 565, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='当前连通域的数量(个):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=388, y=541)  # 提示位置
label_num_Label = tkinter.Label(root, text="0", font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_num_Label.place(x=548, y=541)  # 内容位置

# ======================================创建统计数据面板标签======================================
frame = canvas.create_rectangle(700, 50, 1009, 483, fill="", outline='black')  # 边框
frame = canvas.create_rectangle(700, 158, 1009, 483, fill="", outline='black')  # 分割边框1
frame = canvas.create_rectangle(700, 253, 1009, 483, fill="", outline='black')  # 分割边框2
frame = canvas.create_rectangle(700, 348, 1009, 483, fill="", outline='black')  # 分割边框3
imagename = tkinter.Label(root, text='统计数据面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=710, y=35)  # 标题位置

# 创建麦粒的总数标签
frame = canvas.create_rectangle(720, 78, 989, 103, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='麦粒的总数(个):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=79)  # 提示位置
label_all_Label = tkinter.Label(root, text=label_all, font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_all_Label.place(x=837, y=79)  # 内容位置

# 创建麦粒的总质量标签
frame = canvas.create_rectangle(720, 118, 989, 143, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='麦粒的总质量(克):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=119)  # 提示位置
mass_all_Label = tkinter.Label(root, text=mass_all, font='微软雅黑 11', bg="#CAD0DA")  # 内容
mass_all_Label.place(x=852, y=119)  # 内容位置

# 创建完整的麦粒总数标签
frame = canvas.create_rectangle(720, 173, 989, 198, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='完整的麦粒总数(个):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=174)  # 提示位置
label_Healthy_Label = tkinter.Label(root, text=label_Healthy, font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_Healthy_Label.place(x=867, y=174)  # 内容位置

# 创建完整的麦粒总质量标签
frame = canvas.create_rectangle(720, 213, 989, 238, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='完整的麦粒总质量(克):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=214)  # 提示位置
mass_Healthy_Label = tkinter.Label(root, text=mass_Healthy, font='微软雅黑 11', bg="#CAD0DA")  # 内容
mass_Healthy_Label.place(x=881, y=214)  # 内容位置

# 创建破损的麦粒总数标签
frame = canvas.create_rectangle(720, 268, 989, 293, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='破损的麦粒总数(个):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=269)  # 提示位置
label_Breakage_Label = tkinter.Label(root, text=label_Breakage, font='微软雅黑 11', bg="#CAD0DA")  # 内容
label_Breakage_Label.place(x=867, y=269)  # 内容位置

# 创建破损的麦粒总质量标签
frame = canvas.create_rectangle(720, 308, 989, 333, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='破损的麦粒总质量(克):', font='微软雅黑 11', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=309)  # 提示位置
mass_Breakage_Label = tkinter.Label(root, text=mass_Breakage, font='微软雅黑 11', bg="#CAD0DA")  # 内容
mass_Breakage_Label.place(x=881, y=309)  # 内容位置

# 创建破损占比标签
frame = canvas.create_rectangle(720, 363, 989, 388, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='破损占比(破损总数/总数)X100%:', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=364)  # 提示位置
label_rate_Label = tkinter.Label(root, text=label_rate, font='微软雅黑 10', bg="#CAD0DA")  # 内容
label_rate_Label.place(x=925, y=364)  # 内容位置

# 创建破损率标签
frame = canvas.create_rectangle(720, 403, 989, 428, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='破损率(破损总质量/总质量)X100%:', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=404)  # 提示位置
mass_rate_Label = tkinter.Label(root, text=mass_rate, font='微软雅黑 10', bg="#CAD0DA")  # 内容
mass_rate_Label.place(x=939, y=404)  # 内容位置

# 创建环境光照强度标签
frame = canvas.create_rectangle(720, 443, 989, 468, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='环境光照强度（0-100）:', font='微软雅黑 10', bg="#CAD0DA")  # 提示
imagename.place(x=725, y=444)  # 提示位置
light_Label = tkinter.Label(root, text=light_val.value, font='微软雅黑 10', bg="#CAD0DA")  # 内容
light_Label.place(x=876, y=444)  # 内容位置

# ======================================创建操作控制面板标签======================================
frame = canvas.create_rectangle(700, 505, 1009, 584, fill="", outline='black')  # 边框
imagename = tkinter.Label(root, text='操作控制面板', font='微软雅黑 12', bg="#CAD0DA")  # 标题
imagename.place(x=710, y=490)  # 标题位置


def button_click1():
    """ 显隐按钮. """
    global show_status
    # 显隐识别线标志位翻转，为下一次点击做准备
    show_status = not show_status


def button_click2():
    """ 启停按钮. """
    global flag_runStop
    # 传送带启停标志位翻转，为下一次点击做准备
    flag_runStop = not flag_runStop
    if flag_runStop:
        # 传送带电机启动
        UART_Send("R")
    else:
        # 传送带电机停止
        UART_Send("S")


def button_click3():
    """ 导出按钮. """
    global matrix_data
    filepath = 'data'
    # 检查'data'文件夹下是否存在，若不存在则创建一个'data'文件夹
    if not os.path.isdir(filepath):
        os.makedirs(filepath)
    # 检查路径是否重复，若重复在后面加上数字
    filename = check_filename_available('data.txt')
    # 采用制表符分割，导出matrix_data为txt文本到'data'文件夹下
    np.savetxt(filename, matrix_data, delimiter='\t', fmt='%s')
    # 提示用户已经导出
    messagebox.showinfo('提示', '已成功导出到' + filename + '！')


def button_click4():
    """ 退出按钮. """
    # 回收主窗口
    root.destroy()
    # 下电前停止传送带
    UART_Send("S")


# 创建显隐按钮
button1 = tkinter.Button(root, text="显示 / 隐藏", bg="#FFFFE0", font='12', relief=tkinter.SOLID,
                         command=button_click1)
button1.place(x=723, y=515, width=120, height=60)

# 创建启停按钮
button2 = tkinter.Button(root, text="启动 / 停止", bg="#FFF5EE", font='12', relief=tkinter.SOLID,
                         command=button_click2)
button2.place(x=866, y=515, width=120, height=60)

# 创建导出按钮
button3 = tkinter.Button(root, text="≡ 导出数据", bg='#CAE1EE', relief=tkinter.SOLID, command=button_click3)
button3.place(x=0, y=0, width=90, height=30)

# 创建退出按钮
exit_button = tkinter.Button(root, text="X", bg="#FC9D9A", relief=tkinter.SOLID, command=button_click4)
exit_button.place(x=994, y=0, width=30, height=30)


def button_click():
    """ 点击"开始"按钮. """
    global flag_start
    flag_start = True
    # 回收启动界面背景图片和启动界面两个按钮
    imagestart.destroy()
    buttonstart.destroy()
    buttonexit.destroy()

photo = Image.open("Start.jpg")
photo = ImageTk.PhotoImage(photo)
imagestart = tkinter.Label(root, text='等待图像传入...', image=photo)
imagestart.place(x=0, y=0, width=1024, height=600)

# 创建“开始”按钮
buttonstart = tkinter.Button(root, text="开 始", font='微软雅黑 19', bg="#7FFFD4", borderwidth=1,
                                 relief=tkinter.SOLID, command=button_click)
buttonstart.place(x=312, y=420, width=115, height=65)

# 创建“退出”按钮
buttonexit = tkinter.Button(root, text="退 出", font='微软雅黑 19', bg="#FF7777", borderwidth=1,
                                relief=tkinter.SOLID, command=root.destroy)
buttonexit.place(x=592, y=420, width=115, height=65)



# 启动Tk界面
root.mainloop()
