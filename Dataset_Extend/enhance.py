import os
import cv2
import numpy as np
import shutil

dir = 'dataset-img'
save_dir = 'test_enhance'
label_dir = 'dataset-label'
save_label_dir = 'test_label_enhance'

filelist = os.listdir(dir)
for file in filelist:
    img = cv2.imread(dir + '/' + file)
    gauss = np.random.normal(0,25,img.shape)
    gauss_img = img + gauss
    gauss_img = np.clip(gauss_img, a_min=0, a_max=255).astype(np.uint8)
    gauss_enhance_img_1 = cv2.convertScaleAbs(gauss_img, 100, 1.5)
    gauss_enhance_img_2 = cv2.convertScaleAbs(gauss_img, 100, 0.9)
    cv2.imwrite(save_dir + '/' + file[:-4] + '_enhance_1.jpg', gauss_enhance_img_1)
    cv2.imwrite(save_dir + '/' + file[:-4] + '_enhance_2.jpg', gauss_enhance_img_2)
    shutil.copy(label_dir + '/' + file[:-4] + '.txt',
                save_label_dir + '/' + file[:-4] + '_enhance_1.txt')
    shutil.copy(label_dir + '/' + file[:-4] + '.txt',
                save_label_dir + '/' + file[:-4] + '_enhance_2.txt')