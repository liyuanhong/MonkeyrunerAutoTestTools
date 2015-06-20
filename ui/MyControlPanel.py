#coding=utf-8
import subprocess
import wx
from widget import TabPage


class MyControlPanel(): 
    def __init__(self,panel2Page2,parent,delayTime,scriptArea,mokeyCode,dosCode):
        self.panel2Page2 = panel2Page2
        self.parent = parent
        self.delayTime = delayTime
        self.scriptArea = scriptArea
        self.mokeyCode = mokeyCode
        self.dosCode = dosCode
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
        cmd = self.parent.adbPath + 'adb shell input keyevent 3'
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.parent.getIsRecord() == 0:
            pass
        elif self.parent.getIsRecord() == 1:
            if self.parent.getScriptType() == 0:
                scp1 = 'device.press("KEYCODE_HOME","DOWN_AND_UP")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                scp = scp1+scp2
                shot = ''
                self.recordMonkeyScript(scp, shot)
            elif self.parent.getScriptType() == 1: 
                scp1 = cmd
                scp2 = scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.recordDosScript(scp, shot)

    def sendBackEVT(self,event):
        cmd = self.parent.adbPath + 'adb shell input keyevent 4'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.parent.getIsRecord() == 0:
            pass
        elif self.parent.getIsRecord() == 1:
            if self.parent.getScriptType() == 0:
                scp1 = 'device.press("KEYCODE_BACK","DOWN_AND_UP")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                scp = scp1+scp2
                shot = ''
                self.recordMonkeyScript(scp, shot)
            elif self.parent.getScriptType() == 1: 
                scp1 = cmd
                scp2 = scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.recordDosScript(scp, shot)
    def sendMenuEVT(self,event):
        cmd = self.parent.adbPath + 'adb shell input keyevent 82'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.parent.getIsRecord() == 0:
            pass
        elif self.parent.getIsRecord() == 1:
            if self.parent.getScriptType() == 0:
                scp1 = 'device.press("KEYCODE_MENU","DOWN_AND_UP")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                scp = scp1+scp2
                shot = ''
                self.recordMonkeyScript(scp, shot)
            elif self.parent.getScriptType() == 1: 
                scp1 = cmd
                scp2 = scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.recordDosScript(scp, shot)
    def sendVoiceUpEVT(self,event):
        cmd = self.parent.adbPath + 'adb shell input keyevent 24'
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
#         os.system(cmd)
        if self.parent.getIsRecord() == 0:
            pass
        elif self.parent.getIsRecord() == 1:
            if self.parent.getScriptType() == 0:
                scp1 = 'device.press("KEYCODE_VOLUME_UP","DOWN_AND_UP")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                scp = scp1+scp2
                shot = ''
                self.recordMonkeyScript(scp, shot)
            elif self.parent.getScriptType() == 1: 
                scp1 = cmd
                scp2 = scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.recordDosScript(scp, shot)
    def sendVoiceDownEVT(self,event):
        cmd = self.parent.adbPath + 'adb shell input keyevent 25'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.parent.getIsRecord() == 0:
            pass
        elif self.parent.getIsRecord() == 1:
            if self.parent.getScriptType() == 0:
                scp1 = 'device.press("KEYCODE_VOLUME_DOWN","DOWN_AND_UP")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                scp = scp1+scp2
                shot = ''
                self.recordMonkeyScript(scp, shot)
            elif self.parent.getScriptType() == 1: 
                scp1 = cmd
                scp2 = scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.recordDosScript(scp, shot)
    def sendLongPressHomeEVT(self,event):
        cmd = self.parent.adbPath + 'adb shell input keyevent --longpress 3'
#         os.system(cmd)
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.parent.getIsRecord() == 0:
            pass
        elif self.parent.getIsRecord() == 1:
            if self.parent.getScriptType() == 0:
                scp1 = 'device.press("KEYCODE_HOME","DOWN")\nMonkeyRunner.sleep("2")\ndevice.press("KEYCODE_HOME","UP")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                scp = scp1+scp2
                shot = ''
                self.recordMonkeyScript(scp, shot)
            elif self.parent.getScriptType() == 1: 
                scp1 = cmd
                scp2 = scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.recordDosScript(scp, shot)        
        
    def recordMonkeyScript(self,scp,shot):
        if self.parent.getScreentShotType() == 0:
            shot = ''
        elif self.parent.getScreentShotType() == 1:
            shot = ''
        elif self.parent.getScreentShotType() == 2:
            shot = ''
        scp = scp + shot + '\n\n'
        self.mokeyCode.append(scp)
        self.parent.addMonkeyCodeIndex()
        self.scriptArea.SetValue(self.parent.getCodeFromList(self.mokeyCode))
        self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
        
    def recordDosScript(self,scp,shot):
        if self.parent.getScreentShotType() == 0:
            shot = ''
        elif self.parent.getScreentShotType() == 1:
            shot = ''
        elif self.parent.getScreentShotType() == 2:
            shot = ''
        scp = scp + shot + '\n'
        self.dosCode.append(scp)
        self.parent.addDosCodeIndex()
        self.scriptArea.SetValue(self.parent.getCodeFromList(self.dosCode))
        self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())