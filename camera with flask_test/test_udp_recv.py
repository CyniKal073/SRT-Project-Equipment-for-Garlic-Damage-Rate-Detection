import socket
import cv2
import numpy as np



udp_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 确定通信协议类型

recv_addr = ('0.0.0.0', 31111)
udp_socket.bind(recv_addr)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

udp_socket.setblocking(0)  # 设置为非阻塞模式
def recv_img():
    while True:
        try:
            recv_byte, send_addr = udp_socket.recvfrom(921600)
            nparr = np.fromstring(recv_byte, dtype='uint8', sep='')  # 化为数组
            print(nparr)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # 解码为彩色图
            cv2.imshow('CyniKal', img)
        except BlockingIOError as error:
            pass
        x=cv2.waitKey(1)
        if x==ord('s'):
            break

recv_img()

cv2.destroyAllWindows()
udp_socket.close()

'''  # 用于test文件接收
with open('D:/888.txt','wb') as file:
        data,send_addr=udp_socket.recvfrom(max_chunk_size)
        file.write(data)
udp_socket.close()
'''
