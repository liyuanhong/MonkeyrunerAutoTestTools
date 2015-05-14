'''
Created on 2015-5-14

@author: xm
'''
import wx


class MyClass(object):

    def __init__(self, params):
        pass
    
    def show(self):
        self.win = wx.App()
        self.frame = wx.Frame(None, -1, 'simple.py')
        self.frame.Show()
        self.win.MainLoop()
        
MyClass("").show();