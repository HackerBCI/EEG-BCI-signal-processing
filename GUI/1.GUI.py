import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.Qt import *
import random
import threading 
import time
import numpy as np
import pandas as pd
from scipy import signal
import serial
import passfilter 


ComPort = serial.Serial('COM8') 
ComPort.baudrate = 115200          
ComPort.bytesize = 8            
ComPort.parity   = 'N'           
ComPort.stopbits = 1
random_data = np.arange(50)

global fs
fs = 10     
global cutoff
cutoff = 2

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
               
        self.setMinimumSize(QSize(300, 200))    
        self.setWindowTitle("BCI") 
        pybutton = QPushButton('Click me', self)        
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)        
    def clickMethod(self):
        print('Clicked Pyqt button.')

        seconWin.show()
        mainWin.close()

class second_window(QWidget):

    def __init__(self):
        print ("start")       
        QWidget.__init__(self)

        self.setMinimumSize(QSize(600, 500))    
        self.setWindowTitle("Iron_BCI") 
              

        self.figure = plt.figure(figsize=(0,2,),facecolor='y',  edgecolor='r') #  color only     
        self.figure1 = plt.figure(figsize=(0,2),facecolor='y') # color only
                
        self.canvas = FigureCanvas(self.figure)
        self.figure.subplots_adjust(0.2, 0.4, 0.8, 1)  # only graph 
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure1.subplots_adjust(0.2, 0.4, 0.8, 1)  # only graph 
        
       # self.toolbar = NavigationToolbar(self.canvas, self)
       # self.toolbar1 = NavigationToolbar(self.canvas1, self)
        
        pybutton = QPushButton('graph', self)

        
        global axis_x
        axis_x=0


        pybutton.clicked.connect(self.clickMethod)
        pybutton.move(350, 10)
        pybutton.resize(100,32)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50,100,0,11) # move background
        layout.setGeometry(QRect(0, 0, 80, 68))# nothing  
      # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)    
      # layout.addWidget(self.toolbar1)
        layout.addWidget(self.canvas1)        

       # start for add cufoff value
        self.le_num1 = QLineEdit()
        self.le_num1.setFixedSize(50, 20) # size                        
        self.pb_num1 = QPushButton('cutoff')
        self.pb_num1.setFixedSize(50, 60) # size
        self.pb_num1.clicked.connect(self.show_dialog_num1)               
        #layout1 = QGridLayout()        
       # layout.addWidget(QLabel('cutoff'))
        # stop for add cufoff value

        # start for add fps
        self.le_num2 = QLineEdit()
        self.le_num2.setFixedSize(50, 20) # size                        
        self.pb_num2 = QPushButton('fs')
        self.pb_num2.setFixedSize(50, 60) # size
        self.pb_num2.clicked.connect(self.show_dialog_num2)               
        #layout1 = QGridLayout()        
       # layout.addWidget(QLabel('fs'))
        # start for add fps



               
        layout.addWidget(self.le_num1)       
        self.pb_num1.move(10, 0)        
        layout.addWidget(self.pb_num1)
        self.setLayout(layout)

        layout.addWidget(self.le_num2)       
        self.pb_num1.move(90, 100)        
        layout.addWidget(self.pb_num2)
        self.setLayout(layout)
    
    def clickMethod(self):

      #  while 1:
         try:
          for i in range(0,50,1):
        #   print((ComPort.readline()))
           random_data[i] = int(ComPort.readline())
           
          result = pd.DataFrame({'data': random_data} )          
          result = passfilter.butter_highpass_filter(result.data,cutoff, fs)                  
          result = pd.DataFrame({'data': result} )          
          result['data']=result['data'].astype('int')        
         #print (result)
          result  =  passfilter.butter_lowpass_filter(result.data,cutoff, fs)  
         #print (result)
           
         except ValueError:
          print ("ValueError")
                                
         #data = [random.random() for i in range(axis)]
         #data1 = [random.random() for i in range(axis)]
        # print (result)
        # data1=result["data"]

         data=result
         bias= data.sum()/50
       
         #self.figure.clear()
         #self.figure1.clear()
        
         ax = self.figure.add_subplot(111)
         ax1 = self.figure1.add_subplot(111)
        
         #ax.plot(data, '*-')                         
         #ax.axis([0, 2000, 0, 20000])
         global axis_x

         ax.plot(range(axis_x, axis_x+50,1),data,color = '#0a0b0c') 
         ax.axis([axis_x-50, axis_x+50, bias-500, bias+500])  #
         
         ax1.plot(range(axis_x, axis_x+50,1),data) 
         ax1.axis([axis_x-500, axis_x+500, bias-5000, bias+5000])  #
         
         axis_x=axis_x+50        
                  
         self.canvas.draw()
         self.canvas1.draw()

         thread=threading.Thread(target=self.clickMethod, args=())
         thread.start()                
# input data
    def show_dialog_num1(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'cut frecuency:')
        global cutoff
        cutoff = value
        print (cutoff)
    def show_dialog_num2(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'fs:')
        global fs
        fs = value
        print (fs)
        
       # thread.start()
       # mainWin.show()
       # seconWin.close()  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    seconWin = second_window()
   
    
    sys.exit( app.exec_() )
