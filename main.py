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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from finalui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from live import Ui_Dialog
from datetime import datetime
import mysql.connector

from SqlManager import SQL

import AutoControl
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
        proxy_split = proxy.split(":")
        os.system(f"adb -s {self.handle} shell am broadcast -a com.vat.vpn.CONNECT_PROXY -n com.vat.vpn/.ui.ProxyReceiver --es address {proxy_split[0]} --es port {proxy_split[1]}  --es username {proxy_split[2]} --es password {proxy_split[3]}")
    def input_clip(self, data):
        os.system(f"adb -s {self.handle} shell am startservice ca.zgrs.clipper/.ClipboardService")
        os.system(f"adb -s {self.handle} shell am broadcast -a clipper.set -e text \"{data}\"")
        os.system(f"adb -s {self.handle} shell input keyevent 279")

    def proxyclear(self):
        os.system(f"adb -s {self.handle} shell settings put global http_proxy :0")

class MainWindow(QMainWindow):
    signal_device = pyqtSignal(int)
    signal_proxy = pyqtSignal(int)
    signal_data = pyqtSignal(str,str,str,str,str,int)
    signal_live = pyqtSignal(int)
    signal_die = pyqtSignal(int)
    signal_recheck = pyqtSignal(int)
    signal2 = pyqtSignal(str,int)
    signal_time = pyqtSignal(str)
    signal_sort = pyqtSignal(int,str,str,str,str)
    list_live = []
    start = True
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.livewindow = QtWidgets.QMainWindow()
        self.uic1 = Ui_Dialog()
        self.uic1.setupUi(self.livewindow)
        self.uic.tableWidget.setColumnWidth(0, 300)
        self.uic.tableWidget.setColumnWidth(1, 300)
        self.uic.tableWidget.setColumnWidth(2, 300)
        self.uic.tableWidget.setColumnWidth(3, 300)
        self.uic.tableWidget.setColumnWidth(4, 300)
        self.uic.pushButton_7.clicked.connect(self.GetDevice_Button)
        self.uic.pushButton_5.clicked.connect(self.GetProxy_Button)
        self.uic.pushButton_6.clicked.connect(self.GetLiveAccount)
        self.uic.stop.clicked.connect(self.Stop_All)
        self.uic.start.clicked.connect(self.start_timer)
        self.signal_device.connect(self.update_device)
        self.signal_proxy.connect(self.update_proxy)
        self.signal_data.connect(self.update_data)
        self.signal2.connect(self.update_status)
        self.list_device = []
        self.list_proxy = []
        self.start = True
        self.live = 0
        self.die = 0
        self.recheck = 0
        self.signal_live.connect(self.live_update)
        self.signal_die.connect(self.die_update)
        self.signal_recheck.connect(self.recheck_update)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time = QTime(0, 0, 0)


    def updatekk(self,status,i):
        self.signal2.emit(status,i)
    def updatekk2(self,device, user, pass_user, proxy, status, i):
        self.signal_data.emit(device, user, pass_user, proxy, status, i)

    #Device Get Button
    def GetDevice_Button(self):
        threading.Thread(target=self.GetDevice_Num).start()

    def GetDevice_Num(self):
        self.list_device = Getdevice()
        self.signal_device.emit(len(self.list_device))
        self.uic.tableWidget.setRowCount(len(self.list_device))

    def update_device(self,num):
        self.uic.label_43.setText(str(num))

    #ProxyGet
    def GetProxy_Button(self):
        threading.Thread(target=self.GetProxy_Num).start()
    def GetProxy_Num(self):
        file_path = 'proxy.txt'
        with open(file_path, 'r') as file:
            self.list_proxy = file.readlines()
        self.signal_proxy.emit(len(self.list_proxy))

    def update_proxy(self,num):
        self.uic.label_38.setText(str(num))

    #liveaccountGet
    def GetLiveAccount(self):
        self.livewindow.show()
        self.uic1.pushButton.clicked.connect(self.sort_data_thread)
        self.uic1.pushButton_2.clicked.connect(self.extract_live)
        self.uic1.pushButton_3.clicked.connect(self.sort_data_all_thread)

    def sort_data_thread(self):
        threading.Thread(target=self.sort_data).start()

    def sort_data_all_thread(self):
        threading.Thread(target=self.sort_data_all).start()
    def extract_live(self):
        if self.list_live != []:
            list_date = str(datetime.now())
            date = list_date.replace(" ","")
            date = date.replace(".","")
            date = date.replace(":", "-")
            name = f"{date}.txt"
            open(name,"x")
            with open(name, "a") as file:
                # Ghi nội dung vào file
                for data in self.list_live:
                    file.write(f"{data}\n")
    def sort_data_all(self):
        self.list_live.clear()
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = f"SELECT * FROM raw_accounts WHERE status = 4"
        cursor = connection.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        self.uic1.tableWidget.setRowCount(len(result_set))
        time.sleep(2)
        row_table = 0
        for row in result_set:
            self.list_live.append(f"{row[1]} | {row[2]} | {row[5]} | {row[8]}")
            self.uic1.tableWidget.setItem(row_table, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.uic1.tableWidget.setItem(row_table, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.uic1.tableWidget.setItem(row_table, 2, QtWidgets.QTableWidgetItem(str(row[5])))
            self.uic1.tableWidget.setItem(row_table, 3, QtWidgets.QTableWidgetItem(str(row[8])))
            row_table += 1

    def sort_data(self):
        self.list_live.clear()
        from_date = str(self.uic1.textEdit.toPlainText())
        to_date = str(self.uic1.textEdit_2.toPlainText())
        config = {
            'user': 'vlaapp',
            'password': 'aOzd1$635',
            'host': '11.0.0.199',
            'port': '3306',
            'database': 'vlaapp'
        }
        connection = mysql.connector.connect(**config)
        query = f"SELECT * FROM raw_accounts WHERE status = 4 AND updated_at = '{from_date}'"
        print("True")
        cursor = connection.cursor()
        cursor.execute(query)
        print("True")
        result_set = cursor.fetchall()
        self.uic1.tableWidget.setRowCount(len(result_set))
        row_table = 0
        for row in result_set:
            self.list_live.append(f"{row[1]} | {row[2]} | {row[5]} | {row[8]}")
            self.uic1.tableWidget.setItem(row_table, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.uic1.tableWidget.setItem(row_table, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.uic1.tableWidget.setItem(row_table, 2, QtWidgets.QTableWidgetItem(str(row[5])))
            self.uic1.tableWidget.setItem(row_table, 3, QtWidgets.QTableWidgetItem(str(row[8])))
            row_table += 1
    def StartAll(self):
        for i in range(len(self.list_device)):
            data_device = SQL(self.list_device[i])
            id = ""
            user = ""
            pass_user = ""
            result_set  = data_device.GetAccountData()
            for row in result_set:
                id = row[0]
                user = row[1]
                pass_user = row[2]
            proxy = "181.177.94.145:7719:jackprovn:Dienchau3vn"
            self.signal_data.emit(self.list_device[i],user,pass_user,proxy,"Created",i)
            #d = AutoControl.Checker_Yeah(self.list_device[i],user,pass_user,proxy,id,i)
            #threading.Thread(target=d.Walmart_Checker).start()
            t = threading.Thread(target=self.auto, args=(self.list_device[i],user,pass_user,proxy,id,i))
            t.start()


    def Stop_All(self):
        self.start  = False
    def auto(self, device, user, pass_user, proxy,id, i):

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
        obj = Auto(device)
        obj.change_proxy(proxy)
        while self.start:
            obj.DeleteCache("com.target.ui")
            time.sleep(5)
            point_logo = obj.find("target\\logo.png")
            if point_logo > [(0,0)]:
                obj.click(point_logo[0][0],point_logo[0][1])
                time.sleep(10)
                point_sigin = obj.find("target\\sigin.png")
                if point_sigin > [(0, 0)]:
                    obj.click(point_sigin[0][0], point_sigin[0][1])
                    time.sleep(10)
                    point_email = obj.find("target\\email.png")
                    if point_email > [(0,0)]:
                        obj.click(point_email[0][0],point_email[0][1])
                        obj.input_clip(user)
                        time.sleep(1)
                        point_pass = obj.find("target\\password.png")
                        if point_pass > [(0,0)]:
                            obj.click(point_pass[0][0],point_pass[0][1])
                            obj.input_clip(pass_user)
                            time.sleep(1)
                            obj.swipe(510, 1212, 508, 526)
                            point_sigin = obj.find("target\\sigin.png")
                            if point_sigin > [(0,0)]:
                                obj.click(point_sigin[0][0],point_sigin[0][1])

            time.sleep(10)

            point_live1 = obj.find("target\\live1.png")
            time.sleep(2)
            point_live2 = obj.find("target\\live2.png")
            time.sleep(2)
            if point_live1 > [(0,0)] or point_live2 > [(0,0)]:
                self.signal2.emit("Live",i)
            else:
                point_die1 = obj.find("target\\die1.png")
                time.sleep(2)
                point_die2 = obj.find("target\\die2.png")
                time.sleep(2)
                if point_die1 > [(0, 0)] or point_die2 > [(0, 0)]:
                    self.signal2.emit("Die", i)
                else:
                    self.signal2.emit("Recheck", i)

            time.sleep(2)
            self.signal2.emit(f"{device} is Done", i)
            time.sleep(2)
            cursor.execute(query)
            result_set = cursor.fetchall()
            user = ""
            pass_user = ""
            for row in result_set:
                id = row[0]
                user = row[1]
                pass_user = row[2]
            self.signal_data.emit(self.list_device[i],user,pass_user,proxy,"Created",i)
        self.signal2.emit("Device Stopped",i)



    def Start_Button(self):
        threading.Thread(target=self.StartAll).start()

    def update_data(self,device,email,password,proxy,status,index):
        self.uic.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(device))
        self.uic.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(email))
        self.uic.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(password))
        self.uic.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(proxy))
        self.uic.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(status))
    def update_status(self,status,index):
        self.uic.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(status))

    #update live,die,recheck
    def live_update(self,num):
        self.uic.label_5.setText(str(num))

    def die_update(self, num):
        self.uic.die_update.setText(str(num))

    def recheck_update(self, num):
        self.uic.label_13.setText(str(num))

    #update time running
    def start_timer(self):
        threading.Thread(target=self.StartAll).start()
        self.timer.start(1000)  # Gọi hàm update_timer mỗi 1000ms (1 giây)
        self.time = QTime(0, 0, 0)
        self.update_timer()

    def update_timer(self):
        self.time = self.time.addSecs(1)
        time_text = self.time.toString("hh:mm:ss")
        self.uic.time_update.setText(f'{time_text}')

#Sql Updated
def update_sql(id,status):
    config = {
    'user': 'vlaapp',
    'password': 'aOzd1$635',
    'host': '11.0.0.199',
    'port': '3306',
    'database': 'vlaapp'
    }

    connection = mysql.connector.connect(**config)
    list_date = str(datetime.now())
    date = list_date.split(" ")
    if status == "live":
        query = f"UPDATE raw_accounts SET status = 4, updated_at = {date[0]} WHERE id = {id}"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    elif status == "die":
        query = f"UPDATE raw_accounts SET status = 3, updated_at = {date[0]} WHERE id = {id}"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
#Getdevice
def Getdevice():
    devices = subprocess.check_output("adb devices")
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

