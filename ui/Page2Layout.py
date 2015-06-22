#coding:utf-8
import os
import subprocess

import wx


class Page2Layout(object):
    
    def __init__(self,parent,page2):
        object.__init__(self)
        self.adbPath = os.getcwd() + '\\..\\tools\\platform-tools\\'
        
        self.parent= parent
        self.page2 = page2
        
        
        self.addPage1Layout()
        
    def addPage1Layout(self):
        page2BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.page2.SetSizer(page2BoxSizer)
        panel1 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(520,640))
#         panel1.SetBackgroundColour("#ff0000")
        self.logArea = wx.TextCtrl(panel1,wx.ID_ANY,size = wx.Size(520,640),pos = (0,0),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.HSCROLL)        
        
        page2BoxSizer1 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(355,320),style = wx.BORDER_SIMPLE)
        panel2.SetBackgroundColour("#00ff00")
        
        panel3 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(355,320),style = wx.BORDER_SIMPLE)
        panel3.SetBackgroundColour("#0000ff")
        
        page2BoxSizer.Add(panel1)
        page2BoxSizer.Add(page2BoxSizer1)
        page2BoxSizer1.Add(panel2)
        page2BoxSizer1.Add(panel3)
  
  
  
  
  
  
  
  
  
  
  
  
        
        cmd = self.adbPath + 'adb shell pm list package'
        a = os.popen(cmd).readlines()        
        for i in range(0,len(a)):
            print a[i].replace('\n','').replace("package:",'')
        
        
    
        
