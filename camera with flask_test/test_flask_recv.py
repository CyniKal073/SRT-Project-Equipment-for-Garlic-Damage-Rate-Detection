from flask import Flask
from flask import Response
from flask import render_template
import socket
import cv2
import numpy as np

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 确定通信协议类型
recv_addr = ('192.168.137.1', 8081)
while True:
    try:
        udp_socket.bind(recv_addr)
    except OSError:
        pass
    else:
        break
udp_socket.setblocking(0)  # 设置为非阻塞模式




'''
def UDP_Recv():
    while True:
        try:
            udp_socket.bind(recv_addr)
        except OSError:
            pass
        else:
            break
    udp_socket.setblocking(0)  # 设置为非阻塞模式
'''

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html')



def generate():
    image = cv2.imread('templates/IMG_20250504_182426.jpg')
    image = cv2.imencode('.jpg', image)[1].tobytes()
    while True:
        try:
            recv_byte, send_addr = udp_socket.recvfrom(921600)
            receive_data = np.frombuffer(recv_byte, dtype='uint8')
            r_img = cv2.imdecode(receive_data, 1)
            image = cv2.imencode('.jpg', r_img)[1].tobytes()
            nparr = np.fromstring(recv_byte, dtype='uint8', sep='')
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('CyniKal', img)
            cv2.waitKey(30)
        except BlockingIOError:
            pass
        except cv2.error:
            pass
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')



'''
capture = cv2.VideoCapture(0)  # 0为电脑内置摄像头

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 设置每帧图片的宽
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 设置每帧图片的高



def generate():
    while True:
        ret, frame = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
        frame = cv2.flip(frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
        img_encode = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 50])[1]  # 对每帧图进行编码,压缩画质
        data_encode = np.array(img_encode)
        byte_encode = data_encode.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_encode + b'\r\n\r\n')
'''


@app.route('/data_recv')
def data_recv():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')








'''
@app.route('/')
def index():
    return render_template('test.html')
def generate():
    while True:
        try:
            recv_byte, send_addr = udp_socket.recvfrom(921600)
            nparr = np.fromstring(recv_byte, dtype='uint8', sep='')  # 化为数组
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # 解码为彩色图
        except BlockingIOError as error:
            pass
        return img


@app.route('/img')
def data_recv():
    return Response(generate())
'''
if __name__ == '__main__':
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--ip', type=str, required=True, help='IP地址')
    ap.add_argument('-o', '--port', type=int, required=True, help='端口号')
    args = vars(ap.parse_args())
    '''

    '''
    t = threading.Thread(target=UDP_Recv())
    t.start()
    '''

    app.run(host='192.168.137.1', port='23333', debug=True, threaded=True, use_reloader=False)




