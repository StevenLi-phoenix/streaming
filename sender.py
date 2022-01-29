import pickle
import socket
import sys
import time

import atexit
import cv2


class sender:
    def __init__(self):
        PORT = 18082
        IPADDRESS = '192.168.0.105'
        SERVER_ADDRESS = (IPADDRESS, PORT)  # print(socket.gethostbyname(socket.gethostname()))

        self.cilent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cilent.connect(SERVER_ADDRESS)
        atexit.register(self.close)

    def main(self, x=196, y=147):
        self.cap = cv2.VideoCapture(0)
        atexit.register(self.close)
        print(x, y)
        while True:
            ret, img = self.cap.read()
            if ret:
                # img = cv2.imencode(".png", img)[1]
                # ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
                # image_bytes = np.array(cv2.imencode('.jpg', img)[1]).tobytes()
                # self.cilent.send(f"LEN{len(image_bytes)}".encode("utf-8"))
                img = cv2.resize(img, (x, y))
                img_bytes = pickle.dumps(img)
                self.cilent.send(img_bytes)
                time.sleep(1 / 15)

    def close(self):
        self.cilent.close()
        self.cap.release()
        print("Closed")


if __name__ == '__main__':
    s = sender()
    s.main(int(sys.argv[1]), int(sys.argv[2]))
