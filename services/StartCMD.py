#coding:utf-8
import os
import threading

class StartCMD(threading.Thread):
    
    def __init__(self,cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
        
    def run(self):
        self.logcat = os.system(self.cmd)
        
    
