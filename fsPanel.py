#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time

from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot, QObjectCleanupHandler
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QStackedLayout, QLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QPalette, QBrush

from fsSocket import *
from fsGauge import *
from fsLayout import *
from fsDebug import *


class Main(QWidget):
  
    def __init__(self):
        QWidget.__init__(self)
        
        self.magneto = magnetoGauge()
        self.magneto.initialize({'mag': {'value':0}})
        
        self.switch = switchPanel()
        
        self.light = lightPanel()
        
        self.warn = warnPanel()
        
        self.radio = radioPanel()
        self.radio.initialize({})
        
        self.airspeed = airspeedGauge()
        
        self.accelerometer = accelerometerGauge()
        self.accelerometer.initialize({'load': {'value':0}})
        
        self.attitude = attitudeGauge()
        self.attitude.initialize({'pitch': {'value':0}, 'roll': {'value':0}})
        
        self.altitude = altitudeGauge()
        self.altitude.initialize({'alt': {'value':0}, 'baro': {'value':0}})
        
        self.turnslip = turnslipGauge()
        self.turnslip.initialize({'turn': {'value':0}, 'slip': {'value':0}})
        
        self.dg = dgGauge()
        self.dg.initialize({'cap': {'value':0}})
        
        self.vario = varioGauge()
        self.vario.initialize({'vvi': {'value':0}})
        
        self.fuel = fuelGauge()
        self.fuel.initialize({'fuel': {'value':0}})
        
        self.manifold = manifoldGauge()
        self.manifold.initialize({'man': {'value':0}, 'flow': {'value':0}})
        
        self.vacuum = vacuumGauge()
        self.vacuum.initialize({'vacuum': {'value':0}})
        
        self.oil = oilGauge()
        self.oil.initialize({'heat': {'value':0, 'max': 250}, 'psi': {'value':0, 'max': 25}})
        
        self.vor = vorGauge()
        self.vor.initialize({'obs': {'value':0}, 'tofr': {'value':1}, 'dme': {'value':0}, 'hdef': {'value':0}, 'vdef': {'value':0}})
        
        self.adf = adfGauge()
        self.adf.initialize({'frq': {'value':0}, 'card': {'value':0}, 'brg': {'value':0}})
        
        self.engine = engineGauge()
        self.engine.initialize({'rpm': {'value':0}})
        
        self.trim = trimGauge()
        self.trim.initialize({'pitch': {'value':0}})
        
        self.ident = identPanel()
        
        self.debug = fsDebug(self)
        self.debug.keyPressEvent = self.keyPressEvent
        self.debug.appendText('debug initiated', 'info')
        self.debug.appendText('error test', 'error')
        
        self.stack = QStackedLayout(self)
        #print (self.stack.parent.vor.param)
        
        for i in range(NUM_LAYOUT):
          page = QWidget()
          layout = QGridLayout()
          page.setLayout(layout)
          self.stack.addWidget(page)
        self.setFSLayout(DEFAULT_LAYOUT)
        
        self.b = 0
        
    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_1):
          self.setFSLayout(1)
        elif (key == Qt.Key_2):
          self.setFSLayout(2)
        elif (key == Qt.Key_3):
          self.setFSLayout(3)
        elif (key == Qt.Key_4):
          self.setFSLayout(4)
        elif (key == Qt.Key_5):
          self.b = (self.b + 1) % 2
          self.switch.setValue({'power':self.b})
          self.light.setValue({'power':self.b})
          #self.warn.setValue({'power':self.b,'gene':1,'oil':1,'fuel':1,'gear':1})
        elif (key == Qt.Key_D):
          self.setFSLayout(0)
        elif (key == Qt.Key_Space):
          self.setWindowState(self.windowState() ^ Qt.WindowFullScreen)
        elif (key == Qt.Key_Q):
          self.close()
        elif (key == Qt.Key_7):
          self.setPanel(-1)
        elif (key == Qt.Key_9):
          self.setPanel(1)
        
        elif (key == Qt.Key_B):
          self.airspeed.setup({'unit':'kt'})
        elif (key == Qt.Key_N):
          self.airspeed.setup({'unit':'kmh'})

        elif (key == Qt.Key_C):
          self.light.setValue({'strobe':1})
        elif (key == Qt.Key_U):
          self.socket.send("com", "outer", -1)
        elif (key == Qt.Key_I):
          self.socket.send("com", "outer", 1)
        elif (key == Qt.Key_O):
          self.socket.send("com", "inner", -1)
        elif (key == Qt.Key_P):
          self.socket.send("com", "inner", 1)
        elif (key == Qt.Key_K):
          self.socket.send("com", "button", 1)
        elif (key == Qt.Key_L):
          self.socket.send("nav", "coder", -1)
        elif (key == Qt.Key_M):
          self.socket.send("nav", "coder", 1)
        

    def setBackground(self, pic):
        palette = QPalette()
        pixmap = QPixmap(pic)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)
    
    def setPanel(self, direction):
        index = (self.activeLayout + direction) % NUM_LAYOUT
        if (index == 0):
          index = (index + direction) % NUM_LAYOUT
        self.setFSLayout(index)

    def setFSLayout(self, index):
        self.activeLayout = index
        #self.stack.setCurrentIndex(index)
        layout = self.stack.widget(index).layout()
        populateLayout(self, layout, index)
        self.stack.setCurrentIndex(index)
    
    def setUDPSocket(self, socket):
      
        self.socket = socket
        
        socket.switch.connect(self.switch.setValue)
        socket.light.connect(self.light.setValue)
        socket.warn.connect(self.warn.setValue)
        socket.radio.connect(self.radio.setValue)
        socket.airspeed.connect(self.airspeed.setValue)
        socket.load.connect(self.accelerometer.setValue)
        socket.attitude.connect(self.attitude.setValue)
        socket.altitude.connect(self.altitude.setValue)
        socket.turnslip.connect(self.turnslip.setValue)
        socket.dg.connect(self.dg.setValue)
        socket.vario.connect(self.vario.setValue)
        socket.vacuum.connect(self.vacuum.setValue)
        socket.flow.connect(self.manifold.setValue)
        socket.fuel.connect(self.fuel.setValue)
        socket.oil.connect(self.oil.setValue)
        socket.vor.connect(self.vor.setValue)
        socket.adf.connect(self.adf.setValue)
        socket.engine.connect(self.engine.setValue)
        socket.trim.connect(self.trim.setValue)
        socket.magneto.connect(self.magneto.setValue)
        
        socket.panel.connect(self.setPanel)
        socket.debug.connect(self.debug.appendText)
        
      
def main():
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    
    thread = QThread()
    socket = fsSocket()
    socket.moveToThread(thread)
    socket.finished.connect(thread.quit)
    thread.started.connect(socket.run)
    
    fs = Main()
    fs.setUDPSocket(socket)
    fs.setWindowTitle("FS Panel")
    fs.resize(1280, 1024)
    fs.setGeometry(0,0,1280,1024)
    fs.move(0,0)
    #fs.show()
    fs.showFullScreen()
    
    '''
    th = QThread()
    fsw = fsWorker()
    fsw.moveToThread(th)
    fsw.finished.connect(th.quit)
    th.started.connect(fsw.run)
    fsw.layout.connect(fs.setFSLayout)
    th.start()
    '''
    
    thread.start()
    
    app.exec_()
    
    socket.stop()
    thread.quit()
    
    sys.exit(0)


if __name__ == "__main__":
    main()
    
