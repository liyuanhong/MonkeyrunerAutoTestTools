#coding:utf-8

import threading
import wx
import time
import os

class ShowScreenService(threading.Thread):
        def __init__(self,img,height,width,bitmap,backgroundImage,imageShower,panel2Txt1,screenRate,freshRate):
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
            self.screenRate = screenRate
            #0表示结束线程，1表示循环运行线程
            self.clo = 0
            print 'init myThread'
            
            
        def run(self):
            self.clo = 1
           
            file = open('D:\\screenshot\\info.txt','r')
            name = file.readline()
            width = file.readline()
            height = file.readline()
            file.close()
#             info = name + '\n' + "width:" + width + '\n' + "height:" + height
            info = name + "width:" + width + "height:" + height
            self.panel2Txt1.SetValue(info)
            while self.clo == 1:
                self.file = open('D:\\screenshot\\ctrl.txt','r')
                try:
                    self.ctrl = int(self.file.read())
                    self.file.close()
                except:
                    print 'ctrl file is empty'          
                if (self.ctrl == 1):
                    self.img = wx.Image('D:\screenshot\monkeyPic.png'.decode('utf-8'),wx.BITMAP_TYPE_PNG,-1)
                    self.height = self.img.GetHeight()
                    self.width = self.img.GetWidth()
                    self.img.Rescale(self.getPerfectWith(self.width, self.height),self.getPerfectHeight(self.width, self.height))
                    self.bitmap = self.img.ConvertToBitmap()
                    self.backgroundImage.SetBitmap(self.bitmap)
                    self.imageShower.Refresh()
                    self.backgroundImage.Refresh()
                    #print 'do event '
                elif (self.ctrl == 0):
                    pass
                time.sleep(self.freshRate)
                #print str(self.freshRate)

        #转换手机屏幕尺寸，以适应屏幕的显示
        def getPerfectWith(self,width,height):
            if 360 < width and width <= 480:
                self.screenRate.setScreenRate(3.0/4.0)
                return width*3/4
            elif 480 < width and width <= 720:
                self.screenRate.setScreenRate(1.0/2.0)
                return width*1/2
            elif 720 < width and width <= 1080:
                self.screenRate.setScreenRate(1.0/3.0)
                return width*1/3
            elif 1080 < width and width <= 1440:
                self.screenRate.setScreenRate(1.0/4.0)
                return width*1/4
            elif 1440 < width:
                self.screenRate.setScreenRate(1440.0/width)
                return width*1440/width
            else:
                self.screenRate.setScreenRate(1.0)
                return width
    
        #转换手机屏幕尺寸，以适应屏幕的显示
        def getPerfectHeight(self,width,height):
            if 360 < width and width <= 480:
                self.screenRate.setScreenRate(3.0/4.0)
                return height*3/4
            elif 480 < width and width <= 720:
                self.screenRate.setScreenRate(1.0/2.0)
                return height*1/2
            elif 720 < width and width <= 1080:
                self.screenRate.setScreenRate(1.0/3.0)
                return height*1/3
            elif 1080 < width and width <= 1440:
                self.screenRate.setScreenRate(1.0/4.0)
                return height*1/4
            elif 1440 < width:
                self.screenRate.setScreenRate(1440.0/width)
                return height*1440/width
            else:
                self.screenRate.setScreenRate(1.0)
                return height

        def stop(self):
                self.clo = 0