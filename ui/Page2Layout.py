#coding:utf-8
import os
import subprocess
import sys

import wx

from services import JudgeCrashService
from services.ShowLogService import ShowLogService
from services.StartCMD import StartCMD


class Page2Layout(object):
    
    def __init__(self,parent,page2):
        object.__init__(self)
        self.adbPath = os.getcwd() + '\\..\\tools\\platform-tools\\'
        self.logPath = os.getcwd() + '\\..\\temp\\log\\'
        #判断是否正在抓取日志
        self.isCapturing = False
        #判断抓取日志前，是否情况缓存
        self.isClearCache = True
        #设置过滤日志级别
        self.filterLevels = ['','Info','Debug','Verbose','Error','Warn','Fatal','Silent']
        self.filterLevel = ''
        self.parent= parent
        self.page2 = page2
        #要抓取的应用的pid
        self.pid = 0
        #设置日志区域是否自动滚动(1表示自动滚动，0表示不自动滚动)
        self.isAutoScroll = 1
        #是否开启崩溃判断，0表示不开启，1表示开启
        self.crashJudge = 0
        #将要执行的命令
        self.cmd = self.adbPath + 'adb logcat ' + '> ' + self.logPath + 'log.txt'
        self.logcatCMD = self.adbPath + 'adb logcat '
        self.cacheCMD = ''
        self.levelCMD = ''
        self.packageCMD = ''
        self.writeCMD = '> ' + self.logPath + 'log.txt'
        self.packageName = ''
        #将要执行的monkey命令
        self.monkey = self.adbPath + 'adb shell monkey'
        self.monkeyCMD1 = ''
        self.monkeyCMD2 = ''
        self.monkeyCMD3 = ''
        self.monkeyCMD4 = ''
        
        
        self.addPage1Layout()
        
    def addPage1Layout(self):
        page2BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.page2.SetSizer(page2BoxSizer)
        page2BoxSizer1 = wx.BoxSizer(wx.VERTICAL)
        
        filterPanel = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(520,100))
        label = wx.StaticText(filterPanel,wx.ID_ANY,u'命令：',pos = (0,5))
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.adbShellTxt = wx.TextCtrl(filterPanel,wx.ID_ANY,self.cmd,(40,0),(400,25))
        self.capLogcatBut = wx.Button(filterPanel,wx.ID_ANY,u'抓取日志',(445,0),wx.Size(70,25))
        self.capLogcatBut.Bind(wx.EVT_BUTTON,self.capLogcatButEVT)
        label = wx.StaticText(filterPanel,wx.ID_ANY,u'包名：',pos = (0,33))
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.packageFilter = wx.ComboBox(filterPanel,wx.ID_ANY,'',(40,30),(400,25))
        self.packageFilter.SetItems(self.getPackageList())
        self.packageFilter.Bind(wx.EVT_COMBOBOX,self.filterPackageEVT)
        self.refreshPackageListtBut = wx.Button(filterPanel,wx.ID_ANY,u'刷新',(445,30),wx.Size(70,25))
        self.refreshPackageListtBut.Bind(wx.EVT_BUTTON,self.refreshPackageListtButEVT)
        label = wx.StaticText(filterPanel,wx.ID_ANY,u'过滤：',pos = (0,65))
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.filterTxt = wx.TextCtrl(filterPanel,wx.ID_ANY,'',(40,60),(400,25))      
        self.exportLogBut = wx.Button(filterPanel,wx.ID_ANY,u'导出日志',(445,60),wx.Size(70,25))
        self.exportLogBut.Bind(wx.EVT_BUTTON,self.exportLogEVT)
        panel1 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(520,540))             
        self.logArea = wx.TextCtrl(panel1,wx.ID_ANY,size = wx.Size(520,540),pos = (0,0),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.VSCROLL)        
        
        page2BoxSizer2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(355,320))
        label = wx.StaticText(panel2,wx.ID_ANY,u'过滤级别：',pos = (5,5))
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.levelFilter = wx.ComboBox(panel2,wx.ID_ANY,'',(80,0),(100,25))
        self.levelFilter.SetItems(self.filterLevels)
        self.levelFilter.Bind(wx.EVT_COMBOBOX,self.filterLevelEVT)
        self.radioScrollBut = wx.RadioButton(panel2,wx.ID_ANY,u'滚动',(200,5),style = wx.RB_GROUP)
        self.radioNoScrollBut = wx.RadioButton(panel2,wx.ID_ANY,u'不滚动',(260,5)) 
        self.radioScrollBut.Bind(wx.EVT_RADIOBUTTON, self.autoScrollCtrEVT)
        self.radioNoScrollBut.Bind(wx.EVT_RADIOBUTTON, self.autoScrollCtrEVT)
        label = wx.StaticText(panel2,wx.ID_ANY,u'抓取前是否清空缓存：',pos = (5,33))
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.radioClearBut = wx.RadioButton(panel2,wx.ID_ANY,u'否',(200,33),style = wx.RB_GROUP)
        self.radioNotClearBut = wx.RadioButton(panel2,wx.ID_ANY,u'是',(260,33)) 
        self.radioClearBut.Bind(wx.EVT_RADIOBUTTON,self.clearCacheEVT)
        self.radioNotClearBut.Bind(wx.EVT_RADIOBUTTON,self.clearCacheEVT)
        label = wx.StaticText(panel2,wx.ID_ANY,u'应用程序崩溃判断开关：',pos = (5,61))
        label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.radioCrashJudgeCloseBut = wx.RadioButton(panel2,wx.ID_ANY,u'关闭',(200,61),style = wx.RB_GROUP)
        self.radioCrashJudgeOpenBut = wx.RadioButton(panel2,wx.ID_ANY,u'打开',(260,61)) 
        self.radioCrashJudgeCloseBut.Bind(wx.EVT_RADIOBUTTON,self.crashJudgeEVT)
        self.radioCrashJudgeOpenBut.Bind(wx.EVT_RADIOBUTTON,self.crashJudgeEVT)
        
        panel3 = wx.Panel(self.page2,wx.ID_ANY,size = wx.Size(355,320),style = wx.BORDER_SIMPLE)
        self.monkeyCMDArea =  wx.TextCtrl(panel3,wx.ID_ANY,size = wx.Size(350,100),pos = (0,0),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE)
        self.monkeyCMDArea.SetValue(self.monkey)
        label = wx.StaticText(panel3,wx.ID_ANY,u'monkey测试使用命令行更方便灵活，这里不做集成。',pos = (0,100))
        
        
        page2BoxSizer.Add(page2BoxSizer1)
        page2BoxSizer1.Add(filterPanel)
        page2BoxSizer1.Add(panel1)
        page2BoxSizer.Add(page2BoxSizer2)
        page2BoxSizer2.Add(panel2)
        page2BoxSizer2.Add(panel3)

    def endLogcatEVT(self,event):
        cmd = '..\\closeCMD'
        os.system(cmd)  
            
    def capLogcatButEVT(self,event):   
        readObj = os.popen(self.adbPath + 'adb devices')
        judge = readObj.readlines()
        readObj.close()
        if len(judge) == 3:        
            if self.isCapturing == False:
                self.capLogcatBut.SetLabel(u'结束抓取')
                self.logArea.SetValue('')
                file = open(self.logPath + 'log.txt','w')
                file.write('')
                file.close()
                capService = StartCMD(self.cmd)
                capService.start()      
                self.showLogSer = ShowLogService(self,self.logPath,self.logArea)
                self.showLogSer.start()    
                self.isCapturing = True    
                if self.crashJudge == 1:
                    crashJudege = JudgeCrashService.JudgeCrashService(self)
                    crashJudege.stop() 
                    crashJudege.start() 
                elif self.crashJudge == 0:
                    pass      
            elif self.isCapturing == True:
                self.capLogcatBut.SetLabel(u'抓取日志')            
                cmd = '..\\closeCMD'
                os.system(cmd)
                self.showLogSer.stop()
                self.isCapturing = False
        else:
            dialog = wx.MessageDialog(self.parent.frame,'连接已中断，请连接手机！'.decode('UTF-8'),'消息'.decode('UTF-8'),wx.OK_DEFAULT)
            dialog.ShowModal()
            
    def getPackageList(self):
            cmd = self.adbPath + 'adb shell pm list package'
            readObj = os.popen(cmd)
            self.packageList = readObj.readlines()
            try:
                readObj.close()
            except Exception,e:
                print e
            self.packageList.insert(0,'')
            for i in range(0,len(self.packageList)):
                self.packageList[i] = self.packageList[i].replace('\n','').replace("package:",'')
            return self.packageList
        
    def refreshPackageListtButEVT(self,event):
        readObj = os.popen(self.adbPath + 'adb devices')
        judge = readObj.readlines()
        readObj.close()
        if len(judge) == 3:
            cmd = self.adbPath + 'adb shell pm list package'
            readObj = os.popen(cmd)
            self.packageList = readObj.readlines()
            readObj.close()
            self.packageList.insert(0,'')
            for i in range(0,len(self.packageList)):
                self.packageList[i] = self.packageList[i].replace('\n','').replace("package:",'')
            self.packageFilter.SetItems(self.packageList)
        else:
            dialog = wx.MessageDialog(self.parent.frame,'连接已中断，请连接手机！'.decode('UTF-8'),'消息'.decode('UTF-8'),wx.OK_DEFAULT)
            dialog.ShowModal()
            
    def autoScrollCtrEVT(self,event):
        if event.GetId() == self.radioScrollBut.GetId():
            self.isAutoScroll = 1
        elif event.GetId() == self.radioNoScrollBut.GetId():
            self.isAutoScroll = 0
            
    def exportLogEVT(self,event):
        dlg = wx.FileDialog(self.parent.frame,"",os.getcwd(), "", "XYZ files (*.log)|*.log", style=wx.SAVE)
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            file = open(path,'w')
            file.write(self.logArea.GetValue())
            file.close()
        dlg.Destroy()
        
    def clearCacheEVT(self,event):
        if event.GetId() == self.radioClearBut.GetId():
            self.cacheCMD = ' '
            self.setCmdTxt()
            self.isClearCache = True
        elif event.GetId() == self.radioNotClearBut.GetId():
            self.cacheCMD = self.adbPath + 'adb logcat -c && '
            self.setCmdTxt()
            self.isClearCache = False
                  
    def filterLevelEVT(self,event):
        level = self.filterLevels[self.levelFilter.GetSelection()]
        if level == '':
            self.levelCMD = ' '
            self.setCmdTxt()
        elif level == 'Info':
            self.levelCMD = '*:I '
            self.setCmdTxt()
        elif level == 'Debug':
            self.levelCMD = '*:D '
            self.setCmdTxt()
        elif level == 'Verbose':
            self.levelCMD = '*:V '
            self.setCmdTxt()
        elif level == 'Error':
            self.levelCMD = '*:E '
            self.setCmdTxt()
        elif level == 'Warn':
            self.levelCMD = '*:W '
            self.setCmdTxt()
        elif level == 'Fatal':
            self.levelCMD = '*:F '
            self.setCmdTxt()
        elif level == 'Silent':
            self.levelCMD = '*:S '
            self.setCmdTxt()
            
    def setCmdTxt(self):
        self.cmd = self.cmd = self.cacheCMD + self.logcatCMD + self.levelCMD + self.packageCMD + self.writeCMD
        self.adbShellTxt.SetValue(self.cmd)
        
    def filterPackageEVT(self,event):
        readObj = os.popen(self.adbPath + 'adb devices')
        judge = readObj.readlines()
        readObj.close()
        if len(judge) == 3:
            cmd = '''@echo off
adb shell "ps | grep '''       
            index = self.packageFilter.GetSelection()
            package = self.packageList[index]
            self.packageName = package
            if package == '':
                self.packageCMD = ' '
                self.setCmdTxt()
            else:
                cmd = cmd + package + '\"'
                file2 = open(self.adbPath + 'getPidInfo.cmd','w')
                file2.write(cmd)
                file2.close()               
                readObj = os.popen(self.adbPath + 'getpid.cmd')
                self.pid = readObj.readlines()       
                readObj.close()                
                self.packageCMD = '| find ' +  '\"' + self.pid[0].replace('\n','') + '\" '
                self.setCmdTxt()
        else:
            dialog = wx.MessageDialog(self.parent.frame,'连接已中断，请连接手机！'.decode('UTF-8'),'消息'.decode('UTF-8'),wx.OK_DEFAULT)
            dialog.ShowModal()
        
    def crashJudgeEVT(self,event):
        if event.GetId() == self.radioCrashJudgeOpenBut.GetId():
            self.crashJudge = 1
        elif event.GetId() == self.radioCrashJudgeCloseBut.GetId():
            self.crashJudge = 0
        
    
        
        
        
        
            
        
        
    

        
        
    
        
