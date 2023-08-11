#region Import Module
import os
try:
    import threading, subprocess, base64, cv2, random
    import numpy as np
except:
    os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
    os.system("pip install numpy")
import threading, subprocess, random
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from live_ui import Ui_Dialog
from datetime import datetime
from SqlManager import SQL
from AutoControl import Checker_Options
from Auto_Lib import Auto
from PyQt5.QtWidgets import *
#endregion

class MainWindow(QMainWindow):
    #region properties
    signal_device = pyqtSignal(int)
    signal_proxy = pyqtSignal(int)
    signal_time = pyqtSignal(str)
    signal_sort = pyqtSignal(int, str, str, str, str)
    signal_sort_data = pyqtSignal(int, str, str, str, str)
    list_live = []
    #endregion
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.livewindow = QtWidgets.QMainWindow()
        self.uic1 = Ui_Dialog()
        self.uic1.setupUi(self.livewindow)
        self.uic.pushButton_7.clicked.connect(self.GetDevice_Button)
        self.uic.pushButton_5.clicked.connect(self.GetProxy_Button)
        self.uic.pushButton_6.clicked.connect(self.GetLiveAccount)
        self.uic.stop.clicked.connect(self.Stop_All)
        self.uic.start.clicked.connect(self.start_timer)
        self.signal_device.connect(self.update_device)
        self.signal_proxy.connect(self.update_proxy)
        self.list_device = []
        self.list_proxy = []
        self.live = 0
        self.die = 0
        self.recheck = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time = QTime(0, 0, 0)
        self.list_obj = []
        self.signal_sort_data.connect(self.update_data_sort)

    # region Device Control
    ...

    # Device Get Button
    def GetDevice_Button(self):
        threading.Thread(target=self.GetDevice_Num).start()

    def GetDevice_Num(self):
        Device = Auto("GET")
        self.list_device = Device.Getdevice()
        self.signal_device.emit(len(self.list_device))
        self.uic.tableWidget.setRowCount(len(self.list_device))

    def update_device(self, num):
        self.uic.label_43.setText(str(num))
    # endregion

    #region Proxy Control
    # ProxyGet
    def GetProxy_Button(self):
        threading.Thread(target=self.GetProxy_Num).start()

    def GetProxy_Num(self):
        file_path = 'proxy.txt'
        with open(file_path, 'r') as file:
            self.list_proxy = file.readlines()
        self.signal_proxy.emit(len(self.list_proxy))

    def update_proxy(self, num):
        self.uic.label_38.setText(str(num))

    # endregion

    #region Live Account Checker Control
    # liveaccountGet
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
            date = list_date.replace(" ", "")
            date = date.replace(".", "")
            date = date.replace(":", "-")
            name = f"{date}.txt"
            open(name, "x")
            with open(name, "a") as file:
                # Ghi nội dung vào file
                for data in self.list_live:
                    file.write(f"{data}\n")

    def sort_data_all(self):
        self.uic1.tableWidget.clearContents()
        self.list_live.clear()
        data_get = SQL("GET")
        result_set = data_get.GetAllAccountLive()
        self.uic1.tableWidget.setRowCount(len(result_set))
        row_table = 0
        for row in result_set:
            self.list_live.append(f"{row[1]} | {row[2]} | {row[5]} | {row[8]}")
            self.signal_sort_data.emit(row_table,str(row[1]),str(row[2]),str(row[5]),str(row[8]))
            time.sleep(0.001)
            row_table += 1

    def sort_data(self):
        self.uic1.tableWidget.clearContents()
        self.list_live.clear()
        from_date = str(self.uic1.textEdit.toPlainText())
        to_date = str(self.uic1.textEdit_2.toPlainText())
        data_get = SQL("GET")
        result_set = data_get.GetAccountWithDate(from_date, to_date)
        self.uic1.tableWidget.setRowCount(len(result_set))
        row_table = 0
        for row in result_set:
            self.list_live.append(f"{row[1]} | {row[2]} | {row[5]} | {row[8]}")
            self.signal_sort_data.emit(row_table, str(row[1]), str(row[2]), str(row[5]), str(row[8]))
            row_table += 1
            time.sleep(0.001)

    def update_data_sort(self,index,user,pass_user,status,update):
        self.uic1.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(user))
        self.uic1.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(pass_user))
        self.uic1.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(str(status)))
        self.uic1.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(str(update)))

    #endregion

    #region Auto Control
    def StartAll(self):
        try:
            for i in range(len(self.list_device)):
                d = Checker_Options(self.list_device[i],self.list_proxy[random.randint(0,1)].replace("\n",""), i)
                self.list_obj.append(d)
                d.status_signal.connect(self.update_status)
                d.data_signal.connect(self.update_data)
                d.live_signal.connect(self.live_update)
                d.die_signal.connect(self.die_update)
                d.recheck_signal.connect(self.recheck_update)
                if self.uic.comboBox.currentText() == " Walmart":
                    threading.Thread(target = d.Walmart_Checker).start()
                elif self.uic.comboBox.currentText() == " Target App":
                    threading.Thread(target = d.Target_Checker).start()
        except:
            print("Error In StartAll Funtion In MainWindow")

    def Stop_All(self):
        for obj in self.list_obj:
            obj.check_stop()

    #endregion

    #region Table Data Update Control
    def update_data(self, device, email, password, proxy, status, index):
        self.uic.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(device))
        self.uic.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(email))
        self.uic.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(password))
        self.uic.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(proxy))
        self.uic.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(status))

    def update_status(self, status, index):

        self.uic.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem(status))
    #endregion

    #region Update Capture Control
    # update live,die,recheck
    def live_update(self, num):
        self.live += num
        self.uic.label_5.setText(str(self.live))

    def die_update(self, num):
        self.die += num
        self.uic.die_update.setText(str(self.die))

    def recheck_update(self, num):
        self.recheck += num
        self.uic.label_13.setText(str(self.recheck))

    #endregion

    #region Timecount Control
    def start_timer(self):
        threading.Thread(target=self.StartAll).start()
        self.timer.start(1000)  # Gọi hàm update_timer mỗi 1000ms (1 giây)
        self.time = QTime(0, 0, 0)
        self.update_timer()

    def update_timer(self):
        self.time = self.time.addSecs(1)
        time_text = self.time.toString("hh:mm:ss")
        self.uic.time_update.setText(f'{time_text}')
    #endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
