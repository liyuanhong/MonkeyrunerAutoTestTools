#coding:utf-8
import os
import subprocess
import sys

import wx

from services.StartCMD import StartCMD


class Page2Layout(object):
    
    def __init__(self,parent,page2):
        object.__init__(self)
        self.adbPath = os.getcwd() + '\\..\\tools\\platform-tools\\'
        
        self.parent= parent
        self.page2 = page2
        self.pid = 0
        
        
        self.addPage1Layout()
        
    def addPage1Layout(self):
        page2BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.page2.SetSizer(page2BoxSizer)
        page2BoxSizer1 = wx.BoxSizer(wx.VERTICAL)
        
        filterPanel = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(520,100))
        wx.StaticText(filterPanel,wx.ID_ANY,u'命令：',pos = (0,0))
        self.adbShellTxt = wx.TextCtrl(filterPanel,wx.ID_ANY,'adb logcat',(35,0),(400,20))
        
        
        
        panel1 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(520,540))
              
#         panel1.SetBackgroundColour("#ff0000")
        self.logArea = wx.TextCtrl(panel1,wx.ID_ANY,size = wx.Size(520,540),pos = (0,0),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.HSCROLL)        
        
        page2BoxSizer2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(355,320))
#         panel2.SetBackgroundColour("#00ff00")
        self.closeLogcatBut = wx.Button(panel2,wx.ID_ANY,u'结束日志',(0,0),wx.Size(70,25))
        self.closeLogcatBut.Bind(wx.EVT_BUTTON,self.endLogcatEVT)
        
        panel3 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(355,320),style = wx.BORDER_SIMPLE)
        panel3.SetBackgroundColour("#0000ff")
        
        page2BoxSizer.Add(page2BoxSizer1)
        page2BoxSizer1.Add(filterPanel)
        page2BoxSizer1.Add(panel1)
        page2BoxSizer.Add(page2BoxSizer2)
        page2BoxSizer2.Add(panel2)
        page2BoxSizer2.Add(panel3)
  
  
#         cmd = self.adbPath + 'adb shell pm list package'
#         a = os.popen(cmd).readlines()        
#         for i in range(0,len(a)):
#             print a[i].replace('\n','').replace("package:",'')
            
#         cmd1 = 'adb logcat -c && adb logcat *:V | find \"com.example.testprogram\"'
#         print cmd1


        self.pid = os.popen(self.adbPath + 'getpid.cmd').readlines()
        print self.pid
        cmd2 = self.adbPath + 'adb logcat *:E | find ' +  '\"' + self.pid[0].replace('\n','') + '\"'
        a = StartCMD(cmd2)
        a.start()

    def endLogcatEVT(self,event):
            cmd = '..\\closeCMD'
            os.system(cmd)  
            
        
        
    

        
        
    
        
