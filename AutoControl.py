import time,random
from Auto_Lib import Auto
from SqlManager import SQL
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import *

class Checker_Options(QObject):
    status_signal = pyqtSignal(str, int)
    data_signal = pyqtSignal(str, str, str, str, str, int)
    live_signal = pyqtSignal(int)
    die_signal = pyqtSignal(int)
    recheck_signal = pyqtSignal(int)
    start = True
    def __init__(self, device,proxy,i):
        super().__init__()
        self.device = device
        self.proxy = proxy
        self.i = i

    def Target_Checker(self):
        flag = 0
        obj = Auto(self.device)
        obj.proxyclear()
        time.sleep(2)
        obj.change_proxy(self.proxy)
        time.sleep(2)
        data_account = SQL(self.device)
        while self.start:
            try:
                flag = 0
                result = data_account.GetAccountData()
                if result != "error":
                    for row in result:
                        id = row[0]
                        user = row[1]
                        pass_user = row[2]
                    self.data_signal.emit(self.device,user,pass_user,self.proxy,"Created",self.i)
                    time.sleep(random.randint(2,3))
                    obj.DeleteCache("com.target.ui")
                    self.status_signal.emit("Cache Cleared",self.i)
                    time.sleep(random.randint(2,3))
                    self.status_signal.emit("Checking By Email And Password......",self.i)
                    point_logo = obj.find("target\\logo.png")
                    if point_logo > [(0, 0)]:
                        self.status_signal.emit("Target Openned", self.i)
                        obj.click(point_logo[0][0], point_logo[0][1])
                        time.sleep(5)
                        self.status_signal.emit("Log In By Email And Password", self.i)
                        point_sigin = obj.find("target\\sigin.png")
                        if point_sigin > [(0, 0)]:
                            obj.click(point_sigin[0][0], point_sigin[0][1])
                            time.sleep(5)
                            point_email = obj.find("target\\email.png")
                            if point_email > [(0, 0)]:
                                obj.click(point_email[0][0], point_email[0][1])
                                obj.input_clip(user)
                                time.sleep(1)
                                point_pass = obj.find("target\\password.png")
                                if point_pass > [(0, 0)]:
                                    obj.click(point_pass[0][0], point_pass[0][1])
                                    obj.input_clip(pass_user)
                                    time.sleep(1)
                                    obj.swipe(510, 1212, 508, 526)
                                    point_sigin = obj.find("target\\sigin.png")
                                    if point_sigin > [(0, 0)]:
                                        obj.click(point_sigin[0][0], point_sigin[0][1])
                                    else:
                                        flag = 1
                                else:
                                    flag = 1
                            else:
                                flag = 1
                        else:
                            flag = 1
                    else:
                        flag = 1
                    if(flag == 1):
                        self.recheck_signal.emit(1)
                        self.status_signal.emit("Recheck",self.i)
                        time.sleep(2)
                    else:
                        point_die1 = obj.find("target\\die1.png")
                        point_die2 = obj.find("target\\die2.png")
                        if point_die1 > [(0,0)] or point_die2 >[(0,0)]:
                            self.die_signal.emit(1)
                            self.status_signal.emit("Die",self.i)
                        else:
                            point_live1 = obj.find("target\\live1.png")
                            point_live2 = obj.find("target\\live1.png")
                            if point_live1 >[(0,0)] or point_live2 > [(0,0)]:
                                self.live_signal.emit(1)
                                self.status_signal.emit("Live",self.i)
                                data_account.UpdateSqlStatus("live",id)
                            else:
                                self.recheck_signal.emit(1)
                                self.status_signal.emit("Recheck", self.i)
                    time.sleep(2)
                else:
                    self.status_signal.emit("SQL Error!", self.i)
                    self.start = False
                    time.sleep(10)
            except:
                self.status_signal.emit("Something Error Rechecking...!", self.i)
                time.sleep(2)
        self.status_signal.emit("Stopped",self.i)


    def Walmart_Checker(self):
        obj = Auto(self.device)
        obj.change_proxy(self.proxy)
        data_account = SQL(self.device)
        while self.start:
            try:
                exist = 0
                flag = 0
                result = data_account.GetAccountData()
                if result != "error":
                    for row in result:
                        id = row[0]
                        user = row[1]
                        pass_user = row[2]
                    self.data_signal.emit(self.device, user, pass_user, self.proxy, "Created", self.i)
                    time.sleep(random.randint(2, 3))
                    obj.DeleteCache("com.walmart.android")
                    self.status_signal.emit("Cache Cleared",self.i)
                    time.sleep(2)
                    self.status_signal.emit("Walmart Opened", self.i)
                    point_walmart = obj.find("img\\walmart_icon.png")
                    if point_walmart > [(0, 0)]:
                        obj.click(point_walmart[0][0], point_walmart[0][1])
                        time.sleep(5)
                        self.status_signal.emit("Checking By Email And Password", self.i)
                        point_sign = obj.find("img\\signin.png")
                        if point_sign > [(0, 0)]:
                            obj.click(point_sign[0][0], point_sign[0][1])
                            time.sleep(3)
                            point_flag1 = obj.find("img\\Flag_Valid.png")
                            if point_flag1 > [(0, 0)]:
                                obj.swipe(515, 1166, 540, 701)
                                time.sleep(2)
                                point_email = obj.find("img\\email_box.png")
                                if point_email > [(0, 0)]:
                                    obj.click(point_email[0][0], point_email[0][1])
                                    time.sleep(2)
                                    obj.input_clip(user)
                                    time.sleep(2)
                                    point_continue = obj.find("img\\continue.png")
                                    if point_continue > [(0, 0)]:
                                        obj.click(point_continue[0][0], point_continue[0][1])
                                        time.sleep(8)
                                        point_exist = obj.find("img\\Tontai.png")
                                        if point_exist > [(0, 0)]:
                                            exist = 1
                                            obj.swipe(510, 1212, 508, 526)
                                            obj.swipe(510, 1212, 508, 526)
                                            time.sleep(2)
                                            point_password = obj.find("img\\password_box.png")
                                            if point_password > [(0, 0)]:
                                                obj.click(point_password[0][0], point_password[0][1])
                                                time.sleep(1)
                                                obj.input_clip(pass_user)
                                                obj.swipe(510, 1212, 508, 526)
                                                obj.swipe(510, 1212, 508, 526)
                                                time.sleep(3)
                                                point_sign_2 = obj.find("img\\sigin2.png")
                                                if point_sign_2 > [(0, 0)]:
                                                    obj.click(point_sign_2[0][0], point_sign_2[0][1])
                                                else:
                                                    flag = 1
                                            else:
                                                flag = 1
                                    else:
                                        flag = 1
                                else:
                                    flag = 1
                            else:
                                self.status_signal.emit("Checking By Email And Password", self.i)
                                obj.swipe(515, 1166, 540, 701)
                                point_email = obj.find("img\\email_box.png")
                                if point_email > [(0, 0)]:
                                    obj.click(point_email[0][0], point_email[0][1])
                                    obj.input_clip(user)
                                    time.sleep(1)
                                    point_password = obj.find("img\\password_box.png")
                                    if point_password > [(0, 0)]:
                                        obj.click(point_password[0][0], point_password[0][1])
                                        obj.input_clip(pass_user)
                                        time.sleep(1)
                                        point_sign = obj.find("img\\sigin2.png")
                                        if point_sign > [(0, 0)]:
                                            obj.click(point_sign[0][0], point_sign[0][1])
                                            time.sleep(8)
                                            point_exist = obj.find("img\\Tontai.png")
                                            if point_exist > [(0, 0)]:
                                                exist = 1

                                                obj.swipe(510, 1212, 508, 526)
                                                obj.swipe(510, 1212, 508, 526)
                                                time.sleep(2)
                                                point_password = obj.find("img\\password_box.png")
                                                if point_password > [(0, 0)]:
                                                    obj.click(point_password[0][0], point_password[0][1])
                                                    time.sleep(1)
                                                    obj.input_clip(pass_user)
                                                    obj.swipe(510, 1212, 508, 526)
                                                    obj.swipe(510, 1212, 508, 526)
                                                    time.sleep(3)
                                                    point_sign_2 = obj.find("img\\sigin2.png")
                                                    if point_sign_2 > [(0, 0)]:
                                                        obj.click(point_sign_2[0][0], point_sign_2[0][1])
                                                    else:
                                                        flag = 1
                                                else:
                                                    flag = 1
                                        else:
                                            flag = 1
                                    else:
                                        flag = 1
                                else:
                                    flag = 1
                        else:
                            flag = 1
                    else:
                        flag = 1

                    time.sleep(10)
                    if flag == 1:
                        self.recheck_signal.emit(1)
                        self.status_signal.emit("Recheck", self.i)
                    else:
                        point_check = obj.find("img\\live1.png")
                        if point_check > [(0, 0)]:
                            self.live_signal.emit(1)
                            self.status_signal.emit("Live", self.i)
                            data_account.UpdateSqlStatus("live",id)
                        else:
                            if exist == 0:
                                point_red = obj.find("img\\die.png")
                                if point_red > [(0, 0)]:
                                    self.die_signal.emit(1)
                                    self.status_signal.emit("Die", self.i)
                                else:
                                    point_error = obj.find("img\\error.png")
                                    point_sign = obj.find("img\\sigin2.png")
                                    point_check = obj.find("img\\recheck.png")
                                    if point_error > [(0, 0)] or point_check > [(0, 0)] or point_sign > [0, 0]:
                                        self.recheck_signal.emit(1)
                                        self.status_signal.emit("Recheck", self.i)
                                    else:
                                        self.die_signal.emit(1)
                                        self.status_signal.emit("Die", self.i)
                            else:
                                point_sign = obj.find("img\\sigin2.png")
                                point_check = obj.find("img\\recheck.png")
                                if point_sign > [(0, 0)] or point_check > [(0, 0)]:
                                    self.recheck_signal.emit(1)
                                    self.status_signal.emit("Recheck", self.i)
                                else:
                                    self.die_signal.emit(1)
                                    self.status_signal.emit("Die", self.i)
                    time.sleep(2)
                    self.status_signal.emit("Done", self.i)
                else:
                    self.status_signal.emit("Error in SQL", self.i)
                    self.start = False
                    time.sleep(10)
            except:
                self.status_signal.emit("Something Error Rechecking...", self.i)
                time.sleep(2)
        self.status_signal.emit("Device Stopped", self.i)

    def check_stop(self):
        self.start = False




