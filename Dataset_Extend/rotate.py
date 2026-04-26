import os
import cv2
import shutil

def img_rotate(img, angle, filename, save_dir):
    if angle == 90:
        angle2cv = cv2.ROTATE_90_CLOCKWISE
    elif angle == 180:
        angle2cv = cv2.ROTATE_180
    elif angle == 270:
        angle2cv = cv2.ROTATE_90_COUNTERCLOCKWISE
    img_rotate = cv2.rotate(img, angle2cv)
    cv2.imwrite(save_dir + '/' + filename[:-4] + '_angel=%d.jpg' %(angle), img_rotate)

def label_rotate(label_dir, filename, save_dir, angel):
    label = open(label_dir + '/' + filename[:-4] + '.txt', mode='r')
    data = label.read()
    label.close()
    classids , xs, ys, ws, hs = [], [], [], [], []
    i = 0
    while len(data) != i+1:
        if i == 0:
            classids.append(data[i])
            i = i + 1
        elif data[i] == ' ':
            xs.append(data[i+1:i+9])
            i = i + 9
            ys.append(data[i+1:i+9])
            i = i + 9
            ws.append(data[i+1:i+9])
            i = i + 9
            hs.append(data[i+1:i+9])
            i = i + 9
        elif data[i] == '\n' and len(data) != i+1:
            classids.append(data[i+1])
            i = i + 2
    create = open(save_dir + '/' + filename[:-4] + '_angel=%d.txt' % (angel), mode='w')
    create.close()
    new_classids, new_xs, new_ys, new_ws, new_hs = [], [], [], [], []
    for i in range(len(classids)):
        new_classids.append(classids[i])
        if angel == 90:
            new_xs.append((str(1. - float(ys[i]))[:8]))
            new_ys.append(xs[i])
            new_ws.append(hs[i])
            new_hs.append(ws[i])
        elif angel == 180:
            new_xs.append((str(1. - float(xs[i]))[:8]))
            new_ys.append((str(1. - float(ys[i]))[:8]))
            new_ws.append(ws[i])
            new_hs.append(hs[i])
        elif angel == 270:
            new_xs.append(ys[i])
            new_ys.append((str(1. - float(xs[i]))[:8]))
            new_ws.append(hs[i])
            new_hs.append(ws[i])
        rotate_label = open(save_dir + '/' + filename[:-4] + '_angel=%d.txt' %(angel), mode='r+')
        rotate_label.seek(0, 2)
        rotate_label.write(new_classids[i] + ' ' + new_xs[i] + ' ' + new_ys[i] + ' ' + new_ws[i] + ' ' + new_hs[i] + '\n')
        rotate_label.close()

dir = 'test_enhance'
save_dir = 'test'
label_dir = 'test_label_enhance'
label_save_dir = 'test_label'

filelist = os.listdir(label_dir)
for file in filelist:
    #img = cv2.imread(dir + '/' + file)
    #img_rotate(img, 90, file, save_dir)
    label_rotate(label_dir, file, label_save_dir, 90)
    #shutil.copy(label_dir + '/' + file[:-4] + '.txt',
    #            label_save_dir + '/' + file[:-4] + '_angel=90.txt')
    #img_rotate(img, 180, file, save_dir)
    label_rotate(label_dir, file, label_save_dir, 180)
    #shutil.copy(label_dir + '/' + file[:-4] + '.txt',
    #            label_save_dir + '/' + file[:-4] + '_angel=180.txt')
    #img_rotate(img, 270, file, save_dir)
    label_rotate(label_dir, file, label_save_dir, 270)
    #shutil.copy(label_dir + '/' + file[:-4] + '.txt',
    #            label_save_dir + '/' + file[:-4] + '_angel=270.txt')
