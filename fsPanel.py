#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QObjectCleanupHandler
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QStackedLayout, QLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QPalette, QBrush

from fsSocket import *
from fsGauge import *
from fsLayout import *

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self.switch = switchPanel()
        self.light = lightPanel()
        self.radio = radioPanel()
        self.airspeed = airspeedGauge()
        self.attitude = attitudeGauge()
        self.altitude = altitudeGauge()
        self.turnslip = turnslipGauge()
        self.dg = dgGauge()
        self.vario = varioGauge()
        self.fuel = fuelGauge()
        self.vacuum = vacuumGauge()
        self.oil = oilGauge()
        self.vor = vorGauge()
        self.adf = adfGauge()
        self.engine = engineGauge()
        self.trim = trimGauge()
        self.ident = identPanel()
        
        self.debug = QTextEdit()
        self.setDebug('debug initiated')
        self.debug.keyPressEvent = self.keyPressEvent
        
        self.stack = QStackedLayout(self)
        for i in range(NUM_LAYOUT):
          page = QWidget()
          layout = QGridLayout()
          page.setLayout(layout)
          self.stack.addWidget(page)
        self.setFSLayout(DEFAULT_LAYOUT)
        

    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_1):
          self.setFSLayout(0)
        elif (key == Qt.Key_2):
          self.setFSLayout(1)
        elif (key == Qt.Key_3):
          self.setFSLayout(2)
        elif (key == Qt.Key_D):
          self.setFSLayout(3)
        elif (key == Qt.Key_Space):
          self.setWindowState(self.windowState() ^ Qt.WindowFullScreen)
        elif (key == Qt.Key_Q):
          self.close()
        elif (key == Qt.Key_V):
          self.socket.send("nav", "button", 1)

    def setBackground(self, pic):
        palette = QPalette()
        pixmap = QPixmap(pic)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)
    
      
    def setPanel(self, direction):
        index = (self.activeLayout + direction ) % NUM_LAYOUT
        self.setFSLayout(index)

    def setFSLayout(self, index):
        self.activeLayout = index
        layout = self.stack.widget(index).layout()
        populateLayout(self, layout, index)
        self.stack.setCurrentIndex(index)
          

    def setDebug(self, text):
      self.debug.append(text)
      #self.debug.insertPlainText(text)
      #self.debug.insertHtml('<font color=red>test</font><br>')
      
    def setUDPSocket(self, socket):
        self.socket = socket
        #socket.battery.connect(self.switch.setSwitch)
        #socket.altern.connect(self.switch.setSwitch)
        #socket.mixture.connect(self.switch.setSwitch)
        #socket.pump.connect(self.switch.setSwitch)
        #socket.carbu.connect(self.switch.setSwitch)
        #socket.gear.connect(self.switch.setSwitch)
        #socket.flaps.connect(self.switch.setSwitch)
        socket.switch.connect(self.switch.setSwitch)
        socket.light.connect(self.light.setLight)
        socket.com.connect(self.radio.setCom)
        socket.nav.connect(self.radio.setNav)
        socket.xpdr.connect(self.radio.setXpdr)
        socket.airspeed.connect(self.airspeed.setValue)
        socket.attitude.connect(self.attitude.setValue)
        socket.altitude.connect(self.altitude.setValue)
        socket.turnslip.connect(self.turnslip.setValue)
        socket.dg.connect(self.dg.setValue)
        socket.vario.connect(self.vario.setValue)
        socket.vacuum.connect(self.vacuum.setValue)
        socket.fuel.connect(self.fuel.setValue)
        socket.oil.connect(self.oil.setValue)
        socket.vor.connect(self.vor.setValue)
        socket.adf.connect(self.adf.setValue)
        socket.engine.connect(self.engine.setValue)
        socket.trim.connect(self.trim.setValue)
        
        socket.panel.connect(self.setPanel)
        socket.debug.connect(self.setDebug)


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
    