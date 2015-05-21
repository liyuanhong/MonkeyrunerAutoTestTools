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

class MyClass(object):

    def __init__(self, params):
        #定义窗体尺寸
        self.winSize = wx.Size(900,730)
        #刷新率默认为0.05秒每次
        self.freshRate = 0.05
        #动态显示手机屏幕的线程
        self.connectThread = None
    
    #显示主窗体
    def show(self):
        win = wx.App()
        frame = wx.Frame(None, -1, 'simple.py',size = self.winSize) 
        nb = wx.Notebook(frame,wx.NewId())    
        menuBar = wx.MenuBar()
        
        #添加tab标签页
        page1 = TabPage.TabPage(nb)
#         page2 = TabPage.TabPage(nb)
        nb.AddPage(page1,u'录制脚本')
        self.addPage1Layout(frame, page1);
        
#         nb.AddPage(page2,'page2')                   
        self.addMenu(menuBar,frame);
        
        frame.SetMenuBar(menuBar);
        frame.Show()
        win.MainLoop()
      
    #添加菜单项  
    def addMenu(self,menuBar,frame):
        menuFile = wx.Menu()
        menuOpenItem = wx.MenuItem(menuFile,wx.NewId(),text = u"打开")
        menuFile.Append(menuOpenItem.GetId(),u"打开")
        
        menuExitItem = wx.MenuItem(menuFile,wx.NewId(),text = u"退出")        
        menuFile.Append(menuExitItem.GetId(),u"退出")
        frame.Bind(wx.EVT_MENU, self.myExit)
        
        menuBar.Append(menuFile,u"文件")
    
    #录制脚本页面页面布局
    def addPage1Layout(self,frame,page1):
        page1BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        page1.SetSizer(page1BoxSizer)
        panel1 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(360,640))
#         panel1.SetBackgroundColour("#aaaa00")
        
        img = wx.Image('..\\pic\\阳光小秒拍.png'.decode('utf-8'),wx.BITMAP_TYPE_PNG,-1)
        height = img.GetHeight()
        width = img.GetWidth()
        img.Rescale(width/2,height/2)
        bitmap = img.ConvertToBitmap()               
        panel1.SetAutoLayout(True)
        backgroundImage = wx.StaticBitmap(panel1,wx.ID_ANY,bitmap)
        
        page1BoxSizer2 = wx.BoxSizer(wx.VERTICAL)        
        panel2 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,300))
#         panel2.SetBackgroundColour("#00aaaa")       
        nb = wx.Notebook(panel2,wx.ID_ANY,(10,0),size = wx.Size(508,300))
        
        #连接面板添加布局
        panel2Page1 = TabPage.TabPage(nb)
#         panel2Page1.SetBackgroundColour("#ff0000")
        buttonCon = wx.Button(panel2Page1,wx.ID_ANY,u'连接手机',(5,5),wx.Size(70,25))
        frame.Bind(wx.EVT_BUTTON,lambda evt, mark=0 : self.startConnect(frame, buttonCon, img, width, height, bitmap, backgroundImage, panel1),buttonCon)
        buttonDisCon = wx.Button(panel2Page1,wx.ID_ANY,u'中断连接',(80,5),wx.Size(70,25))
        frame.Bind(wx.EVT_BUTTON,lambda evt, mark=0 : self.endConnect(buttonCon, self.connectThread),buttonDisCon)
        panel2panel0 = wx.Panel(panel2Page1,wx.ID_ANY,(5,35),wx.Size(145,80),wx.BORDER_SIMPLE | wx.TE_MULTILINE )
#         panel2panel0.SetBackgroundColour("#ff0000")
        panel2Txt1 = wx.TextCtrl(panel2panel0,wx.ID_ANY,u"phone:sanxing\nwidth:720\nheight:1280",(0,0),wx.Size(145,80),wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        panel2Txt1.SetEditable(False)




        panel2Page2 = TabPage.TabPage(nb)
#         panel2Page2.SetBackgroundColour("#ffffff")
        nb.AddPage(panel2Page1,u'连接')
        nb.AddPage(panel2Page2,u'控制')
        
        
        
        panel3 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,360))
#         panel3.SetBackgroundColour("#aa0000")       

        wx.StaticText(panel3,wx.ID_ANY,u'脚本区域：',pos = (10,2)) 
        scriptArea = wx.TextCtrl(panel3,wx.ID_ANY,size = wx.Size(508,317),pos = (10,22),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE | wx.HSCROLL)
        scriptArea.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
         
        page1BoxSizer.Add(panel1)
        page1BoxSizer.Add(page1BoxSizer2)
        page1BoxSizer2.Add(panel2)
        page1BoxSizer2.Add(panel3)
        
        
    
    def myExit(self,event):
        wx.Exit()
        
        
         #连接手机并开始屏幕的同步显示
    def startConnect(self,frame,buttonCon,img,width,height,bitmap,backgroundImage,panel1):
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
            
            self.connectThread = ShowScreenService.ShowScreenService(img,height,width,bitmap,backgroundImage,panel1,self.freshRate)
            self.connectThread.start()
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
            return width*1/3
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
            return height*1/3
        elif 1440 < width:
            return height*1440/width
        else:
            return height
    
MyClass("").show();