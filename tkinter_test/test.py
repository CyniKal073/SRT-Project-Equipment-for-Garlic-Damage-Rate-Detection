from tkinter import *
# 创建主窗口
win =Tk()
win.title("控制管理界面")
win.geometry('400x250')
# 添加一个 Scale 控件，默认垂直方向，步长设置为 5，长度为200，滑动块的大小为 50，最后使用label参数文本
s=Scale(win, from_ =100, to =0,resolution =5,length =200,sliderlength= 20,label ='音量控制' )
s.pack()
# 设置滑块的位置
s.set(value=15)
# 显示窗口
mainloop()