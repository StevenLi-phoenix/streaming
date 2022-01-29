import atexit
import pickle
import socket
import threading
import time

import cv2
import numpy as np


class Server:
    def __init__(self):
        PORT = 18082
        IPADDRESS = '192.168.0.105'
        SERVER_ADDRESS = (IPADDRESS, PORT)  # print(socket.gethostbyname(socket.gethostname()))

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER_ADDRESS)
        self.recieve_length = 1024
        atexit.register(self.close)
        self.img_s = None
        self.rate = [0 for i in range(100)]

    def main(self):
        self.server.listen()
        while True:
            self.conn, addr = self.server.accept()
            print(f"[ ACK ]{addr} connect\tcurrent {threading.active_count()}")
            t = threading.Thread(target=self.handle_client)
            t.start()

    def handle_client(self):
        while True:
            msg = self.conn.recvfrom(100000000)
            if len(msg) is not None:
                print(f"\r Last recieved: {sum(self.rate)} out of {len(self.rate)}", end="\t")
                # img_s = cv2.imdecode(np.asarray(bytearray(msg), dtype='uint8'), cv2.IMREAD_COLOR)
                try:
                    img_s = pickle.loads(msg[0])
                    if img_s is None:
                        pass
                    else:
                        self.img_s = cv2.resize(img_s, (640, 480))
                        self.rate.pop(0)
                        self.rate.append(1)
                except pickle.UnpicklingError:
                    # print("数据包过大")
                    self.rate.pop(0)
                    self.rate.append(0)
                except ValueError:
                    print("unregistered extension code 121")
                    self.rate.pop(0)
                    self.rate.append(0)
                except EOFError:
                    print("Ran out of input")
                    self.rate.pop(0)
                    self.rate.append(0)
                    break
                except Exception as e:
                    print(e, "Bypass")
                    self.rate.pop(0)
                    self.rate.append(0)
                # print(type(data))
                # img_s = cv2.imdecode(msg, cv2.IMREAD_COLOR)
        self.close()

    def close(self):
        self.conn.close()
        self.server.close()
        cv2.destroyAllWindows()
        print("Closed")


if __name__ == '__main__':
    s = Server()
    threading.Thread(target=s.main).start()
    while sum(s.rate) < 1:
        time.sleep(0.1)
    print("Create window")
    while sum(s.rate) > 0:
        pic = s.img_s
        if np.max(pic) < 50:
            pic_max = np.max(pic)
            pic_min = np.min(pic)
            pic = pic - pic_min
            pic = pic * (1 / (pic_max - pic_min))
            # pic = np.array(pic).astype("float32")
            # pid = cv2.bilateralFilter(pic, 0, 100, 5)
        cv2.imshow("remote_pic", pic)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    s.close()
    exit(0)
