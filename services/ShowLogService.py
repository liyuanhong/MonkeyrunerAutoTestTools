#coding:utf-8
import os
import threading
import time


class ShowLogService(threading.Thread):
    
    def __init__(self,parent,logPath,logArea):
        threading.Thread.__init__(self)
        self.sepaTime = 0.5
        self.ctr = 1
        self.log = ''
        self.parent = parent
        self.logPath = logPath
        self.logArea = logArea
                      
    
    def run(self):
        threading.Thread.run(self)
        print 
        while self.ctr == 1:
            time.sleep(self.sepaTime)
            if self.parent.filterTxt.GetValue() == '':
                if self.parent.isAutoScroll == 1:
                    self.file = open(self.logPath + 'log.txt','r')
                    self.log = self.file.read()
                    self.logArea.SetValue(self.log.decode('utf-8'))
                    self.logArea.ShowPosition(self.logArea.GetLastPosition())
                elif self.parent.isAutoScroll == 0:
                    pass
                self.file.close()
            else:
                if self.parent.isAutoScroll == 1:
                    self.file = open(self.logPath + 'log.txt')
                    logs = ''
                    for log in self.file: 
                        log = log.decode('utf-8')
                        if log.find(self.parent.filterTxt.GetValue()) != -1:
                            logs += log
                    self.logArea.SetValue(logs)
                    self.logArea.ShowPosition(self.logArea.GetLastPosition())
                elif self.parent.isAutoScroll == 0:
                    pass
                self.file.close()
        
    def stop(self):
        self.ctr = 0