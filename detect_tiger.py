import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
import cv2
import time

model_loc = './model/model_tigercat.h5'
model = load_model(model_loc)

def classify_tiger(img):
  classes = ['cat', 'tiger']
  pic = Image.open(img)
  pic = pic.convert('RGB')
  pic = pic.resize((100, 100))
  pic = np.asarray(pic)
  classified_prob = model.predict(np.array([pic]))
  # 虎の場合1、猫の場合0
  is_tiger = np.argmax(classified_prob)
  # モデルによる分類結果と分類される確率を表示
  print('Classified into:\t{}'.format(classes[is_tiger]))
  print('Probability:\t\t{:.3f}'.format(classified_prob.max()))
  return (classes[is_tiger], classified_prob.max())

# 動作確認用
is_tiger, prob = classify_tiger('./img/tiger.jpg')

if (is_tiger == "tiger") & (prob > 0.6):
  print("tiger")

img_cap = cv2.VideoCapture(1)

while img_cap.isOpened():

  # ビデオ画像の処理
  img_arr = []
  ret, img_base = img_cap.read()
  xp = int(img_base.shape[1])  # 1920
  yp = int(img_base.shape[0])  # 1080
  cx = int(xp / 2)
  cy = int(yp / 2)
  # print(xp, " + ", yp)

  resize = 100
  img_crop = cv2.resize(img_base[cy - 500:cy + 500, cx - 500:cx + 500], (resize, resize))
  cv2.imshow('Images for CNN', img_base)

  imgCV_RGB = img_crop[:, :, ::-1]
  img_pil = Image.fromarray(imgCV_RGB)

  data = np.asarray(img_pil)
  img_arr.append(data)
  img_arr = np.array(img_arr)
  img_arr = img_arr.astype('float32') / 255
  img_arr.shape[:]

  classified_prob = model.predict(img_arr)
  classes = ['nothing', 'tiger']
  is_tiger = np.argmax(classified_prob)
  # print('Classified into:\t{}'.format(classes[is_tiger]))
  # print('Probability:\t\t{:.3f}'.format(classified_prob.max()))

  if is_tiger:
    print("tiger")

  time.sleep(0.5)


  if cv2.waitKey(10) == 27:
    break

cv2.destroyAllWindows()