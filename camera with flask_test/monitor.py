
import numpy as np
import cv2
from socket import *
from flask import Flask, Response


s = socket(AF_INET, SOCK_DGRAM) # 创建UDP套接字
addr = ('0.0.0.0', 8081)  # 0.0.0.0表示本机
s.bind(addr)

s.setblocking(0) # 设置为非阻塞模式

def gen():
    while True:
        data = None
        try:
            data, _ = s.recvfrom(921600)
            receive_data = np.frombuffer(data, dtype='uint8')
            r_img = cv2.imdecode(receive_data, 1)
            image = cv2.imencode('.jpg', r_img)[1].tobytes()
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'

        except BlockingIOError as e:
            pass


if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    def index():
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0', port=1212)







