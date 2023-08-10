import os,time
try:
 import threading,subprocess,base64,cv2,random
 import numpy as np
except:
  os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
  os.system("pip install numpy")
import threading,subprocess,base64,cv2,random
import numpy as np
from datetime import datetime

class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self):
        #os.system(f'adb -s {self.handle} exec-out screencap -p > {name}.png')
        pipe = subprocess.Popen(f'adb -s {self.handle} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image
    def click(self,x,y):
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
            text =  str(base64.b64encode(VN.encode('utf-8')))[1:]
            os.system(f"adb -s {self.handle} shell ime set com.android.adbkeyboard/.AdbIME")
            os.system(f"adb -s {self.handle} shell am broadcast -a ADB_INPUT_B64 --es msg {text}")
            return
        os.system(f"adb -s {self.handle} shell input text '{text}'")
    def find(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        #image = cv2.rectangle(img2, retVal[0],(retVal[0][0]+img.shape[0],retVal[0][1]+img.shape[1]), (0,250,0), 2)
        #cv2.imshow("test",image)
        #cv2.waitKey(0)
        #cv2.destroyWindow("test")
        return retVal
    def tapimg(self,img='',tap='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        tap = cv2.imread(tap)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        result2 = cv2.matchTemplate(img,tap,cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(result2 >= threshold)
        retVal2 = list(zip(*loc2[::-1]))
        if retVal > [(0, 0)]:
            self.click(retVal2[0][0],retVal2[0][1])
        else:
            return 0

def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
GetDevices()
thread_count = len(GetDevices())

class starts(threading.Thread):
    def __init__(self, nameLD,min_sleep,max_sleep, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
        self.min_sleep = min_sleep
        self.max_sleep = max_sleep
    def run(self):
        with open('cmt.txt',encoding='utf-8') as f:
            lis_cm = f.readlines()
            f.close()
        min_sleep = self.min_sleep
        max_sleep = self.max_sleep
        device = self.device
        d = Auto(device)
        def step1(d):
            c = 0
            while True:
                try:
                    c += 1
                    poin  = d.find('img\\3.png')
                    if poin > [(0, 0)] :
                        d.click(poin[0][0],poin[0][1])
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
                        step2(d)
                        break
                    poin2  = d.find('img\\1.png')
                    if poin2 > [(0, 0)] :
                        d.click(poin2[0][0],poin2[0][1])
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
                        step3(d)
                        break
                    poin3  = d.find('img\\5.png')
                    if poin3 > [(0, 0)] :
                        d.off('com.facebook.katana')
                        time.sleep(1)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thoat Tin | Time:", time.ctime(time.time()))
                        step1(d)
                        break
                    if c == 10:
                        d.off('com.facebook.katana')
                        time.sleep(1)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thoát lỗi | Time:", time.ctime(time.time()))
                        step1(d)
                        break
                except:
                    return 0
        def step2(d):
            c = 0
            while True:
                try:
                    c += 1
                    poin3  = d.find('img\\5.png')
                    if poin3 > [(0, 0)] :
                        time.sleep(1)
                        d.off('com.facebook.katana')
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thoat Tin | Time:", time.ctime(time.time()))
                        step1(d)
                        break
                    poin2  = d.find('img\\3.png')
                    if poin2 > [(0, 0)] :
                        d.click(poin2[0][0],poin2[0][1])
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
                        step2(d)
                        break
                    poin  = d.find('img\\1.png')
                    if poin > [(0, 0)] :
                        d.click(poin[0][0],poin[0][1])
                        step3(d)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Like | Time:", time.ctime(time.time()))
                        break
                    else:
                        time.sleep(2)
                        d.swipe(268,705,268,362)
                        time.sleep(2)
                        d.swipe(268,705,268,362)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Lướt | Time:", time.ctime(time.time()))
                    if c == 10:
                        d.off('com.facebook.katana')
                        time.sleep(1)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thoát lỗi | Time:", time.ctime(time.time()))
                        step1(d)
                        break
                except:
                    return 0
        def step3(d):
            i_sleep = random.randint(min_sleep,max_sleep)
            message=random.choice(lis_cm)
            cmt = message.split("\n")[0]
            c = 0
            while True:
                try:
                    c += 1
                    poin  = d.find('img\\2.png')
                    if poin > [(0, 0)] :
                        d.click(poin[0][0],poin[0][1])
                        time.sleep(2)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thực Hiện Cmt[",cmt,"] | Time:", time.ctime(time.time()))
                        step4(d)
                        d.InpuText(cmt)
                        time.sleep(4)
                    if c == 10:
                        d.off('com.facebook.katana')
                        time.sleep(1)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thoát lỗi | Time:", time.ctime(time.time()))
                        step1(d)
                        break
                except:
                    return 0
        def step4(d):
            i_sleep = random.randint(min_sleep,max_sleep)
            message=random.choice(lis_cm)
            cmt = message.split("\n")[0]
            c = 0
            while True:
                try:
                    c += 1
                    poin  = d.find('img\\6.png')
                    if poin > [(0, 0)] :
                        time.sleep(2)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thực Hiện Cmt[",cmt,"] | Time:", time.ctime(time.time()))
                        d.InpuText(cmt)
                        time.sleep(4)
                    poin2  = d.find('img\\4.png')
                    if poin2 > [(0, 0)] :
                        d.click(poin2[0][0],poin2[0][1])
                        time.sleep(1)
                        d.off('com.facebook.katana')
                        time.sleep(1)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Chờ [",i_sleep,"'] | Time:", time.ctime(time.time()))
                        time.sleep(i_sleep)
                        step1(d)
                        break
                    if c == 10:
                        d.off('com.facebook.katana')
                        time.sleep(1)
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Thoát lỗi | Time:", time.ctime(time.time()))
                        step1(d)
                        break
                except:
                    return 0
        step1(d)


min_sleep = int(input(">> Nhập số min sleep (s): "))
max_sleep = int(input(">> Nhập số max sleep (s): "))
def main(m):
        device = GetDevices()[m]
        for i in range(m, max_sleep, thread_count):
                run = starts(device,min_sleep,max_sleep,device,)
                run.run()

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()
