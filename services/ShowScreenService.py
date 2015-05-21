#coding:utf-8

import threading
import wx
import time

class ShowScreenService(threading.Thread):
        def __init__(self,img,height,width,bitmap,backgroundImage,imageShower,panel2Txt1,freshRate):
            threading.Thread.__init__(self)
            self.img = img
            self.height = height
            self.width = width
            self.bitmap = bitmap
            self.backgroundImage = backgroundImage
            self.freshRate = freshRate
            self.imageShower = imageShower
            self.size = wx.Size(self.width/2,self.height/2)
            self.imageShower.SetSize(self.size)
            self.imageShower.Refresh()
            self.panel2Txt1 = panel2Txt1
            #0表示结束线程，1表示循环运行线程
            self.clo = 0
            print 'init myThread'
            
            
        def run(self):
            self.clo = 1
            file = open('D:\\screenshot\\info.txt','r')
            name = file.readline()
            width = file.readline()
            height = file.readline()
#             info = name + '\n' + "width:" + width + '\n' + "height:" + height
            info = name + "width:" + width + "height:" + height
            self.panel2Txt1.SetValue(info)
            while self.clo == 1:
                self.file = self.file = open('D:\\screenshot\\ctrl.txt','r')
                try:
                    self.ctrl = int(self.file.read())
                    self.file.close()
                except:
                    print 'ctrl file is empty'          
                if (self.ctrl == 1):
                    self.img = wx.Image('D:\screenshot\monkeyPic.png'.decode('utf-8'),wx.BITMAP_TYPE_PNG,-1)
                    self.height = self.img.GetHeight()
                    self.width = self.img.GetWidth()
                    self.img.Rescale(self.width/2,self.height/2)
                    self.bitmap = self.img.ConvertToBitmap()
                    self.backgroundImage.SetBitmap(self.bitmap)
                    self.imageShower.Refresh()
                    self.backgroundImage.Refresh()
                    #print 'do event '
                elif (self.ctrl == 0):
                    pass
                time.sleep(self.freshRate)
                #print str(self.freshRate)

        def stop(self):
                self.clo = 0