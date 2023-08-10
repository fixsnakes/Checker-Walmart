import os


try:
    import threading, subprocess, base64, cv2, random
    import numpy as np
except:
    os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
    os.system("pip install numpy")
import threading, subprocess, base64, cv2, random
import numpy as np

import sys
import time



from PyQt5.QtCore import QThread, pyqtSignal
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from last import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector




class Auto:
    def __init__(self, handle):
        self.handle = handle

    def screen_capture(self):
        # os.system(f'adb -s {self.handle} exec-out screencap -p > {name}.png')
        pipe = subprocess.Popen(f'adb -s {self.handle} exec-out screencap -p',
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, shell=True)
        # image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image

    def click(self, x, y):
        os.system(f'adb -s {self.handle} shell input tap {x} {y}')

    def swipe(self, x1, y1, x2, y2):
        os.system(f"adb -s {self.handle} shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000")

    def Back(self):
        os.system(f"adb -s {self.handle} shell input keyevent 3")

    def DeleteCache(self, package):
        subprocess.check_output(f"adb -s {self.handle} shell pm clear {package}")

    def off(self, package):
        os.system(f"adb -s {self.handle} shell am force-stop {package}")

    def InpuText(self, text=None, VN=None):
        if text == None:
            text = str(base64.b64encode(VN.encode('utf-8')))[1:]
            os.system(f"adb -s {self.handle} shell ime set com.android.adbkeyboard/.AdbIME")
            os.system(f"adb -s {self.handle} shell am broadcast -a ADB_INPUT_B64 --es msg {text}")
            return
        os.system(f"adb -s {self.handle} shell input text '{text}'")

    def find(self, img='', threshold=0.99):
        img = cv2.imread(img)  # sys.path[0]+"/"+img)
        img2 = self.screen_capture()
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        return retVal

    def tapimg(self, img='', tap='', threshold=0.99):
        img = cv2.imread(img)  # sys.path[0]+"/"+img)
        tap = cv2.imread(tap)
        img2 = self.screen_capture()
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        result2 = cv2.matchTemplate(img, tap, cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(result2 >= threshold)
        retVal2 = list(zip(*loc2[::-1]))
        if retVal > [(0, 0)]:
            self.click(retVal2[0][0], retVal2[0][1])
        else:
            return 0

    def change_proxy(self, proxy):
        os.system(f"adb -s {self.handle} shell settings put global http_proxy {proxy}")

    def input_clip(self, data):
        os.system(f"adb -s {self.handle} shell am startservice ca.zgrs.clipper/.ClipboardService")
        os.system(f"adb -s {self.handle} shell am broadcast -a clipper.set -e text \"{data}\"")
        os.system(f"adb -s {self.handle} shell input keyevent 279")



class MainWindow(QMainWindow):
    signal = pyqtSignal(str, str, str, int,str,str)
    signal2 = pyqtSignal(str,int)

    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.tableWidget.setColumnWidth(0, 300)
        self.uic.tableWidget.setColumnWidth(1, 300)
        self.uic.tableWidget.setColumnWidth(2, 300)
        self.uic.tableWidget.setColumnWidth(3, 300)
        self.uic.tableWidget.setColumnWidth(4, 300)
        self.uic.tableWidget.setRowCount(50)
        self.uic.Run.clicked.connect(self.call)
        self.uic.tableWidget.setGeometry(QtCore.QRect(0, 70, 1600, 800))
        self.uic.Run.setGeometry(QtCore.QRect(0, 0, 90, 50))
        self.uic.Stop.setGeometry(QtCore.QRect(90, 0, 90, 50))
        self.signal.connect(self.update_data)
        self.signal2.connect(self.update_status)

    def run(self):
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = "SELECT * FROM raw_accounts WHERE status = 0 AND script_id = 1 OR status = 2 AND script_id = 1 ORDER BY RAND() LIMIT 1"
        cursor = connection.cursor()
        list_proxy = ["23.94.144.106:15690", "23.94.144.106:27229"]
        list_device = Getdevice()
        for i in range(list_device):
            cursor.execute(query)
            result_set = cursor.fetchall()
            user = ""
            pass_user = ""
            for row in result_set:
                user = row[1]
                pass_user = row[2]
            self.signal.emit(list_device[i],user, pass_user, i,list_proxy[random.randint(0,1)],"created")
            threading.Thread(target=self.auto, args=(user, pass_user, i)).start()

    def auto(self, device, user, pass_user, i):
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = "SELECT * FROM raw_accounts WHERE status = 0 AND script_id = 1 OR status = 2 AND script_id = 1 ORDER BY RAND() LIMIT 1"
        cursor = connection.cursor()
        list_proxy = ["23.94.144.106:15690", "23.94.144.106:27229"]
        while True:
            time.sleep(random.randint(1, 3))
            self.signal2.emit("Openning Walrmart...", i)
            time.sleep(random.randint(1, 3))
            self.signal2.emit("Done", i)
            time.sleep(random.randint(1, 3))
            cursor.execute(query)
            result_set = cursor.fetchall()
            user = ""
            pass_user = ""
            for row in result_set:
                user = row[1]
                pass_user = row[2]
            self.signal.emit(user, pass_user, i,list_proxy[random.randint(0,1)],"created")

    def call(self):
        t = threading.Thread(target=self.run)
        t.start()

    def update_call(self, user, pass_user,index):
        self.signal.emit(user, pass_user, index)
        self.signal2.emit(user,index)

    def update_data(self, device, name, user, index,proxy,status):
        self.uic.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(name))
        self.uic.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(name))
        self.uic.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(user))
        self.uic.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(proxy))
        self.uic.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(status))

    def update_status(self, status, index):
        self.uic.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(status))

def Getdevice():
    devices = subprocess.check_output("adb devices")
    devices = devices.decode("utf-8")
    # check output khi goi adb devices
    p = str(devices).replace("b'List of devices attached", "").replace('\\r\\n', "").replace(" ", "").replace("'",
                                                                                                              "").replace(
        'b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached', "")
    delimiters = ["\\tunauthorized", "\\tdevice"]
    if len(p) > 0:
        for delimiter in delimiters:
            p = " ".join(p.split(delimiter))
        listdevice = p.split(" ")
        listdevice.pop()
        listdevice.remove("988768383253454241")
        return listdevice
    else:
        return "none"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
