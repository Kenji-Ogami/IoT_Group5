# $ python3 serial_exemple.py COM5 9600

from PIL import Image
import numpy as np
from keras.models import load_model
import cv2
import time
import serial
import sys

class COM:
  def __init__(self, port, baud):
    self.com = serial.Serial(port, baud)

  def write(self, wdata):
    self.com.write(wdata.encode('utf-8'))

  def read(self):
    return self.com.read_all().decode('utf-8')

if __name__=="__main__":
    # setup serial
    # c = COM(sys.argv[1], sys.argv[2])

    # load model
    model_loc = './model/model_tigercat.h5'
    model = load_model(model_loc)

    # camera
    img_cap = cv2.VideoCapture(0)

    while img_cap.isOpened():
      img_arr = []
      ret, img_base = img_cap.read()
      xp = int(img_base.shape[1])  # 1920
      yp = int(img_base.shape[0])  # 1080
      cx = int(xp / 2)
      cy = int(yp / 2)

      resize = 100
      img_crop = cv2.resize(img_base[cy - 500:cy + 500, cx - 500:cx + 500], (resize, resize))
      cv2.imshow('Images', img_base)

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

      if is_tiger:
        print('Classified into:\t{}'.format(classes[is_tiger]))
        print('Probability:\t\t{:.3f}'.format(classified_prob.max()))
        # c.write('a')
        # print(c.read())

      time.sleep(0.5)

      if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()

# 静止画の場合
# def classify_tiger(img):
#   classes = ['cat', 'tiger']
#   pic = Image.open(img)
#   pic = pic.convert('RGB')
#   pic = pic.resize((100, 100))
#   pic = np.asarray(pic)
#   classified_prob = model.predict(np.array([pic]))
#   # 虎の場合1、猫の場合0
#   is_tiger = np.argmax(classified_prob)
#   # モデルによる分類結果と分類される確率を表示
#   print('Classified into:\t{}'.format(classes[is_tiger]))
#   print('Probability:\t\t{:.3f}'.format(classified_prob.max()))
#   return (classes[is_tiger], classified_prob.max())
#
# is_tiger, prob = classify_tiger('./img/tiger.jpg')
#
# if (is_tiger == "tiger") & (prob > 0.6):
#   print("tiger")
