#
# キャプチャーした画像は100x100にリサイズし
# フォルダーに格納される
#
#---------------------------------------------------------
import cv2
import os

if not os.path.exists('img'):
    os.mkdir('img')
if not os.path.exists('img/p'):
    os.mkdir('img/p')
if not os.path.exists('img/g'):
    os.mkdir('img/g')
if not os.path.exists('img/c'):
    os.mkdir('img/c')
if not os.path.exists('img/b'):
    os.mkdir('img/b')

p_num = 0 #パー
g_num = 0 #グー
c_num = 0 #チョキ
b_num = 0 #ブランク

img_cap = cv2.VideoCapture(1)

d_rect = 0

while True:
    ret, img_base = img_cap.read()
    #img_gray = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
    
    # print(gray.shape[:3]) # (480, 640)
    xp = int(img_base.shape[1])
    yp = int(img_base.shape[0])
    cx = int(xp/2)
    cy = int(yp/2)

    if (d_rect == 1):
        # show the capture area
        cv2.rectangle(img_base, (cx-500, cy-500), (cx+500, cy+500), color=(0, 200, 200), thickness=5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_base,'capture area',(100,450), font, 1,(0,200,200),2,cv2.LINE_AA)

    resize = 100
    img_crop = cv2.resize(img_base[cy-500:cy+500, cx-500:cx+500], (resize, resize))

    # caputer images
    c = cv2.waitKey(10)
    if c == ord('p'):
        cv2.imwrite('img/p/{0}.png'.format(p_num), img_crop)
        p_num = p_num + 1
    elif c == ord('g'):
        cv2.imwrite('img/g/{0}.png'.format(g_num), img_crop)
        g_num = g_num + 1
    elif c == ord('c'):
        cv2.imwrite('img/c/{0}.png'.format(c_num), img_crop)
        c_num = c_num + 1
    elif c == ord('b'):
        cv2.imwrite('img/b/{0}.png'.format(b_num), img_crop)
        b_num = b_num + 1
    elif c == ord('d'):
        if (d_rect == 1):
            d_rect = 0
        else:
            d_rect = 1
    elif c == 27 or c == ord('q'):  # Esc
        break

    cv2.imshow('Images for CNN', img_base)
img_cap.release()
cv2.destroyAllWindows()

