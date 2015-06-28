#coding:utf-8

from mhlib import PATH
import os, sys
import subprocess
import thread

from wx import Size
import wx

from bean import ScreenRate
from services import StartMonkeyService, ShowScreenService
from ui import MyControlPanel
from ui.Page2Layout import Page2Layout
from widget import  TabPage


curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
sys.path.append(curPath + '\\..')
sys.path.append(curPath + '\\..\\widget')
sys.path.append(curPath + '\\..\\services')
sys.path.append(curPath + '\\..\\util')














class MyClass(object):

    def __init__(self, params):
        #定义窗体尺寸
        self.winSize = wx.Size(900,730)
        #刷新率默认为0.05秒每次
        self.freshRate = 0.05
        #动态显示手机屏幕的线程
        self.connectThread = None
        #截图保存路径
        self.picPath = 'D:\screenshot'
        #定义屏幕操作的类型，0表示点击，1表示滑动，2表示左右滑动，3表示上下滑动，4表示长按
        self.eventType = 0
        #定义录制脚本的类型，0表示monkeyrunner脚本，1表示DOS脚本
        self.scriptType = 0
        #定义显示与真实屏幕的比例
        self.screenRate = ScreenRate.ScreenRate()
        #定义拖动的起始点
        self.startPosition = (0,0)
        #定义拖动的结束点
        self.endPosition = (0,0)
        #截图的方式0表示自动，1表示手动,2表示不截图
        self.screenShotType = 1
        self.screenIndex = 0
        self.dosScreenIndex = 0
        #是否录制脚本0，表示 不录制，1表示录制
        self.isRecord = 0
        #将要录制的代码部分
        self.mokeyCode = []
        self.dosCode = []
        self.exportMonkeyCode = []
        self.exportDosCode = []
        #当前代码的录制索引
        self.monkeyCodeIndex = 0
        self.dosCodeIndex = 0
        #定义adb执行的路径
        self.adbPath = os.getcwd() + '\\..\\tools\\platform-tools\\'
        #定义了monkeyrunner的执行路径
        self.monParh = os.getcwd() + '\\..\\tools\\tools\\'
        #定义脚本的前部分代码
        self.txt = '''import sys
import time
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
device = MonkeyRunner.waitForConnection()\n\n'''
        self.exportMonkeyCode.append(self.txt)
        self.dosTxt = ''
        self.exportDosCode.append(self.dosTxt)
        
    
    #显示主窗体
    def show(self):
        win = wx.App()
        self.frame = wx.Frame(None, -1, 'simple.py',size = self.winSize) 
        nb = wx.Notebook(self.frame,wx.NewId())    
        menuBar = wx.MenuBar()
        
        #添加tab标签页
        page1 = TabPage.TabPage(nb)
        self.page2 = TabPage.TabPage(nb)
        nb.AddPage(page1,u'录制脚本')
        self.addPage1Layout(self.frame, page1);
        
        nb.AddPage(self.page2,u'monkey与日志')                   
        self.addMenu(menuBar,self.frame);
        
        self.frame.SetMenuBar(menuBar);
        self.frame.Bind(wx.EVT_CLOSE,self.closeWinEVT)
        self.frame.Show()
        win.MainLoop()
      
    #添加菜单项  
    def addMenu(self,menuBar,frame):
        menuFile = wx.Menu()
        menuOpenItem = wx.MenuItem(menuFile,wx.NewId(),text = u"打开脚本")
        menuSaveAsItem = wx.MenuItem(menuFile,wx.ID_ANY,text = u"导出Monkeyrunner脚本")
        menuSaveAsItem1 = wx.MenuItem(menuFile,wx.ID_ANY,text = u"导出Dos脚本")
        menuSaveItem = wx.MenuItem(menuFile,wx.ID_ANY,text = u"保存")
        menuExitItem = wx.MenuItem(menuFile,wx.NewId(),text = u"退出")
        menuFile.Append(menuOpenItem.GetId(),u"打开脚本")
        menuFile.Append(menuSaveAsItem.GetId(),u"导出Monkeyrunner脚本")
        menuFile.Append(menuSaveAsItem1.GetId(),u"导出Dos脚本")
        menuFile.Append(menuSaveItem.GetId(),u"保存")            
        menuFile.Append(menuExitItem.GetId(),u"退出")
        frame.Bind(wx.EVT_MENU, self.myExit,menuExitItem)
        frame.Bind(wx.EVT_MENU,self.exportMonkeyScriptEVT,menuSaveAsItem)
        frame.Bind(wx.EVT_MENU,self.exportDosScriptEVT,menuSaveAsItem1)
        menuOpenItem.Enable(False)
        menuSaveItem.Enable(False)
        
        menuControl = wx.Menu()
        menuClearDos = wx.MenuItem(menuControl,wx.ID_ANY,text = u"清空Dos脚本")
        menuClearMon = wx.MenuItem(menuControl,wx.ID_ANY,text = u"清空Monkeyrunner脚本")
        menuRerecord = wx.MenuItem(menuControl,wx.ID_ANY,text = u"重新录制")
        menuCancleRerecord = wx.MenuItem(menuControl,wx.ID_ANY,text = u"撤销录制")
        playMonScript = wx.MenuItem(menuControl,wx.ID_ANY,text = u"回放Monkeyrunner脚本")
        menuControl.Append(menuRerecord.GetId(), u"重新录制")       
        menuControl.Append(menuClearMon.GetId(), u"清空Monkeyrunner脚本")   
        menuControl.Append(menuClearDos.GetId(), u"清空Dos脚本")  
        menuControl.Append(menuCancleRerecord.GetId(), u"撤销录制")
        menuControl.Append(playMonScript.GetId(), u"回放Monkeyrunner脚本")
         
        frame.Bind(wx.EVT_MENU,self.reRecordEVT,menuRerecord) 
        frame.Bind(wx.EVT_MENU,self.clearMonCodeEVT,menuClearMon) 
        frame.Bind(wx.EVT_MENU,self.clearDosCodeEVT,menuClearDos) 
        frame.Bind(wx.EVT_MENU,self.cancleRerecordEVT,menuCancleRerecord)
        frame.Bind(wx.EVT_MENU,self.playMonScriptEVT,playMonScript)
        
        
        menuAbout = wx.Menu()
        menuVersoin = wx.MenuItem(menuAbout,wx.ID_ANY,text = u"版本")
        menuAbout.Append(menuVersoin.GetId(), u"版本")
        frame.Bind(wx.EVT_MENU,self.showVersionEVT,menuVersoin)
        
          
        menuBar.Append(menuFile,u"文件")
        menuBar.Append(menuControl,u"控制")
        menuBar.Append(menuAbout,u"关于")
    
    #录制脚本页面页面布局
    def addPage1Layout(self,frame,page1):
        page1BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        page1.SetSizer(page1BoxSizer)
        self.panel1 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(360,640))
        self.panel1.SetBackgroundColour("#aaaa00")
        
        img = wx.Image('..\\pic\\阳光小秒拍.png'.decode('utf-8'),wx.BITMAP_TYPE_PNG,-1)
        self.height = img.GetHeight()
        self.width = img.GetWidth()
        img.Rescale(self.width/2,self.height/2)
        bitmap = img.ConvertToBitmap()               
        self.panel1.SetAutoLayout(True)
        backgroundImage = wx.StaticBitmap(self.panel1,wx.ID_ANY,bitmap)
        
        page1BoxSizer2 = wx.BoxSizer(wx.VERTICAL)        
        panel2 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,300))
#         panel2.SetBackgroundColour("#00aaaa")       
        nb = wx.Notebook(panel2,wx.ID_ANY,(10,0),size = wx.Size(508,300))
        
        #连接面板添加布局
        panel2Page1 = TabPage.TabPage(nb)
#         panel2Page1.SetBackgroundColour("#ff0000")
        buttonCon = wx.Button(panel2Page1,wx.ID_ANY,u'连接手机',(5,5),wx.Size(70,25))
        frame.Bind(wx.EVT_BUTTON,lambda evt, mark=0 : self.startConnect(frame, buttonCon, img, self.width, self.height, bitmap, backgroundImage, self.panel1,panel2Txt1),buttonCon)
        buttonDisCon = wx.Button(panel2Page1,wx.ID_ANY,u'中断连接',(80,5),wx.Size(70,25))
        frame.Bind(wx.EVT_BUTTON,lambda evt, mark=0 : self.endConnect(buttonCon, self.connectThread),buttonDisCon)
        #给背景图片添加点击事件，而不是给panel添加事件
        backgroundImage.Bind(wx.EVT_MOUSE_EVENTS,self.screenEVT)
        
        
        panel2panel0 = wx.Panel(panel2Page1,wx.ID_ANY,(5,35),wx.Size(145,80),wx.BORDER_SIMPLE | wx.TE_MULTILINE )
#         panel2panel0.SetBackgroundColour("#ff0000")
        panel2Txt1 = wx.TextCtrl(panel2panel0,wx.ID_ANY,u"phone:sanxing\nwidth:720\nheight:1280",(0,0),wx.Size(145,80),wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        panel2Txt1.SetEditable(False)      
        radioClickBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'点击',(190,10),style = wx.RB_GROUP)
        radioDragBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'拖曳',(190,30))       
        radioPressBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'长按',(190,80))
        
        wx.StaticText(panel2Page1,wx.ID_ANY,u'坐标：',pos = (250,10))
        self.coodinate = wx.TextCtrl(panel2Page1,wx.ID_ANY,'(0,0)',(290,10),(180,20))
        self.coodinate.SetEditable(False) 
        
        radioLeftAndRight = wx.RadioButton(panel2Page1,wx.ID_ANY,u'左右',(250,50),style = wx.RB_GROUP)
        radioUpAndDown = wx.RadioButton(panel2Page1,wx.ID_ANY,u'上下',(320,50))
        
        wx.StaticText(panel2Page1,wx.ID_ANY,u'长按时长：',pos = (190,100))
        self.longPressTxt = wx.TextCtrl(panel2Page1,wx.ID_ANY,'5',size = (100,20),pos = (250,100))
        wx.StaticText(panel2Page1,wx.ID_ANY,u'秒',pos = (355,100))
        
        self.recordButOff = wx.RadioButton(panel2Page1,wx.ID_ANY,u'停止录制',(5,125),style = wx.RB_GROUP)
        self.recordButOn = wx.RadioButton(panel2Page1,wx.ID_ANY,u'开始录制',(80,125))
        self.recordButOn.Bind(wx.EVT_RADIOBUTTON,self.recordButEVT)
        self.recordButOff.Bind(wx.EVT_RADIOBUTTON,self.recordButEVT)
        
        self.inputText = wx.TextCtrl(panel2Page1,wx.ID_ANY,'',(190,130),(160,25))
        inputBut = wx.Button(panel2Page1,wx.ID_ANY,u'输入',(360,130),wx.Size(50,25))
        delBut = wx.Button(panel2Page1,wx.ID_ANY,u'DEL',(420,130),wx.Size(50,25))
        inputBut.Bind(wx.EVT_BUTTON,self.inputTextEVT)
        delBut.Bind(wx.EVT_BUTTON,self.delTextEVT)
        
        wx.Panel(panel2Page1,wx.ID_ANY,pos = (165,0),size = wx.Size(1,160),style = wx.BORDER_SIMPLE)
        wx.Panel(panel2Page1,wx.ID_ANY,pos = (0,165),size = wx.Size(508,1),style = wx.BORDER_SIMPLE)
        
        radioLeftAndRight.Enable(False)
        radioUpAndDown.Enable(False)
        self.longPressTxt.SetEditable(False)
        
        wx.StaticText(panel2Page1,wx.ID_ANY,u'事件延时：',pos = (5,175))
        self.delayTime = wx.TextCtrl(panel2Page1,wx.ID_ANY,'2',(65,175),(80,20))
        wx.StaticText(panel2Page1,wx.ID_ANY,u'秒',pos = (150,175))
        
        wx.StaticText(panel2Page1,wx.ID_ANY,u'脚本类型：',pos = (5,200))
        self.monkeyBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'monkeyrunner脚本',(5,220),style = wx.RB_GROUP)
        self.dosBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'DOS脚本',(5,240))
        self.monkeyBut.Bind(wx.EVT_RADIOBUTTON,self.changeCodeTypeEVT)
        self.dosBut.Bind(wx.EVT_RADIOBUTTON,self.changeCodeTypeEVT)
        
        wx.StaticText(panel2Page1,wx.ID_ANY,u'添加截图：',pos = (190,175))
        self.radioManShotBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'手动截图',(350,175),style = wx.RB_GROUP)
        self.radioAutoShotBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'自动截图',(260,175))      
        wx.StaticText(panel2Page1,wx.ID_ANY,u'自动截取时长：',pos = (190,200))
        wx.StaticText(panel2Page1,wx.ID_ANY,u'手动截取时长：',pos = (190,220))
        self.autoShotTimeTxt = wx.TextCtrl(panel2Page1,wx.ID_ANY,'',(280,200),(100,20))
        self.manShotTimeTxt = wx.TextCtrl(panel2Page1,wx.ID_ANY,'',(280,220),(100,20))
        self.autoShotTimeTxt.SetEditable(False)
        self.manShotTimeTxt.SetEditable(False)
        wx.StaticText(panel2Page1,wx.ID_ANY,u'秒',pos = (390,200))
        wx.StaticText(panel2Page1,wx.ID_ANY,u'秒',pos = (390,220))
        manShotBut = wx.Button(panel2Page1,wx.ID_ANY,u'添加截图',(420,215),wx.Size(65,25))
        self.screenshotPath = wx.TextCtrl(panel2Page1,wx.ID_ANY,'D:\\screenshot',(110,248),(300,20))
        self.screenshotPath.SetEditable(False)
        selectPathBut = wx.Button(panel2Page1,wx.ID_ANY,u'截图路径',(420,245),wx.Size(65,25))
        self.radioAutoShotBut.Bind(wx.EVT_RADIOBUTTON,self.changeScreenShotTypeEVT)
        self.radioManShotBut.Bind(wx.EVT_RADIOBUTTON,self.changeScreenShotTypeEVT)
        manShotBut.Bind(wx.EVT_BUTTON,self.manScreenshotEVT)
        selectPathBut.Bind(wx.EVT_BUTTON,self.selectScreenshotPathEVT)
        
        
        radioClickBut.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioClickButEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioDragBut.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioDragButEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioPressBut.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioPressButEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioUpAndDown.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioUpAndDownEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioLeftAndRight.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioLeftAndRightEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        
        panel2Page2 = TabPage.TabPage(nb)
             
        panel2Page3 = TabPage.TabPage(nb)
#         panel2Page2.SetBackgroundColour("#ffffff")
        nb.AddPage(panel2Page1,u'连接')
        nb.AddPage(panel2Page2,u'控制')
        nb.AddPage(panel2Page3,u'输入')
                
        panel3 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,360))
#         panel3.SetBackgroundColour("#aa0000")       

        wx.StaticText(panel3,wx.ID_ANY,u'脚本区域：',pos = (10,2)) 
        self.scriptArea = wx.TextCtrl(panel3,wx.ID_ANY,size = wx.Size(508,317),pos = (10,22),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.HSCROLL)
        self.scriptArea.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
         
        page1BoxSizer.Add(self.panel1)
        page1BoxSizer.Add(page1BoxSizer2)
        page1BoxSizer2.Add(panel2)
        page1BoxSizer2.Add(panel3)
        
        #添加控制面板内容
        MyControlPanel.MyControlPanel(panel2Page2,self,self.delayTime,self.scriptArea,self.mokeyCode,self.dosCode)
    
        #添加第二个Tab页面
        Page2Layout(self,self.page2)
        
    def myExit(self,event):
        wx.Exit()     
        if self.connectThread != None:
            cmd = '..\\getProId'
            os.system(cmd)
            self.connectThread.stop()   
        
         #连接手机并开始屏幕的同步显示
    def startConnect(self,frame,buttonCon,img,width,height,bitmap,backgroundImage,panel1,panel2Txt1):
        #通过judge判断设置是否连接，如果连接着就会返回一个3个元素的数组，没有则返回2个元素的数组
        judge = os.popen(self.adbPath + 'adb devices').readlines()
        if len(judge) == 3:
            buttonCon.Enable(False)
            path = 'D:\\screenshot\\'
            if os.path.exists(path):
                print 'path is exit'
            else:
                print'creat the path'
                os.makedirs('D:\\screenshot\\')
            file = open('D:\\screenshot\\ctrl.txt','w')
            file.write('0')
            file.close()
            monkeyrunnerThread = StartMonkeyService.StartMonkeyService()
            monkeyrunnerThread.start()
            
            self.connectThread = ShowScreenService.ShowScreenService(img,height,width,bitmap,backgroundImage,panel1,panel2Txt1,self.screenRate,self.freshRate)
            
            while not os.path.exists('D:\\screenshot\\infoCtrl.txt'):
                pass           
            
            flag = 0
            while  flag != 1:
                file2 = open('D:\\screenshot\\infoCtrl.txt','r')
                if file2.read() == '1':
                    flag = 1
                file2.close()

            self.connectThread.start()
            
            file2 = open('D:\\screenshot\\infoCtrl.txt','w')
            file2.write('0')
            file2.close()            
            
        else:
            dialog = wx.MessageDialog(frame,'请连接你的android手机！'.decode('UTF-8'),'消息'.decode('UTF-8'),wx.OK_DEFAULT)
            dialog.ShowModal()
            
    #断开与手机的连接，并结束相关线程
    def endConnect(self,buttonCon,connectThread):
        buttonCon.Enable(True)
        cmd = '..\\getProId'
        os.system(cmd)
        self.connectThread.stop()
    
    #转换手机屏幕尺寸，以适应屏幕的显示
    def getPerfectWith(self,width,height):
        if 360 < width and width <= 480:
            return width*3/4
        elif 480 < width and width <= 720:
            return width*1/2
        elif 720 < width and width <= 1080:
            return width*1/3
        elif 1080 < width and width <= 1440:
            return width*1/4
        elif 1440 < width:
            return width*1440/width
        else:
            return width
    
    #转换手机屏幕尺寸，以适应屏幕的显示
    def getPerfectHeight(self,width,height):
        if 360 < width and width <= 480:
            return height*3/4
        elif 480 < width and width <= 720:
            return height*1/2
        elif 720 < width and width <= 1080:
            return height*1/3
        elif 1080 < width and width <= 1440:
            return height*1/4
        elif 1440 < width:
            return height*1440/width
        else:
            return height
            
    #设置屏幕操控的方式单机，长按，或者拖动
    def radioClickButEVT(self,radioClickBut,radioDragBut,radioPressBut,radioUpAndDown,radioLeftAndRight,longPressTxt):
        self.eventType = 0
        radioLeftAndRight.Enable(False)
        radioUpAndDown.Enable(False)
        self.longPressTxt.SetEditable(False)
    def radioPressButEVT(self,radioClickBut,radioDragBut,radioPressBut,radioUpAndDown,radioLeftAndRight,longPressTxt):  
            self.eventType = 4
            radioLeftAndRight.Enable(False)
            radioUpAndDown.Enable(False)
            self.longPressTxt.SetEditable(True)
    def radioDragButEVT(self,radioClickBut,radioDragBut,radioPressBut,radioUpAndDown,radioLeftAndRight,longPressTxt):
            radioLeftAndRight.Enable(True)
            radioUpAndDown.Enable(True)
            self.longPressTxt.SetEditable(False)  
            radioLeftAndRight.SetValue(True)
            self.eventType = 2                     
    def radioUpAndDownEVT(self,radioClickBut,radioDragBut,radioPressBut,radioUpAndDown,radioLeftAndRight,longPressTxt):
            self.eventType = 3
    def radioLeftAndRightEVT(self,radioClickBut,radioDragBut,radioPressBut,radioUpAndDown,radioLeftAndRight,longPressTxt):
            self.eventType = 2
            
    def recordButEVT(self,event):
        if event.GetId() == self.recordButOff.GetId():
            self.isRecord = 0
        elif event.GetId() == self.recordButOn.GetId():
            self.isRecord = 1
    
                
    def screenEVT(self,event):
        if event.ButtonDown():
            if self.eventType == 0:
                point = event.GetPosition()
                x = int(point[0]/self.screenRate.getScreenRate())
                y = int(point[1]/self.screenRate.getScreenRate())
                self.coodinate.SetValue('(' + str(x) + ',' + str(y) + ')')
                cmd = self.adbPath + "adb shell input tap " + str(x) + " " + str(y)
#                 os.system(cmd)
                CREATE_NO_WINDOW = 0x08000000
                subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                if self.isRecord == 0:
                    pass
                elif self.isRecord == 1:
                    if self.scriptType == 0:
                        scp1 = 'device.touch(' + str(x) + ',' + str(y) + ',"DOWN_AND_UP")'
                        scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                        shot = ''
                        self.getMonScreenshot(scp1, scp2, shot)
                    elif self.scriptType == 1:
                        scp1 = cmd
                        scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                        scp = scp1 + scp2
                        shot = ''
                        self.getDosScreenshot(scp, shot)
            elif self.eventType == 2 or self.eventType == 3:
                self.startPosition = event.GetPosition()
            elif self.eventType == 4:
                self.startPosition = event.GetPosition()
                x1 = int(self.startPosition[0]/self.screenRate.getScreenRate())
                y1 = int(self.startPosition[1]/self.screenRate.getScreenRate())
                self.coodinate.SetValue('(' + str(x1) + ',' + str(y1) + ')')
                cmd = self.adbPath + "adb shell input touchscreen swipe " + str(x1) + ' ' + str(y1) + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(int(self.longPressTxt.GetValue())*1000)
                CREATE_NO_WINDOW = 0x08000000
                subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                if self.isRecord == 0:
                        pass
                elif self.isRecord == 1:
                    if self.scriptType == 0:
                        scp1 = 'device.drag((' + str(x1) + ',' + str(y1) + '),(' + str(x1) + ',' + str(y1) + '),' + self.longPressTxt.GetValue() +',10)'

                        scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                        shot = ''
                        self.getMonScreenshot(scp1, scp2, shot)
                    elif self.scriptType == 1: 
                        scp1 = cmd
                        scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                        scp = scp1 + scp2
                        shot = ''
                        self.getDosScreenshot(scp, shot)
        elif event.ButtonUp():
            if self.eventType == 2 or self.eventType == 3:
                self.endPosition = event.GetPosition()
                if self.eventType == 2:
                    x1 = int(self.startPosition[0]/self.screenRate.getScreenRate())
                    x2 = int(self.endPosition[0]/self.screenRate.getScreenRate())
                    y1 = int(self.startPosition[1]/self.screenRate.getScreenRate())
                    y2 = int(self.endPosition[1]/self.screenRate.getScreenRate())
                    self.coodinate.SetValue('(' + str(x1) + ',' + str(y1) + ')' + ' ' + '(' + str(x2) + ',' + str(y2) + ')')
                    cmd = self.adbPath + 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y1)
#                     os.system(cmd)   
                    CREATE_NO_WINDOW = 0x08000000
                    subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                    if self.isRecord == 0:
                        pass
                    elif self.isRecord == 1:
                        if self.scriptType == 0:
                            scp1 = 'device.drag((' + str(x1) + ',' + str(y1) + '),(' + str(x2) + ',' + str(y2) + '),1.0,10)'
                            scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                            shot = ''
                            self.getMonScreenshot(scp1, scp2, shot)
                        elif self.scriptType == 1: 
                            scp1 = cmd
                            scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                            scp = scp1 + scp2
                            shot = ''
                            self.getDosScreenshot(scp, shot)
                elif self.eventType == 3:
                    x1 = int(self.startPosition[0]/self.screenRate.getScreenRate())
                    x2 = int(self.endPosition[0]/self.screenRate.getScreenRate())
                    y1 = int(self.startPosition[1]/self.screenRate.getScreenRate())
                    y2 = int(self.endPosition[1]/self.screenRate.getScreenRate())
                    cmd = self.adbPath + 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x1) + ' ' + str(y2)
#                     os.system(cmd)
                    CREATE_NO_WINDOW = 0x08000000
                    subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                    if self.isRecord == 0:
                        pass
                    elif self.isRecord == 1:
                        if self.scriptType == 0:
                            scp1 = 'device.drag((' + str(x1) + ',' + str(y1) + '),(' + str(x2) + ',' + str(y2) + '),1.0,10)'
                            scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                            shot = ''
                            self.getMonScreenshot(scp1, scp2, shot)
                        elif self.scriptType == 1: 
                            scp1 = cmd
                            scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                            scp = scp1 + scp2
                            shot = ''
                            self.getDosScreenshot(scp, shot)

    def inputTextEVT(self,event):
        cmd = self.adbPath + "adb shell input text " + self.inputText.GetValue()
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)        
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            if self.scriptType == 0:
                scp1 = 'device.type("' + self.inputText.GetValue() + '")'
                scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                shot = ''
                self.getMonScreenshot(scp1, scp2, shot)
            elif self.scriptType == 1: 
                scp1 = cmd
                scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp = scp1 + scp2
                shot = ''
                self.getDosScreenshot(scp, shot)
            
    def delTextEVT(self,event):
        cmd = self.adbPath + "adb shell input keyevent 67"
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            if self.scriptType == 0:
                scp1 = 'device.press("KEYCODE_DEL","DOWN_AND_UP")'
                scp2 = '\nMonkeyRunner.sleep(0.5)'
                shot = ''
                self.getMonScreenshot(scp1, scp2, shot)
            elif self.scriptType == 1: 
                scp1 = cmd
#                 scp2 = '\nchoice /t ' + self.delayTime.GetValue() + ' /d y /n >nul\n'
                scp2 = '\n'
                scp = scp1 + scp2
                shot = ''
                self.getDosScreenshot(scp, shot)
        
    def changeCodeTypeEVT(self,event):
        if event.GetId() == self.monkeyBut.GetId():
            self.scriptType = 0
            self.scriptArea.SetValue(self.getCodeFromList(self.mokeyCode))
            self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
        elif event.GetId() == self.dosBut.GetId():
            self.scriptType = 1
            self.scriptArea.SetValue(self.getCodeFromList(self.dosCode))
            self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
            
    def changeScreenShotTypeEVT(self,event):
        if event.GetId() == self.radioAutoShotBut.GetId():
            self.screenShotType = 0
        elif event.GetId() == self.radioManShotBut.GetId():
            self.screenShotType = 1
    #关闭窗口执行的事件
    def closeWinEVT(self,event):
        wx.Exit()
        if self.connectThread != None:
            cmd = '..\\getProId'
            os.system(cmd)
            self.connectThread.stop()
        
    def getCodeFromList(self,codeList):
        if self.scriptType == 0:
            length = self.monkeyCodeIndex
        elif self.scriptType == 1:
            length = self.dosCodeIndex     
        code = ''
        for i in range(0,length):
            code = code + codeList[i]
        return code
    def getExportCodeFromList(self,codeList,type):
        if type == 0:
            length = self.monkeyCodeIndex
        elif type == 1:
            length = self.dosCodeIndex     
        code = ''
        for i in range(0,length):
            code = code + codeList[i]
        return code
    
    def manScreenshotEVT(self,event): 
        if self.scriptType == 0:
            if self.monkeyCodeIndex != 0:
                code = self.mokeyCode[self.monkeyCodeIndex - 1]
                code = code[0:len(code) - 2]
                shot1 = '\nresult = device.takeSnapshot()'
                shot2 = '\nresult.writeToFile("' + str(self.picPath).replace('\\', '\\\\') + '\\\\'  + str(self.screenIndex) + '.png","png")'
                shot = shot1 + shot2 
                code = code + shot + '\n\n'
                self.mokeyCode[self.monkeyCodeIndex - 1] = code
                self.scriptArea.SetValue(self.getCodeFromList(self.mokeyCode))
                self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
                self.screenIndex += 1
        elif self.scriptType == 1:
            if self.dosCodeIndex != 0:
                code = self.dosCode[self.dosCodeIndex - 1]
                code = code[0:len(code) - 1]
                shot1 = "adb shell /system/bin/screencap -p /sdcard/screenshot.png\n"                
                shot2 = 'adb pull /sdcard/screenshot.png ' + self.picPath  + '\\' + str(self.dosScreenIndex) + '.png' + '\n\n'
                shot = shot1 + shot2 
                code = code + shot
                self.dosCode[self.dosCodeIndex - 1] = code
                self.scriptArea.SetValue(self.getCodeFromList(self.dosCode))
                self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
                self.dosScreenIndex += 1
                
    def selectScreenshotPathEVT(self,event):
        dlg = wx.DirDialog(self.frame, "Choose a directory:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.screenshotPath.SetValue(path)
            self.picPath = path
        dlg.Destroy()
        
    def exportMonkeyScriptEVT(self,event):
        self.exportMonkeyCode = self.txt + self.getExportCodeFromList(self.mokeyCode,0)
        dlg = wx.FileDialog(self.frame,"",os.getcwd(), "", "XYZ files (*.py)|*.py", style=wx.SAVE)
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            file = open(path,'w')
            file.write(self.exportMonkeyCode)
            file.close()
        dlg.Destroy()
        
    def exportDosScriptEVT(self,event):
        self.exportDosCode = self.dosTxt + self.getExportCodeFromList(self.dosCode,1) + '\npause'
        dlg = wx.FileDialog(self.frame,"",os.getcwd(), "", "XYZ files (*.bat)|*.bat", style=wx.SAVE)
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            file = open(path,'w')
            file.write(self.exportDosCode)
            file.close()
        dlg.Destroy()
        
    def getMonScreenshot(self,scp1,scp2,shot):
        if self.screenShotType == 0:
            shot1 = '\nresult = device.takeSnapshot()'
            shot2 = '\nresult.writeToFile("' + str(self.picPath).replace('\\', '\\\\') + '\\\\' + str(self.screenIndex) + '.png","png")'
            shot = shot1 + shot2
            self.screenIndex += 1
        elif self.screenShotType == 1:
            shot = ''
        elif self.screenShotType == 2:
            shot = ''
        scp = scp1 + scp2 + shot + '\n\n'
        self.mokeyCode.append(scp)
        self.monkeyCodeIndex += 1
        self.scriptArea.SetValue(self.getCodeFromList(self.mokeyCode))
        self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
        
    def getDosScreenshot(self,scp,shot):
        if self.screenShotType == 0:
            shot1 = "adb shell /system/bin/screencap -p /sdcard/screenshot.png\n"                
            shot2 = 'adb pull /sdcard/screenshot.png ' + self.picPath + '\\'  + str(self.dosScreenIndex) + '.png' + '\n'
            shot = shot1 + shot2
            self.dosScreenIndex += 1
        elif self.screenShotType == 1:
            shot = ''
        elif self.screenShotType == 2:
            shot = ''
        scp = scp + shot + '\n'
        self.dosCode.append(scp)
        self.dosCodeIndex += 1
        self.scriptArea.SetValue(self.getCodeFromList(self.dosCode))
        self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
    
    def clearMonCodeEVT(self,event):
        del self.mokeyCode[:]
        self.monkeyCodeIndex = 0
        self.screenIndex = 0
        if self.scriptType == 0:
            self.scriptArea.SetValue('')
        elif self.scriptType == 1:
            pass   
        print len(self.mokeyCode)    
    def clearDosCodeEVT(self,event):
        del self.dosCode[:]
        self.dosCodeIndex = 0
        self.dosScreenIndex = 0
        if self.scriptType == 0:
            pass
        elif self.scriptType == 1:
            self.scriptArea.SetValue('')       
    def reRecordEVT(self,event):
        del self.mokeyCode[:]
        self.monkeyCodeIndex = 0
        del self.dosCode[:]
        self.dosCodeIndex = 0
        self.screenIndex = 0
        self.dosScreenIndex = 0
        if self.scriptType == 0:
            self.scriptArea.SetValue('')
        elif self.scriptType == 1:
            self.scriptArea.SetValue('')
            
    def showVersionEVT(self,event):
        dialog = wx.MessageDialog(self.frame,u"Androd自动化脚本录制工具\n版本：V1.0.0\n.......\n炫一下测试部",'',wx.YES_DEFAULT)
        dialog.ShowModal()
        
    def cancleRerecordEVT(self,event):
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            if self.scriptType == 0:
                self.monkeyCodeIndex -= 1
                self.scriptArea.SetValue(self.getCodeFromList(self.mokeyCode))
                self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
            elif self.scriptType == 1:
                self.dosCodeIndex -= 1
                self.scriptArea.SetValue(self.getCodeFromList(self.dosCode))
            self.scriptArea.ShowPosition(self.scriptArea.GetLastPosition())
            
    def playMonScriptEVT(self,event):
        wildcard = "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self.frame, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            thePath = dlg.GetPath()
            cmd = self.monParh + 'monkeyrunner  ' + thePath
            try:           
                #通过Python线程池的原理，启动一个线程去执行
                thread.start_new_thread(os.system, (cmd,))     
#                 os.system(cmd)
            except Exception,ex:  
                print Exception,":",ex 
                    
        dlg.Destroy()
        
        
    def getIsRecord(self):
        return self.isRecord
    def getMonkeyCodeInxex(self):
        return self.monkeyCodeIndex
    def getDosCodeIndex(self):
        return self.dosCodeIndex
    def getScriptType(self):
        return self.scriptType
    def getScreentShotType(self):
        return self.screenShotType
    def addMonkeyCodeIndex(self):
        self.monkeyCodeIndex += 1
    def addDosCodeIndex(self):
        self.dosCodeIndex += 1
        
MyClass("").show();