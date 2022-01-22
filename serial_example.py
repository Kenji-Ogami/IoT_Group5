# 実行方法
# $ python serial_exemple.py COM5 9600

import sys
import serial
import time

class COM:
    def __init__(self, port, baud):
        self.com = serial.Serial(port, baud)

    def write(self, wdata):
        self.com.write(wdata.encode('utf-8'))

    def read(self):
        return self.com.read_all().decode('utf-8')

if __name__=="__main__":
    c = COM(sys.argv[1], sys.argv[2])
    while (True):
        c.write('a')
        print(c.read())
        time.sleep(1)


