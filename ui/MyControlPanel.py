#coding=utf-8
import subprocess
import wx
from widget import TabPage


class MyControlPanel(): 
    def __init__(self,panel2Page2,isRecord):
        self.panel2Page2 = panel2Page2
        self.isRecord = isRecord
        self.init()
        
    def init(self):
        buttonHome = wx.Button(self.panel2Page2,wx.ID_ANY,u'Home键',(5,5),wx.Size(70,25))
        buttonBack = wx.Button(self.panel2Page2,wx.ID_ANY,u'返回键',(5,35),wx.Size(70,25))
        buttonMenu = wx.Button(self.panel2Page2,wx.ID_ANY,u'菜单键',(5,65),wx.Size(70,25))
        buttonVoiceUp = wx.Button(self.panel2Page2,wx.ID_ANY,u'音量+',(5,95),wx.Size(70,25))
        buttonVoiceDown = wx.Button(self.panel2Page2,wx.ID_ANY,u'音量-',(5,125),wx.Size(70,25))
        buttonLongPressHome = wx.Button(self.panel2Page2,wx.ID_ANY,u'长按Home键',(5,155),wx.Size(100,25))
        buttonHome.Bind(wx.EVT_BUTTON,self.sendHomeEVT)
        buttonBack.Bind(wx.EVT_BUTTON,self.sendBackEVT)
        buttonMenu.Bind(wx.EVT_BUTTON,self.sendMenuEVT)
        buttonVoiceUp.Bind(wx.EVT_BUTTON,self.sendVoiceUpEVT)
        buttonVoiceDown.Bind(wx.EVT_BUTTON,self.sendVoiceDownEVT)
        buttonLongPressHome.Bind(wx.EVT_BUTTON,self.sendLongPressHomeEVT)
        
        
    def sendHomeEVT(self,event):
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            if self.scriptType == 0:
#                 scp1 = 'device.touch(' + str(x) + ',' + str(y) + ',"DOWN_AND_UP")'
#                 scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
#                 shot = ''
                if self.screenShotType == 0:
                    pass
                elif self.screenShotType == 1:
                    pass
                elif self.screenShotType == 2:
                    pass
            elif self.scriptType == 1: 
                if self.screenShotType == 0:
                    pass
                elif self.screenShotType == 1:
                    pass
                elif self.screenShotType == 2:
                    pass
                
        cmd = 'adb shell input keyevent 3'
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
#         os.system(cmd)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    def sendBackEVT(self,event):
        cmd = 'adb shell input keyevent 4'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    def sendMenuEVT(self,event):
        cmd = 'adb shell input keyevent 82'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    def sendVoiceUpEVT(self,event):
        cmd = 'adb shell input keyevent 24'
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
#         os.system(cmd)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    def sendVoiceDownEVT(self,event):
        cmd = 'adb shell input keyevent 25'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    def sendLongPressHomeEVT(self,event):
        cmd = 'adb shell input keyevent --longpress 3'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass