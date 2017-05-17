#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit, QLabel
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import time


class fsTimer(QObject):
  
    bip = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
      super().__init__()
      
      self.stamp = 0
      
    @pyqtSlot()
    def run(self):
       self.running = True
       print ('fsTimer running')
       
       while self.running:
         stamp = time.time()
         if (stamp - self.stamp >= 0.25):
             self.stamp = stamp
             self.bip.emit()


class debugTextEdit(QTextEdit):
  
    def __init__(self):
        QTextEdit.__init__(self)
        
        self.setStyleSheet("background-color: rgba(0,0,0,90%); color: rgba(0,255,0,90%)")
        
    def appendText(self, text, status=''):
      
      if (status == 'info'):
        self.insertHtml('<font color=yellow>%s</font><br>' % text)
      elif (status == 'debug'):
        self.insertHtml("<font color='white'>%s</font><br>" % (text))
      elif (status == 'error'):
        self.insertHtml("<font color='red'>%s:</font> <font color='white'>%s</font><br>" % ('error', text))
      elif (status == 'except'):
        self.insertHtml("<font color='red'>%s:</font> <font color='white'>%s</font><br>" % ('except', text))
      else:
        self.insertHtml('<font color=lime>%s</font><br>' % text)


class fsDebug(QWidget):

    def __init__(self, parent):
      #super().__init__()
      QWidget.__init__(self)
      
      self.parent = parent
      self.log = debugTextEdit()
      self.fps = QLabel()
      
      self.thread = QThread()
      self.timer = fsTimer()
      self.timer.moveToThread(self.thread)
      self.timer.bip.connect(self.timerBip)
      self.timer.finished.connect(self.thread.quit)
      self.thread.started.connect(self.timer.run)
      
      #self.thread.start()
      try:
        self.thread.start()
        #pass
      except Exception as exc:
        self.log.appendText('socket (%s)' % exc, 'exception')
      
      grid = QGridLayout()
      grid.setSpacing(10)
      grid.addWidget(self.fps, 0, 0, Qt.AlignTop)
      grid.addWidget(self.log, 1, 0, Qt.AlignBottom)
      self.setLayout(grid)

      self.log.keyPressEvent = self.keyPressEvent
      self.fps.keyPressEvent = self.keyPressEvent

    def timerBip(self):
      #pass
      #self.log.appendText(self.parent.switch.getValue("fps"), 'debug')
      self.fps.setText("FPS: %d" % (self.parent.switch.getValue("fps")))
      
    def appendText(self, text, status=''):
      self.log.appendText(text, status)

