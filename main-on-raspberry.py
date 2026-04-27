import tkinter
import cv2
import numpy as np
import time
import onnxruntime as ort
from PIL import Image, ImageTk
import os
import serial

CLASS_NAMES = {
    0: 'Healthy',  
    1: 'Breakage',  
    2: 'Others'    
}


 
class YOLO8:
    def __init__(self, onnx_model, input_image, confidence_thres, iou_thres):
        self.onnx_model = onnx_model
        self.input_image = input_image
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres
        self.classes = CLASS_NAMES
 
    def preprocess(self):
        self.img = self.input_image
        self.img_height, self.img_width = self.img.shape[:2]
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img = cv2.convertScaleAbs(img, alpha=2.0, beta=0)
        img, self.ratio, (self.dw, self.dh) = self.letterbox(img, new_shape=(self.input_width, self.input_height))
        image_data = np.array(img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        return image_data
 
 
    def letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True):
        shape = img.shape[:2]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1]) 
        if not scaleup: 
            r = min(r, 1.0)
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1] 
        dw /= 2 
        dh /= 2
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh)), int(round(dh))
        left, right = int(round(dw)), int(round(dw))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return img, (r, r), (dw, dh)
 
    def postprocess(self, input_image, output):
        outputs = np.transpose(np.squeeze(output[0]))
        rows = outputs.shape[0]
        boxes, scores, class_ids = [], [], []
        ratio = self.img_width / self.input_width, self.img_height / self.input_height 
        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            if max_score >= self.confidence_thres:
                class_id = np.argmax(classes_scores)
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                x -= self.dw  
                y -= self.dh
                x /= self.ratio[0]  
                y /= self.ratio[1]
                w /= self.ratio[0]
                h /= self.ratio[1]
                left = int(x - w / 2)
                top = int(y - h / 2)
                width = int(w)
                height = int(h) 
                boxes.append([left, top, width, height])
                scores.append(max_score)
                class_ids.append(class_id)
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)
        return input_image, indices, boxes, scores, class_ids
 
    def draw_detections(self, img, box, score, class_id, color):
        x1, y1, w, h = box
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        label = f"{self.classes[class_id]}: {score:.2f}"
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
        cv2.rectangle(img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color, cv2.FILLED)
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def main(self):
        session = ort.InferenceSession(
            self.onnx_model, 
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"] if ort.get_device() == "GPU" else ["CPUExecutionProvider"],
        )
        print("YOLO8 目标检测 ONNXRuntime")
        print("模型名称：", self.onnx_model)
        
        model_inputs = session.get_inputs()
        input_shape = model_inputs[0].shape  
        self.input_width = input_shape[2]
        self.input_height = input_shape[3]
        print(f"模型输入尺寸：宽度 = {self.input_width}, 高度 = {self.input_height}")
        img_data = self.preprocess()
        outputs = session.run(None, {model_inputs[0].name: img_data})
        return self.postprocess(self.img, outputs)  
    
def Filter(contours):
    a_sum = 0  
    Sarea = 0  
    a = [] 
    for i, area in enumerate(contours):
        if cv2.contourArea(area) > 400:
            Sarea = max(Sarea, cv2.contourArea(area))
            a.append(contours[i])
            a_sum += 1
    return a_sum, a, Sarea

def UART_Send(msg):
    ser = serial.Serial('/dev/ttyAMA0', 9600)
    ser.write(str(msg).encode())

def camera_detect():
    global flag_det  
    global flag_set  
    global flag_start  
    global flag_runStop  
    
    global label_status 
    global label_time
    global label_detect
    global label_contour_sum
    global label_all
    
    global label_Healthy 
    global label_Breakage 
    global label_Others 
    global label_rate
    
    global show_status  
    global detect_status  
    global status_to_clear  
    
    global threshold_value
    
    global database
    

    flag_det = False 
    flag_set = False 
    flag_start = False
    flag_runStop = False  

    label_status = "......"
    label_time = 0
    label_detect = '不存在'
    label_contour_sum = 0
    label_all = label_Healthy = label_Breakage = label_Others = 0
    label_rate = "...%"
    
    show_status = False  
    detect_status = False  
    status_to_clear = False  
    
    threshold_value = 60
    
    database = np.array(
        [['Result', 'H_Num', 'B_Num', 'O_Num', 'Total', 'N_Rate']])
    
    root_window = tkinter.Tk()
    root_window.title('大蒜破损率检测系统')
    root_window.geometry('1024x600')
    root_window.resizable(False,False)
    root_window['background'] = '#808080'
    root_window.attributes('-fullscreen', True) 
    canvas = tkinter.Canvas(root_window, bg="#CAD0DA", bd="0")  
    canvas.place(x=0, y=0, width=1024, height=600) 

    frame = canvas.create_rectangle(0, 0, 1024, 33, fill='#87CEEB', outline='black')
    imagename = tkinter.Label(root_window, text='大 蒜 破 损 率 鉴 定 系 统', font='微软雅黑 14', bg='#87CEEB') 
    imagename.place(x=404, y=2) 

    frame = canvas.create_rectangle(15, 50, 348, 307, fill="", outline='black')  
    imagename = tkinter.Label(root_window, text='实时图像界面', font='微软雅黑 12', bg="#CAD0DA") 
    imagename.place(x=30, y=35) 
    image = tkinter.Label(root_window, text='等待图像传入waiting...')  
    image.place(x=25, y=62, width=313, height=235)  

    frame = canvas.create_rectangle(363, 50, 685, 307, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='边缘检测界面', font='微软雅黑 12', bg="#CAD0DA")
    imagename.place(x=378, y=35) 
    image_edge = tkinter.Label(root_window, text='等待图像传入...')  
    image_edge.place(x=373, y=62, width=303, height=235)  

    frame = canvas.create_rectangle(15, 330, 348, 440, fill="", outline='black')  
    imagename = tkinter.Label(root_window, text='实时数据面板', font='微软雅黑 12', bg="#CAD0DA")
    imagename.place(x=25, y=315) 

    frame = canvas.create_rectangle(35, 354, 328, 380, fill="", outline='black')
    imagename = tkinter.Label(root_window, text='当前大蒜种粒检测结果：', font='微软雅黑 10', bg="#CAD0DA")
    imagename.place(x=40, y=355)  
    label_status_Label = tkinter.Label(root_window, text=label_status, font='微软雅黑 10', bg="#CAD0DA") 
    label_status_Label.place(x=180, y=355)  

    frame = canvas.create_rectangle(35, 394, 328, 420, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='当前图像推理时间(s)：', font='微软雅黑 10', bg="#CAD0DA")  
    imagename.place(x=40, y=395) 
    label_time_Label = tkinter.Label(root_window, text=label_time, font='微软雅黑 10', bg="#CAD0DA")
    label_time_Label.place(x=170, y=395) 

    frame = canvas.create_rectangle(363, 330, 685, 440, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='实时连通域识别面板', font='微软雅黑 12', bg="#CAD0DA") 
    imagename.place(x=373, y=315) 

    frame = canvas.create_rectangle(383, 354, 665, 380, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='当前连通域识别情况：', font='微软雅黑 10', bg="#CAD0DA")
    imagename.place(x=388, y=355)  
    label_detect_Label = tkinter.Label(root_window, text=label_detect, font='微软雅黑 10', bg="#CAD0DA") 
    label_detect_Label.place(x=515, y=355) 

    frame = canvas.create_rectangle(383, 394, 665, 420, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='当前连通域数量(个)：', font='微软雅黑 10', bg="#CAD0DA") 
    imagename.place(x=388, y=395)  
    label_num_Label = tkinter.Label(root_window, text=label_contour_sum, font='微软雅黑 10', bg="#CAD0DA") 
    label_num_Label.place(x=512, y=395)  

    frame = canvas.create_rectangle(700, 50, 1009, 285, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='统计数据面板', font='微软雅黑 12', bg="#CAD0DA") 
    imagename.place(x=710, y=35) 

    frame = canvas.create_rectangle(720, 74, 989, 100, fill="", outline='black')  
    frame = canvas.create_rectangle(720, 114, 989, 140, fill="", outline='black')  
    frame = canvas.create_rectangle(720, 154, 989, 180, fill="", outline='black')  
    frame = canvas.create_rectangle(720, 194, 989, 220, fill="", outline='black') 
    frame = canvas.create_rectangle(720, 234, 989, 260, fill="", outline='black') 

    imagename = tkinter.Label(root_window, text='大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  
    imagename.place(x=725, y=75)  
    label_all_Label = tkinter.Label(root_window, text=label_all, font='微软雅黑 10', bg="#CAD0DA") 
    label_all_Label.place(x=820, y=75)

    imagename = tkinter.Label(root_window, text='完整大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA") 
    imagename.place(x=725, y=115)  
    label_Healthy_Label = tkinter.Label(root_window, text=label_Healthy, font='微软雅黑 10', bg="#CAD0DA")  
    label_Healthy_Label.place(x=845, y=115)  

    imagename = tkinter.Label(root_window, text='破损大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  
    imagename.place(x=725, y=155)  
    label_Breakage_Label = tkinter.Label(root_window, text=label_Breakage, font='微软雅黑 10', bg="#CAD0DA") 
    label_Breakage_Label.place(x=845, y=155) 

    imagename = tkinter.Label(root_window, text='其他大蒜的总数(个):', font='微软雅黑 10', bg="#CAD0DA")  
    imagename.place(x=725, y=195) 
    label_Others_Label = tkinter.Label(root_window, text=label_Others, font='微软雅黑 10', bg="#CAD0DA") 
    label_Others_Label.place(x=845, y=195)  

    imagename = tkinter.Label(root_window, text='破损率(破损总数/总数)X100%:', font='微软雅黑 10', bg="#CAD0DA")
    imagename.place(x=725, y=235) 
    label_rate_Label = tkinter.Label(root_window, text=label_rate, font='微软雅黑 10', bg="#CAD0DA") 
    label_rate_Label.place(x=920, y=235)  

    def set_threshold_value(value):
        global threshold_value
        threshold_value = value
        label_thres_Label.configure(text = threshold_value)
        
    frame = canvas.create_rectangle(700, 310, 1009, 510, fill="", outline='black')  
    imagename = tkinter.Label(root_window, text='操作控制面板2', font='微软雅黑 12', bg="#CAD0DA")  
    imagename.place(x=725, y=295) 

    frame = canvas.create_rectangle(712, 335, 995, 398, fill="", outline='black')  
    scale = tkinter.Scale(root_window,
                 bg = "#CAD0DA",
                 orient=tkinter.HORIZONTAL,
                 from_=0,
                 to= 255,
                 showvalue=False,
                 length=265,
                 tickinterval=255,   
                 command=set_threshold_value,)
    scale.set(value=60)
    scale.place(x=720, y=345)
    
    frame = canvas.create_rectangle(712, 425, 995, 450, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='二值化阈值:', font='微软雅黑 10', bg="#CAD0DA")  
    imagename.place(x=725, y=426) 
    label_thres_Label = tkinter.Label(root_window, text=threshold_value, font='微软雅黑 10', bg="#CAD0DA") 
    label_thres_Label.place(x=805, y=426) 

    frame = canvas.create_rectangle(15, 460, 685, 584, fill="", outline='black') 
    imagename = tkinter.Label(root_window, text='操作控制面板1', font='微软雅黑 12', bg="#CAD0DA")
    imagename.place(x=25, y=445) 

    def button_click1():
        """显示按钮"""
        global show_status
        show_status = True

    def button_click2():
        global show_status
        show_status = False

    def button_click3():
        UART_Send("R")

    def button_click4():
        UART_Send("S")

    def button_click5():
        t = time.localtime()
        filename = 'data/savedata_%s_%s.txt' %(str(t.tm_year)+str(t.tm_mon).zfill(2)+str(t.tm_mday).zfill(2), str(t.tm_hour).zfill(2)+str(t.tm_min).zfill(2)+str(t.tm_sec).zfill(2))
        if 'data' not in os.listdir():
            os.mkdir('data')
        np.savetxt(filename, database, delimiter='\t', fmt='%s',)

    def button_click6():
        root_window.destroy()

    button1 = tkinter.Button(root_window, text="  显 示  ", bg="#FF68B4", font='18', relief=tkinter.SOLID,
                             command=button_click1)
    button1.place(x=26, y=485, width=140, height=80)

    button2 = tkinter.Button(root_window, text="  隐 藏  ", bg="#FFFF00", font='12', relief=tkinter.SOLID,
                         command=button_click2)
    button2.place(x=196, y=485, width=140, height=80)

    button3 = tkinter.Button(root_window, text="  启 动  ", bg="#0000FF", font='12', relief=tkinter.SOLID,
                         command=button_click3)
    button3.place(x=366, y=485, width=140, height=80)

    button4 = tkinter.Button(root_window, text="  停 止  ", bg="#FF0000", font='12', relief=tkinter.SOLID,
                         command=button_click4)
    button4.place(x=536, y=485, width=140, height=80)

    button5 = tkinter.Button(root_window, text="≡ 导出数据", bg='#CAE1EE', relief=tkinter.SOLID,
                         command=button_click5)
    button5.place(x=0, y=0, width=90, height=33)

    exit_button = tkinter.Button(root_window, text="X", bg="#FC9D9A", relief=tkinter.SOLID,
                                 command=button_click6)
    exit_button.place(x=991, y=0, width=33, height=33)

    for video_index in range(0, 50):
        video = cv2.VideoCapture(video_index)
        if video.isOpened():
            print("%d is Yes" % video_index)
            break 
    
    def imdetect():
        model = 'best.onnx'

        global flag_det  
        global flag_set 
        global flag_start  
        global flag_runStop
        global label_status
        global label_time
        global label_detect 
        global label_contour_sum
        global label_all
        global label_Healthy
        global label_Breakage
        global label_Others
        global label_rate
    
        global show_status 
        global detect_status 
        global status_to_clear  
        
        global threshold_value
        
        global database
        
        if flag_start:
            res, img = video.read() 
            if res:
                cropped_image = img[0:480, 0:320]  
                cropped_image = cv2.flip(cropped_image, 1)
                cropped_image = cv2.flip(cropped_image, 1)
                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                img_median = cv2.medianBlur(gray, 5)
                ret2, thresh2 = cv2.threshold(img_median, int(threshold_value), 255, cv2.THRESH_BINARY)
                contours, hirearchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                a_sum, contours_1, area = Filter(contours)
                if a_sum > 0:
                    label_detect = "存在"
                    detect_status = True
                else:
                    label_detect = "不存在"
                    detect_status = False
                
                if detect_status != status_to_clear:
                    if detect_status:
                        flag_det = True
                status_to_clear = detect_status
                
                edge_img = img
                edge_img = cv2.flip(edge_img, 1)
                edge_img = cv2.flip(edge_img, 1)
                edge_gray = cv2.cvtColor(edge_img, cv2.COLOR_BGR2GRAY)
                edge_img_median = cv2.medianBlur(gray, 5)
                edge_ret2, edge_thresh2 = cv2.threshold(img_median, int(threshold_value), 255, cv2.THRESH_BINARY)
                edge_contours, edge_hirearchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                edge_a_sum, edge_contours_1, edge_area = Filter(edge_contours)
                
                if flag_det:
                    detection = YOLO8(model, img, confidence_thres=0.5, iou_thres=0.45)
                    t1 = time.time()
                    output_image, indices, boxes, scores, class_ids = detection.main()
                    t2 = time.time()
                    label_time = "%.2f" % (t2 - t1)
                    
                    for i in indices:
                        box = boxes[i]
                        score = scores[i]
                        class_id = class_ids[i]
                        label = f"{detection.classes[class_id]}"
                        
                        if label == "Healthy":
                            flag_set = True
                            label_status = "完整"
                            label_Healthy += 1
                            detection.draw_detections(img, box, score, class_id, color = (255, 255, 0))
                            UART_Send("H")
                            
                        if label == "Breakage":
                            flag_set = True
                            label_status = "破损"
                            label_Breakage += 1
                            detection.draw_detections(img, box, score, class_id, color = (0, 255, 255))
                            UART_Send('B')
                            
                        if label == "Others":
                            flag_set = True
                            label_status = "其他"
                            label_Others += 1
                            detection.draw_detections(img, box, score, class_id, color = (255, 0, 255))
                            UART_Send('O')
                            
                    str_FPS = "FPS: %.2f" % (1. / (t2 - t1))
                    cv2.putText(output_image, str_FPS, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
                
                lb_rate = ms_rate = "0"
                label_all = label_Healthy + label_Breakage + label_Others
                
                if label_all > 0:
                    lb_rate = "%.1f" % (label_Breakage * 100 / label_all)
                    label_rate = "%.1f" % (label_Breakage * 100 / label_all) + "%"
                if label_rate == "100.0%":
                    label_rate = "100%"

                label_status_Label.configure(text=label_status)
                label_time_Label.configure(text=label_time)
                label_detect_Label.configure(text=label_detect)
                label_num_Label.configure(text=a_sum)
                label_all_Label.configure(text=label_all)
                label_Healthy_Label.configure(text=label_Healthy)
                label_Breakage_Label.configure(text=label_Breakage)
                label_Others_Label.configure(text=label_Others)
                label_rate_Label.configure(text=label_rate)
                
                if flag_set:
                    edge_img = cv2.drawContours(edge_img, edge_contours_1, -1, (0, 0, 255), 3)
                    edge_img = cv2.resize(edge_img, (303, 235))
                    edge_img = cv2.cvtColor(edge_img, cv2.COLOR_BGR2RGBA)
                    edge_img = Image.fromarray(edge_img)
                    edge_img = ImageTk.PhotoImage(edge_img)
                    image_edge.image = edge_img
                    image_edge['image'] = edge_img
                    data_new = np.array(
                        [label_status, label_Healthy, label_Breakage, label_Others, label_all, label_rate])
                    database = np.r_[database, [data_new]]

                if show_status:
                    col_img = cv2.cvtColor(thresh2, cv2.COLOR_GRAY2RGB)
                    col_img = cv2.drawContours(col_img, contours_1, -1, (250, 10, 250), 2)
                    cv2.rectangle(img, (320, 0), (320, 480), (250, 10, 250), cv2.FILLED)
                    img[0:480, 0:320] = col_img

                img = cv2.resize(img, (313, 235))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(img)
                image.image = img
                image['image'] = img
                
            flag_det = False
            flag_set = False

        root_window.after(1, imdetect)


    def button_click():
        global flag_start
        flag_start = True
        imagestart.destroy()
        buttonstart.destroy()
        buttonexit.destroy()

    photo = Image.open("Start.jpg")
    photo = ImageTk.PhotoImage(photo)
    imagestart = tkinter.Label(root_window, text='等待图像传入...', image=photo)
    imagestart.place(x=0, y=0, width=1024, height=600)

    buttonstart = tkinter.Button(root_window, text="开 始", font='微软雅黑 19', bg="#7FFFD4", borderwidth=1,
                                 relief=tkinter.SOLID, command=button_click)
    buttonstart.place(x=312, y=420, width=115, height=65)

    buttonexit = tkinter.Button(root_window, text="退 出", font='微软雅黑 19', bg="#FF7777", borderwidth=1,
                                relief=tkinter.SOLID, command=root_window.destroy)
    buttonexit.place(x=592, y=420, width=115, height=65)

    imdetect()
    
    root_window.mainloop()
    
if __name__ == "__main__":
    camera_detect()
