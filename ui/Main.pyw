#coding:utf-8
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
sys.path.append(curPath + '\\..')
sys.path.append(curPath + '\\..\\widget')
sys.path.append(curPath + '\\..\\services')
sys.path.append(curPath + '\\..\\util')
import wx
from widget import  TabPage
from services import StartMonkeyService,ShowScreenService
from wx import Size
from bean import ScreenRate
import subprocess

class MyClass(object):

    def __init__(self, params):
        #定义窗体尺寸
        self.winSize = wx.Size(900,730)
        #刷新率默认为0.05秒每次
        self.freshRate = 0.05
        #动态显示手机屏幕的线程
        self.connectThread = None
        #定义屏幕操作的类型，0表示点击，1表示滑动，2表示左右滑动，3表示上下滑动，4表示长按
        self.eventType = 0
        #定义显示与真实屏幕的比例
        self.screenRate = ScreenRate.ScreenRate()
        #定义拖动的起始点
        self.startPosition = (0,0)
        #定义拖动的结束点
        self.endPosition = (0,0)
        #截图的方式0表示自动，1表示手动,2表示不截图
        self.screenShotType = 0
        self.screenIndex = 0
        #是否录制脚本0，表示 不录制，1表示录制
        self.isRecord = 0
        #将要录制的代码部分
        self.code = []
        self.exportCode = []
        #当前代码的录制索引
        self.codeindex = 0
        #定义脚本的前部分代码
        self.txt = '''import sys
import time
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
device = MonkeyRunner.waitForConnection()'''
        self.exportCode.append(self.txt)
        print self.exportCode
    
    #显示主窗体
    def show(self):
        win = wx.App()
        frame = wx.Frame(None, -1, 'simple.py',size = self.winSize) 
        nb = wx.Notebook(frame,wx.NewId())    
        menuBar = wx.MenuBar()
        
        #添加tab标签页
        page1 = TabPage.TabPage(nb)
        page2 = TabPage.TabPage(nb)
        nb.AddPage(page1,u'录制脚本')
        self.addPage1Layout(frame, page1);
        
        nb.AddPage(page2,u'脚本回放')                   
        self.addMenu(menuBar,frame);
        
        frame.SetMenuBar(menuBar);
        frame.Bind(wx.EVT_CLOSE,self.closeWinEVT)
        frame.Show()
        win.MainLoop()
      
    #添加菜单项  
    def addMenu(self,menuBar,frame):
        menuFile = wx.Menu()
        menuOpenItem = wx.MenuItem(menuFile,wx.NewId(),text = u"打开脚本")
        menuSaveAsItem = wx.MenuItem(menuFile,wx.ID_ANY,text = u"导出脚本")
        menuSaveItem = wx.MenuItem(menuFile,wx.ID_ANY,text = u"保存")
        menuFile.Append(menuOpenItem.GetId(),u"打开脚本")
        menuFile.Append(menuSaveAsItem.GetId(),u"导出脚本")
        menuFile.Append(menuSaveItem.GetId(),u"保存")
        
        menuExitItem = wx.MenuItem(menuFile,wx.NewId(),text = u"退出")        
        menuFile.Append(menuExitItem.GetId(),u"退出")
        frame.Bind(wx.EVT_MENU, self.myExit)
        
        menuBar.Append(menuFile,u"文件")
    
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
#         backgroundImage.Bind(wx.EVT_LEFT_DOWN,self.getMousePos)
#         backgroundImage.Bind(wx.EVT_LEFT_DOWN,self.sendClickEVT)
#         backgroundImage.Bind(wx.EVT_LEFT_DOWN,self.dragDownEVT)
#         backgroundImage.Bind(wx.EVT_LEFT_UP,self.dragUpEVT)
        backgroundImage.Bind(wx.EVT_MOUSE_EVENTS,self.screenEVT)
        
        
        panel2panel0 = wx.Panel(panel2Page1,wx.ID_ANY,(5,35),wx.Size(145,80),wx.BORDER_SIMPLE | wx.TE_MULTILINE )
#         panel2panel0.SetBackgroundColour("#ff0000")
        panel2Txt1 = wx.TextCtrl(panel2panel0,wx.ID_ANY,u"phone:sanxing\nwidth:720\nheight:1280",(0,0),wx.Size(145,80),wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        panel2Txt1.SetEditable(False)      
        radioClickBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'点击',(190,10),style = wx.RB_GROUP)
        radioDragBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'拖曳',(190,30))       
        radioPressBut = wx.RadioButton(panel2Page1,wx.ID_ANY,u'长按',(190,80))
        
        radioLeftAndRight = wx.RadioButton(panel2Page1,wx.ID_ANY,u'左右',(250,50),style = wx.RB_GROUP)
        radioUpAndDown = wx.RadioButton(panel2Page1,wx.ID_ANY,u'上下',(320,50))
        
        wx.StaticText(panel2Page1,wx.ID_ANY,u'长按时长：',pos = (190,100))
        self.longPressTxt = wx.TextCtrl(panel2Page1,wx.ID_ANY,'5000',size = (100,20),pos = (250,100))
        wx.StaticText(panel2Page1,wx.ID_ANY,u'毫秒',pos = (355,100))
        
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
        
        radioClickBut.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioClickButEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioDragBut.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioDragButEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioPressBut.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioPressButEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioUpAndDown.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioUpAndDownEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        radioLeftAndRight.Bind(wx.EVT_RADIOBUTTON,lambda evt, mark=0 : self.radioLeftAndRightEVT(radioClickBut, radioDragBut, radioPressBut, radioUpAndDown, radioLeftAndRight, self.longPressTxt))
        


        panel2Page2 = TabPage.TabPage(nb)
        buttonHome = wx.Button(panel2Page2,wx.ID_ANY,u'Home键',(5,5),wx.Size(70,25))
        buttonBack = wx.Button(panel2Page2,wx.ID_ANY,u'返回键',(5,35),wx.Size(70,25))
        buttonMenu = wx.Button(panel2Page2,wx.ID_ANY,u'菜单键',(5,65),wx.Size(70,25))
        buttonVoiceUp = wx.Button(panel2Page2,wx.ID_ANY,u'音量+',(5,95),wx.Size(70,25))
        buttonVoiceDown = wx.Button(panel2Page2,wx.ID_ANY,u'音量-',(5,125),wx.Size(70,25))
        buttonLongPressHome = wx.Button(panel2Page2,wx.ID_ANY,u'长按Home键',(5,155),wx.Size(100,25))
        buttonHome.Bind(wx.EVT_BUTTON,self.sendHomeEVT)
        buttonBack.Bind(wx.EVT_BUTTON,self.sendBackEVT)
        buttonMenu.Bind(wx.EVT_BUTTON,self.sendMenuEVT)
        buttonVoiceUp.Bind(wx.EVT_BUTTON,self.sendVoiceUpEVT)
        buttonVoiceDown.Bind(wx.EVT_BUTTON,self.sendVoiceDownEVT)
        buttonLongPressHome.Bind(wx.EVT_BUTTON,self.sendLongPressHomeEVT)
        
        panel2Page3 = TabPage.TabPage(nb)
#         panel2Page2.SetBackgroundColour("#ffffff")
        nb.AddPage(panel2Page1,u'连接')
        nb.AddPage(panel2Page2,u'控制')
        nb.AddPage(panel2Page3,u'输入')
        
        
        
        panel3 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,360))
#         panel3.SetBackgroundColour("#aa0000")       

        wx.StaticText(panel3,wx.ID_ANY,u'脚本区域：',pos = (10,2)) 
        scriptArea = wx.TextCtrl(panel3,wx.ID_ANY,size = wx.Size(508,317),pos = (10,22),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.HSCROLL)
        scriptArea.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
         
        page1BoxSizer.Add(self.panel1)
        page1BoxSizer.Add(page1BoxSizer2)
        page1BoxSizer2.Add(panel2)
        page1BoxSizer2.Add(panel3)
        
        
    
    def myExit(self,event):
        wx.Exit()
        
        
         #连接手机并开始屏幕的同步显示
    def startConnect(self,frame,buttonCon,img,width,height,bitmap,backgroundImage,panel1,panel2Txt1):
        #通过judge判断设置是否连接，如果连接着就会返回一个3个元素的数组，没有则返回2个元素的数组
        judge = os.popen('adb devices').readlines()
        if len(judge) == 3:
            buttonCon.Enable(False)
            path = 'D:\\screenshot\\'
            filename = 'monkeyPic'
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
            
            print self.width
            print self.height
            
#             width = self.getPerfectWith(self.width, self.height)
#             height = self.getPerfectHeight(self.width, self.height)
#             print width
#             print height
#             self.panel1.SetSize(wx.Size(360,640))
#             print self.panel1.GetBestSize()
#             self.panel1.Refresh()
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
        
    #获取鼠标点击的坐标
#     def getMousePos(self,event):
#         point = event.GetPosition()
# #         print point
#         x = point[0]/self.screenRate.getScreenRate()
#         y = point[1]/self.screenRate.getScreenRate()
#         cmd = "adb shell input tap " + str(x) + " " + str(y)
#         CREATE_NO_WINDOW = 0x08000000
#         subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
# #         os.system(cmd)
#         if self.isRecord == 0:
#             pass
#         elif self.isRecord == 1:
#             scp1 = 'device.touch(' + x + ',' + y + ',"DOWN_AND_UP")'
#             scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
#             scp = scp1 + scp2
#             print self.exportCode.append(scp)
            
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
    
#     #定义屏幕上推动的事件
#     def dragDownEVT(self,event):
#         if self.eventType == 2 or self.eventType == 3:
#             self.startPosition == event.GetPosition()
#     def dragUpEVT(self,event):
#         if self.eventType == 2 or self.eventType == 3:
#             self.endPosition = event.GetPosition()
#             if self.eventType == 2:
#                 x1 = self.startPosition[0]
#                 x2 = self.endPosition[0]
#                 cmd = 'adb shell input swipe ' + str(x1) + ' ' + str(x1) + ' ' + str(x2) + ' ' + str(x2)
#                 os.system(cmd)   
#             elif self.eventType == 3:
#                 y1 = self.startPosition[1]
#                 y2 = self.endPosition[1]
#                 cmd = 'adb shell input swipe ' + str(y1) + ' ' + str(y1) + ' ' + str(y2) + ' ' + str(y2)
#                 os.system(cmd)
                
    def screenEVT(self,event):
        if event.ButtonDown():
            if self.eventType == 0:
                point = event.GetPosition()
                x = point[0]/self.screenRate.getScreenRate()
                y = point[1]/self.screenRate.getScreenRate()
                cmd = "adb shell input tap " + str(x) + " " + str(y)
#                 os.system(cmd)
                CREATE_NO_WINDOW = 0x08000000
                subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                if self.isRecord == 0:
                    pass
                elif self.isRecord == 1:
                    scp1 = 'device.touch(' + str(x) + ',' + str(y) + ',"DOWN_AND_UP")'
                    scp2 = '\nMonkeyRunner.sleep(' + self.delayTime.GetValue() + ')'
                    shot = ''
                    if self.screenShotType == 0:
                        shot1 = 'result = device.takeSnapshot()'
                        shot2 = '\nresult.writeToFile(D:\\' + str(self.screenIndex) + '.png,png)'
                        shot = shot1 + shot2
                        self.screenIndex += 1
                    elif self.screenShotType == 1:
                        shot1 = 'result = device.takeSnapshot()'
                        shot2 = '\nresult.writeToFile(D:\\aaaaaaaaaa' + '.png,png)'
                        shot = shot1 + shot2
                    elif self.screenShotType == 2:
                        pass
                    scp = scp1 + scp2 + shot
                    self.code.append(scp)
                    self.codeindex += 1
                    print self.code
            elif self.eventType == 2 or self.eventType == 3:
                self.startPosition = event.GetPosition()
            elif self.eventType == 4:
                self.startPosition = event.GetPosition()
                x1 = self.startPosition[0]/self.screenRate.getScreenRate()
                y1 = self.startPosition[1]/self.screenRate.getScreenRate()
                cmd = "adb shell input touchscreen swipe " + str(x1) + ' ' + str(y1) + ' ' + str(x1) + ' ' + str(y1) + ' ' + self.longPressTxt.GetValue()
#                 cmd = 'adb shell input touchscreen swipe ' + 
#                 os.system(cmd)
                CREATE_NO_WINDOW = 0x08000000
                subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                if self.isRecord == 0:
                    pass
                elif self.isRecord == 1:
                    pass
        elif event.ButtonUp():
            if self.eventType == 2 or self.eventType == 3:
                self.endPosition = event.GetPosition()
                if self.eventType == 2:
                    x1 = self.startPosition[0]/self.screenRate.getScreenRate()
                    x2 = self.endPosition[0]/self.screenRate.getScreenRate()
                    y1 = self.startPosition[1]/self.screenRate.getScreenRate()
                    y2 = self.endPosition[1]/self.screenRate.getScreenRate()
                    cmd = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y1)
#                     os.system(cmd)   
                    CREATE_NO_WINDOW = 0x08000000
                    subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                    if self.isRecord == 0:
                        pass
                    elif self.isRecord == 1:
                        pass
                elif self.eventType == 3:
                    x1 = self.startPosition[0]/self.screenRate.getScreenRate()
                    x2 = self.endPosition[0]/self.screenRate.getScreenRate()
                    y1 = self.startPosition[1]/self.screenRate.getScreenRate()
                    y2 = self.endPosition[1]/self.screenRate.getScreenRate()
                    cmd = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x1) + ' ' + str(y2)
#                     os.system(cmd)
                    CREATE_NO_WINDOW = 0x08000000
                    subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
                    if self.isRecord == 0:
                        pass
                    elif self.isRecord == 1:
                        pass
                
            
            
#     #向手机发送点击事件
#     def sendClickEVT(self,event):
#         if self.eventType == 0:
#             point = event.GetPosition()
#             x = point[0]/self.screenRate.getScreenRate()
#             y = point[1]/self.screenRate.getScreenRate()
#             cmd = "adb shell input tap " + str(x) + " " + str(y)
#             os.system(cmd)       
    def sendHomeEVT(self,event):
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
    def inputTextEVT(self,event):
        cmd = "adb shell input text " + self.inputText.GetValue()
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    def delTextEVT(self,event):
        cmd = "adb shell input keyevent 67"
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(cmd, creationflags=CREATE_NO_WINDOW)
        if self.isRecord == 0:
            pass
        elif self.isRecord == 1:
            pass
    #关闭窗口执行的事件
    def closeWinEVT(self,event):
        wx.Exit()
        cmd = '..\\getProId'
        os.system(cmd)
        self.connectThread.stop()
        
MyClass("").show();