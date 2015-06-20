#coding:utf-8

import os
import threading

#����Ʒ��˿ռ�ѵ���
class StartMonkeyService(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.monParh = '..\\tools\\tools\\'

#     def run(self):
#         cmd = 'monkeyrunner ' + os.getcwd()
#         cmd = cmd + '\\..\\services\\MonkeyGetBitmapService.py'
#         os.system(cmd)
        
    def run(self):
        cmd = self.monParh + 'monkeyrunner  %cd%/../services/MonkeyGetBitmapService.py'
        os.system(cmd)