import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model

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

is_tiger, prob = classify_tiger('./img/tiger.jpg')

if (is_tiger == "tiger") & (prob > 0.6):
  print("tiger")