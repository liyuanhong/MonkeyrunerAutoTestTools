#coding:utf-8

import os
import threading

#����Ʒ��˿ռ�ѵ���
class StartMonkeyService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        cmd = 'monkeyrunner ' + os.getcwd()
        cmd = cmd + '\\..\\services\\MonkeyGetBitmapService.py'
        os.system(cmd)