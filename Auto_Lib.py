import os
try:
    import threading, subprocess, base64, cv2, random
    import numpy as np
except:
    os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
    os.system("pip install numpy")
import subprocess, base64, cv2
import numpy as np

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