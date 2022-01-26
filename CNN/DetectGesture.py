#
# キャプチャー画像を推定する
# キャプチャー画像を100x100にリサイズする
#
#---------------------------------------------------------
#import keras
import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.models import load_model

import numpy as np
import os
import serial
import time

from PIL import Image
import cv2


# 学習済みモデルのロード
model = load_model("./original_img.h5")
model.summary()
#['c', 'p', 'g', 'b']-> [0, 1, 2, 3]

# 動作確認用
img_arr = []
image = Image.open('./img/g/0.png')
image = image.convert("RGB")
image = image.resize((100, 100))
data = np.asarray(image)
img_arr.append(data)
img_arr = np.array(img_arr)
img_arr = img_arr.astype('float32')/255
img_arr.shape[:]
y_pred = model.predict(img_arr) 
print(y_pred)   
#['c', 'p', 'g', 'b']-> [0, 1, 2, 3]

# ビデオ初期化
#img_cap = cv2.VideoCapture(0)
img_cap = cv2.VideoCapture(1)

#with serial.Serial('/dev/cu.usbmodem14301', timeout=0.1) as ser:
while True:
    
    # ビデオ画像の処理
    img_arr = []
    ret, img_base = img_cap.read()
    xp = int(img_base.shape[1]) #1920
    yp = int(img_base.shape[0]) #1080
    cx = int(xp/2)
    cy = int(yp/2)
    #print(xp, " + ", yp)

    resize = 100
    img_crop = cv2.resize(img_base[cy-500:cy+500, cx-500:cx+500], (resize, resize))
    cv2.imshow('Images for CNN', img_crop)

    imgCV_RGB = img_crop[:, :, ::-1]
    img_pil = Image.fromarray(imgCV_RGB)

    data = np.asarray(img_pil)
    img_arr.append(data)
    img_arr = np.array(img_arr)
    img_arr = img_arr.astype('float32')/255
    img_arr.shape[:]
    
    # 予測
    #['c', 'p', 'g', 'b']-> [0, 1, 2, 3]
    y_pred = model.predict(img_arr) 
    #print(y_pred)
    # 結果の表示
    if y_pred[0].argmax() == 0:
        if (y_pred[0][0] > 0.7):
            print("")
    elif y_pred[0].argmax() == 1:
        if (y_pred[0][1] > 0.7):
            print("グー!!")
    elif y_pred[0].argmax() == 2:
        if (y_pred[0][2] > 0.7):
            print("チョキ!!")
    elif y_pred[0].argmax() == 3:
        if (y_pred[0][3] > 0.7):
            print("パー!!")


    if cv2.waitKey(10) == 27:
        break

# ビデオ開放
cv2.destroyAllWindows()
