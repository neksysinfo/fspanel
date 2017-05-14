#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QPixmap, QPalette, QBrush


class debugTextEdit(QTextEdit):
  
    def __init__(self):
        QTextEdit.__init__(self)
        
        self.setStyleSheet("background-color: rgba(0,0,0,90%); color: rgba(0,255,0,90%)")
        
    def appendText(self, text, status=''):
      
      if (status == 'info'):
        self.insertHtml('<font color=yellow>%s</font><br>' % text)
      elif (status == 'error'):
        self.insertHtml("<font color='red'>%s:</font> <font color='white'>%s</font><br>" % ('error', text))
      elif (status == 'except'):
        self.insertHtml("<font color='red'>%s:</font> <font color='white'>%s</font><br>" % ('except', text))
      else:
        self.insertHtml('<font color=lime>%s</font><br>' % text)


class fsDebug(QObject):

    def __init__(self):
      super().__init__()
      
      self.log = debugTextEdit()
      #self.log.keyPressEvent = self.keyPressEvent

    def appendText(self, text, status=''):
      self.log.appendText(text, status)

