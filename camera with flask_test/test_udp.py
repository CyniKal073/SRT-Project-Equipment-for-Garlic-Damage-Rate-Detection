import socket
import cv2
import numpy as np



udp_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #确定通信协议类型

recv_addr = ('127.0.0.1', 8081)


capture = cv2.VideoCapture(0)  # 0为电脑内置摄像头

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 设置每帧图片的宽
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 设置每帧图片的高

while True:
    ret, frame = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
    frame = cv2.flip(frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
    img_encode = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 50])[1]  # 对每帧图进行编码,压缩画质
    #cv2.imshow('CyniKal', frame)
    data = np.array(img_encode)
    byte_encode = data.tobytes()
    data_len = str(len(byte_encode))
    cv2.waitKey(60)
    '''
    x = cv2.waitKey(50)
    if x == ord('s'):
        break
    '''
    print('照片大小为%s字节'%data_len)

    udp_socket.sendto(byte_encode, recv_addr)

udp_socket.close()



'''    # 用于test文件传输
with open('C:/Users/admin/Desktop/666.txt','rb') as file:
    while True:
        data=file.read(1024)
        if not data:
            break
        udp_socket.sendto(data,recv_addr)

udp_socket.close()
'''



