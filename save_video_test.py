import cv2
import numpy as np

# 0=内蔵カメラ
cap = cv2.VideoCapture(0)

fps = int(cap.get(cv2.CAP_PROP_FPS))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (w, h))

while cap.isOpened():
  ret, frame = cap.read()
  if not ret:
      print("Can't receive frame (stream end?). Exiting ...")
      break

  cv2.imshow('frame', frame)
  out.write(frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
out.release()
cv2.destroyAllWindows()