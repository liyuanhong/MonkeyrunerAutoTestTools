#coding:utf-8
import os
import threading
import time

import wx


class JudgeCrashService(threading.Thread):
    
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.adbPath = os.getcwd() + '\\..\\tools\\platform-tools\\'
        self.parent = parent
        self.ctr = 1
        self.sepaTime = 0.5
        
    def run(self):
        threading.Thread.run(self)
        self.ctr = 1
        while self.ctr == 1:
            time.sleep(self.sepaTime)
            readObj = os.popen(self.adbPath + 'getPidInfo.cmd')
            info = readObj.readlines()   
            readObj.close()
            if len(info) == 0:
                dialog = wx.MessageDialog(self.parent.parent.frame,self.parent.packageName + '已崩溃'.decode('UTF-8'),'消息'.decode('UTF-8'),wx.OK_DEFAULT)
                dialog.ShowModal()
                self.ctr = 0
                
            
    
    def stop(self):
        self.ctr = 0
