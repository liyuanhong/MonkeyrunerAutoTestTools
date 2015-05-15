#coding:utf-8
import wx
from widget import  TabPage

class MyClass(object):

    def __init__(self, params):
        #定义窗体尺寸
        self.winSize = wx.Size(900,670)
    
    #显示主窗体
    def show(self):
        win = wx.App()
        frame = wx.Frame(None, -1, 'simple.py',size = self.winSize) 
        nb = wx.Notebook(frame,wx.NewId())    
        menuBar = wx.MenuBar()
        
        #添加tab标签页
        page1 = TabPage.TabPage(nb)
        page2 = TabPage.TabPage(nb)
        nb.AddPage(page1,'page1')
        self.addPage1Layout(page1)
        
        nb.AddPage(page2,'page2')        
             
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
    
    
    def addPage1Layout(self,page1):
        page1BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        page1.SetSizer(page1BoxSizer)
        panel1 = wx.Panel(page1,wx.ID_ANY,style=wx.BORDER_DOUBLE,size = wx.Size(360,640))
        panel1.SetBackgroundColour("#aaaa00")
        
        page1BoxSizer2 = wx.BoxSizer(wx.VERTICAL)
        
        panel2 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,300))
        panel2.SetBackgroundColour("#00aaaa")
        panel3 = wx.Panel(page1,wx.ID_ANY,size = wx.Size(540,300))
#         panel3.SetBackgroundColour("#aa0000")
        
        scriptArea = wx.TextCtrl(panel3,wx.ID_ANY,size = wx.Size(508,280),pos = (10,2),style = wx.BORDER_SIMPLE | wx.TE_MULTILINE)
        scriptArea.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
         
        page1BoxSizer.Add(panel1)
        page1BoxSizer.Add(page1BoxSizer2)
        page1BoxSizer2.Add(panel2)
        page1BoxSizer2.Add(panel3)
        
        
    
    def myExit(self,event):
        wx.Exit()
        
MyClass("").show();