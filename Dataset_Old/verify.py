from ultralytics import YOLO
import cv2


if __name__ == '__main__':


    # 加载训练好的模型
    model = YOLO('D:\\test16\\weights\\best.pt')
    #model.export(format='onnx', opset=11)
    '''
    # 对验证集进行评估
    metrics = model.val(data='DataSet/test.yaml', batch=1, device=0)
    '''
    sources = 'D:\\PyCharm\\untitled1\\DataSet\\images\\IMG_20250504_180344.jpg'

    #esults = model(source=0, verbose=False, show=True, stream=True)
    from ultralytics import YOLO


    pth_path = r"G:\yolov8\ultralytics-main\ultralytics-main\runs\detect\train17\weights\best.pt"

    test_path = r"G:\yolov8\ultralytics-main\ultralytics-main\detect_test"
    # Load a model
    # model = YOLO('yolov8n.pt')  # load an official model


    # Predict with the model
    results = model('DataSet/images', save=True, conf=0.5)  # predict on an image

'''
    for r in results:
        box = r.boxes.cpu().numpy()
        xyxys = box.xyxy
        #frame = r.orig_img
        #for xyxy in xyxys:
            #cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 1)
        confidences = []
        confidences.append(box.conf)
        class_ids = []
        class_ids.append(box.cls)
        print('xyxys:%s\nclassids:%s\nconfidences:%s' %(xyxys, class_ids, confidences))
        #cv2.imshow('detection', frame)
'''
'''
    results.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 设置每帧图片的宽
    results.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 设置每帧图片的高
    ret, frame = results.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
    frame = cv2.flip(results, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
    img_encode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])[1]  # 对每帧图进行编码,压缩画质
    '''
