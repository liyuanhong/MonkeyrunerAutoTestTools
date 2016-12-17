#coding:utf-8

import os
import threading
import sys

#����Ʒ��˿ռ�ѵ���
class StartMonkeyService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #cmd = 'monkeyrunner ' + os.getcwd()
        cmd = 'monkeyrunner ' + sys.path[0]
        cmd = cmd + '\\..\\services\\MonkeyGetBitmapService.py'
        os.system(cmd)