# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_V2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from audioop import cross
from email.mime import image
from multiprocessing import Event
from tkinter import Frame
import sys
#from tkinter import Frame
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import scipy.signal as sig
import scipy.ndimage as ndi
from PyQt5.QtGui import QImage
from PyQt5.uic import loadUi
import cv2
import numpy as np
import numpy as random
import matplotlib.pyplot as plt
import random

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        loadUi('new_V2.ui', self)
        
        self.crop_btn.clicked.connect(self.crop)
        self.L_rotate_btn.clicked.connect(self.L_rotation)
        self.R_rotate_btn.clicked.connect(self.R_rotation)
        self.hori_flip_btn.clicked.connect(self.hori_filp)
        self.verti_flip_btn.clicked.connect(self.verti_filp)
        self.zoom_in_btn.clicked.connect(self.zoomin_Img)
        self.zoom_out_btn.clicked.connect(self.zoomout_Img)
        self.gv_r.rubberBandChanged['QRect','QPointF','QPointF'].connect(self.gv_img.clear)
        self.gv_g.rubberBandChanged['QRect','QPointF','QPointF'].connect(self.gv_img.clear)
        self.gv_b.rubberBandChanged['QRect','QPointF','QPointF'].connect(self.gv_img.clear)
        self.gray_btn.clicked.connect(self.Gray_filter)
        self.invert_btn.clicked.connect(self.img_Negative)
        self.histoeq_btn.clicked.connect(self.histogram_Equalization)
        self.gaunoise_btn.clicked.connect(self.gaussian_noise)
        self.boxfil_btn.clicked.connect(self.box_filter)
        self.gaufil_btn.clicked.connect(self.gaussian_filter)
        self.median_btn.clicked.connect(self.median_filter)
        self.con_bar.valueChanged['int'].connect(self.gv_img.setNum)
        self.brigth_bar.valueChanged['int'].connect(self.brightness_value)
        self.hue_bar.valueChanged['int'].connect(self.hue_value)
        self.saturation_bar.valueChanged['int'].connect(self.sat_value)
        self.value_bar.valueChanged['int'].connect(self.val_value)
        self.R_bar.valueChanged['int'].connect(self.R_value)
        self.G_bar.valueChanged['int'].connect(self.G_value)
        self.B_bar.valueChanged['int'].connect(self.B_value)
        self.saltAndPep_btn.clicked.connect(self.saltAndPep)
        self.Sharpen_btn.clicked.connect(self.Sharpen)
        self.edgeDetection_btn.clicked.connect(self.edges)
        self.open_btn.clicked.connect(self.open_img)
        self.save_btn.clicked.connect(self.savePhoto)
        self.reset_btn.clicked.connect(self.reset)
        
        self.Add_btn.clicked.connect(self.add)
        self.Subtract_btn.clicked.connect(self.subtract)
        self.Blend_btn.clicked.connect(self.Blend)
        self.Weight_bar.valueChanged['int'].connect(self.Weight_value)
        
        #self.brightness_value_now = 0 # Updated brightness value
        self.new_img = None
##########################################################################################################################

    @pyqtSlot()
    def loadImage(self, fname):
        self.image = cv2.imread(fname)
        self.tmp = self.image
        
        self.setPhoto(self.image)
                      
    def open_img(self):
        fname = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        if fname:
            self.loadImage(fname)
        else:
            print("Invalid Image")  
##########################################################################################################################

    def crop(self):
        
        roi = cv2.selectROI(self.image)
        imcrop = self.image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        self.setPhoto(imcrop)
               
    def verti_filp(self):	
        self.image  = cv2.flip(self.image, 0)
        self.setPhoto(self.image)
    
    def hori_filp(self):	
        self.image  = cv2.flip(self.image, 1)
        self.setPhoto(self.image) 
        
    def L_rotation(self):
        rows, cols, steps = self.image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1) 
        self.image = cv2.warpAffine(self.image, M, (cols, rows))
        self.setPhoto(self.image)
        
    def R_rotation(self):
        rows, cols, steps = self.image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -90, 1) 
        image = cv2.warpAffine(self.image, M, (cols, rows))
        self.setPhoto(self.image)

###################################### FILTER ZONE ##################################
        
    def box_filter(self):
        self.image = cv2.boxFilter(self.image, -1,(20,20))
        self.setPhoto(self.image)
        
    def median_filter(self):
        self.image = cv2.medianBlur(self.image,5)
        self.setPhoto(self.image)
        
    def gaussian_filter(self):
        self.image = cv2.GaussianBlur(self.image,(5,5),0)
        self.setPhoto(self.image) 
        
    def img_Negative(self):
        self.image = ~self.image
        self.setPhoto(self.image)
    
    def Gray_filter(self):
        image = self.image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.setPhoto(gray)
    def saltAndPep(self,image,ps=0.05,pp=0.05):
        image = self.image
        row, col, ch = self.image.shape
        num_s= int(np.ceil(ps*row*col))
        num_p= int(np.ceil(pp*row*col))

        for i in range(num_s):
                y=random.randint(0,row-1)
                x=random.randint(0,col-1)
                self.image[y][x]=[255,255,255]
    
        for i in range(num_p):
                y=random.randint(0,row-1)
                x=random.randint(0,col-1)
                self.image[y][x]=[0,0,0]
        self.setPhoto(self.image)
    
    def Sharpen(self):
        
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        self.image  = cv2.filter2D(self.image, -1, kernel)
        self.setPhoto(self.image)

    def edges(self):
        gray_image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(gray_image, 120, 150)
        self.setPhoto(canny_edges)
                
############################ HSV #########################################     
         
    def brightness_value(self,value):
        self.brightness_value_now = value
        print('Brightness: ',value)
        self.update()

    def hue_value(self,value):
        self.hue_now = value
        print('Min_hue: ',value)
        self.update_h()
               
    def sat_value(self,value):
        self.sat_now = value
        print('Min_sat: ',value)
        self.update_s()                    
        
    def val_value(self,value):
        self.value_now = value
        print('Min_val: ',value)
        self.update_v() 
    
    def Weight_value(self,value):
        self.Weight_value_now = value
        print('Weight: ',value)
        self.update_Weight()
################################# RGB ###########################################        

    def R_value(self,value):
        self.R_now = value
        print('R_val: ',value)
        self.update_R()     
        
    def G_value(self,value):
        self.G_now = value
        print('R_val: ',value)
        self.update_G() 
          
    def B_value(self,value):
        self.B_now = value
        print('B_val: ',value)
        self.update_B()         
                    
############################## USE BAR SLIDE ZONE ##########################################  
            
    def changeBrightness(self,image,value):
        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        image = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return image
    
    def changeHue(self,image,value):
        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        h[h>lim] = 255
        h[h<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        image = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return image
    
    def changeSat(self,image,value):
        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        s[s>lim] = 255
        s[s<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        image = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return image
    
    def changeVal(self,image,value):
        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        image = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return image
    def change_R(self ,image ,value):
        rgb = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
        r,g,b= cv2.split(rgb)
        lim = 255 - value
        r[r>lim] = 255
        r[r<=lim] += value
        final_rgb = cv2.merge((r,g,b))
        image = cv2.cvtColor(final_rgb,cv2.COLOR_RGB2BGR)
        return image

    def change_G(self ,image ,value):
        rgb = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
        r,g,b= cv2.split(rgb)
        lim = 255 - value
        g[g>lim] = 255
        g[g<=lim] += value
        final_rgb = cv2.merge((r,g,b))
        image = cv2.cvtColor(final_rgb,cv2.COLOR_RGB2BGR)
        return image
    
    def change_B(self ,image ,value):
        rgb = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
        r,g,b= cv2.split(rgb)
        lim = 255 - value
        b[b>lim] = 255
        b[b<=lim] += value
        final_rgb = cv2.merge((r,g,b))
        image = cv2.cvtColor(final_rgb,cv2.COLOR_RGB2BGR)
        return image
    
    def changeWeight(self,image,value):
        wt1 = 0.5
        wt2 = value/40
        image = cv2.addWeighted(self.image, wt1, self.image2, wt2, 0)
        return image
       
        
######################################END USE BAR SLIDE ZONE ############################  
  
################################## test  zone ###########################################    

    def changer(self,image,value):
        rgb = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
        r,g,b= cv2.split(rgb)
        lim = 255 - value
        r[r>lim] = 255
        r[r<=lim] += value
        final_rgb = cv2.merge((r,g,b))
        image = cv2.cvtColor(final_rgb,cv2.COLOR_RGB2BGR)
        return image
    
################################## end test zone ########################################

######################################################################################### 
       
    def gaussian_noise(self):
        row, col, ch = self.image.shape
        mean = 0
        var = 0.1
        sigma = var * 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        self.image = self.image + gauss
        self.setPhoto(self.image)
    
    def histogram_Equalization(self):
        img_yuv = cv2.cvtColor(self.image, cv2.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        self.image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        self.setPhoto(self.image)
    
    def zoomin_Img(self):
        self.image = cv2.resize(self.image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        self.setPhoto(self.image)

    def zoomout_Img(self):
        self.image = cv2.resize(self.image, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_CUBIC)
        self.setPhoto(self.image)
##########################################################################################################################

    def setPhoto(self,image):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:
            if(self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888       
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #image = image.rgbSwapped() 
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],qformat)
        #image = image.rgbSwapped()
        self.gv_img.setPixmap(QtGui.QPixmap.fromImage(image))
        
        #self.gv_img.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

          
#################################################################################################

    def update(self):
        img = self.changeBrightness(self.image,self.brightness_value_now)
        self.setPhoto(img) 

    def update_h(self):
        img = self.changeHue(self.image ,self.hue_now)       
        self.setPhoto(img) 

    def update_s(self):
        img = self.changeSat(self.image ,self.sat_now)       
        self.setPhoto(img) 

    def update_v(self):
        img = self.changeVal(self.image ,self.value_now)       
        self.setPhoto(img)
        
#####################################################################################    
    
    def update_R(self):
        img = self.changer(self.image ,self.R_now)       
        self.setPhoto(img)  
            
    def update_G(self):
        img = self.change_G(self.image ,self.G_now)       
        self.setPhoto(img) 
            
    def update_B(self):
        img = self.change_B(self.image ,self.B_now)       
        self.setPhoto(img)         
    
    def update_Weight(self):
        img = self.changeWeight(self.image,self.Weight_value_now)
        self.setPhoto(img) 

#####################################################################################

    def reset(self):
        image = self.tmp
        self.setPhoto(image)
         
    def savePhoto(self):
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename,image)
        print('Image saved as:',self.filename)

##########################################################################################################################

    def add(self):
        
        gname = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        image2 = cv2.imread(gname) 
        
       
        self.image= cv2.resize(self.image,(400,400))
        image2 = cv2.resize(image2,(400,400))

      
        ADD = cv2.add(self.image,image2)
        
        self.setPhoto(ADD)
    
    def subtract(self):
        
        gname = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        image2 = cv2.imread(gname) 
        
       
        self.image= cv2.resize(self.image,(400,400))
        image2 = cv2.resize(image2,(400,400))

      
        ADD = cv2.subtract(self.image,image2)
        
        self.setPhoto(ADD)
    
    def Blend(self):
        gname = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image2 = cv2.imread(gname) 
        
        self.image= cv2.resize(self.image,(400,400))
        self.image2 = cv2.resize(self.image2,(400,400))

        weighted = cv2.addWeighted(self.image, 0.5, self.image2, 0.4, 0)
        self.setPhoto(weighted)


      ###########################################################
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gray_btn.setText(_translate("MainWindow", " To Gray "))
        self.invert_btn.setText(_translate("MainWindow", "Invert Image Colour"))
        self.histoeq_btn.setText(_translate("MainWindow", "Histogram Equalization"))
        self.gaunoise_btn.setText(_translate("MainWindow", "Gaussian Noise"))
        self.boxfil_btn.setText(_translate("MainWindow", "Box Filter"))
        self.gaufil_btn.setText(_translate("MainWindow", "Gaussian Filter"))
        self.saltAndPep_btn.setText(_translate("MainWindow", "Salt and pepper"))
        self.Sharpen_btn.setText(_translate("MainWindow", "Sharpen"))
        self.edgeDetection_btn.setText(_translate("MainWindow", "edge detection"))
        self.median_btn.setText(_translate("MainWindow", "Median Filter"))
        self.crop_btn.setStatusTip(_translate("MainWindow", "Crop"))
        self.L_rotate_btn.setStatusTip(_translate("MainWindow", "Left Rotate"))
        self.R_rotate_btn.setStatusTip(_translate("MainWindow", "Right Rotate"))
        self.hori_flip_btn.setStatusTip(_translate("MainWindow", "Horizontal Flip"))
        self.verti_flip_btn.setStatusTip(_translate("MainWindow", "Vertical Flip"))
        self.zoom_in_btn.setStatusTip(_translate("MainWindow", "Zoom In"))
        self.zoom_out_btn.setStatusTip(_translate("MainWindow", "Zoom Out"))
        self.label.setText(_translate("MainWindow", "Contrast"))
        self.bright.setText(_translate("MainWindow", "Brightness"))
        self.label_3.setText(_translate("MainWindow", "Hue"))
        self.saturation.setText(_translate("MainWindow", "Saturation"))
        self.label_5.setText(_translate("MainWindow", "Value"))
        self.open_btn.setText(_translate("MainWindow", "Open"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.reset_btn.setText(_translate("MainWindow", "Reset"))
        self.Blabel.setText(_translate("MainWindow", "    B"))
        self.Glabel.setText(_translate("MainWindow", "    G    "))
        self.Rlabel.setText(_translate("MainWindow", "    R"))


app = QtWidgets.QApplication(sys.argv)
MainWindow = Ui_MainWindow()
MainWindow.show()
sys.exit(app.exec_())

