#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QSpacerItem

NUM_LAYOUT = 4
DEFAULT_LAYOUT = 2

def populateLayout(parent, layout, index):
    
    if (index == 0):
      
        parent.setBackground("/var/fspanel/images/metal3.jpg")

        #layout.setHorizontalSpacing(20)
        #layout.setVerticalSpacing(20)
        layout.setSpacing(0)
        
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        layout.addLayout(hbox, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        
        layout.addWidget(parent.adf, 1, 0, Qt.AlignTop | Qt.AlignLeft)

        #layout.addWidget(parent.switch, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        
    elif (index == 1):
      
        parent.setBackground("/var/fspanel/images/metal5.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(30)
        
        #spacer = QSpacerItem(1200, 25)
        #layout.addItem(spacer, 0, 0, 1, 4)
        
        layout.addWidget(parent.airspeed, 1, 0, Qt.AlignBottom)
        layout.addWidget(parent.attitude, 1, 1, Qt.AlignBottom)
        layout.addWidget(parent.altitude, 1, 2, Qt.AlignBottom)
        
        vbox = QGridLayout()
        vbox.setSpacing(20)
        vbox.addWidget(parent.radio, 0, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.ident, 1, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.engine, 2, 0, 1, 2, Qt.AlignBottom)
        vbox.addWidget(parent.fuel, 3, 0, Qt.AlignBottom)
        vbox.addWidget(parent.vacuum, 3, 1, Qt.AlignBottom)
        layout.addLayout(vbox, 1, 3, 3, 1, Qt.AlignTop)
        
        layout.addWidget(parent.turnslip, 2, 0, Qt.AlignBottom)
        layout.addWidget(parent.dg, 2, 1, Qt.AlignBottom)
        layout.addWidget(parent.vario, 2, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.oil, 3, 0)
        layout.addWidget(parent.trim, 3, 1, Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(parent.vor, 3, 2, Qt.AlignTop)
        
        #layout.addWidget(parent.switch, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        layout.addLayout(hbox, 4, 0, 1, 4, Qt.AlignTop | Qt.AlignLeft)
      
    elif (index == 2):

        parent.setBackground("/var/fspanel/images/metal1.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(30)
        
        #spacer = QSpacerItem(1200, 25)
        #layout.addItem(spacer, 0, 0, 1, 4)
        
        layout.addWidget(parent.airspeed, 0, 0, Qt.AlignBottom)
        layout.addWidget(parent.attitude, 0, 1, Qt.AlignBottom)
        layout.addWidget(parent.altitude, 0, 2, Qt.AlignBottom)
        
        vbox = QGridLayout()
        vbox.setSpacing(20)
        vbox.addWidget(parent.radio, 0, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.ident, 1, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.fuel, 2, 0, Qt.AlignBottom)
        vbox.addWidget(parent.vacuum, 2, 1, Qt.AlignBottom)
        vbox.addWidget(parent.engine, 3, 0, 1, 2, Qt.AlignBottom)
        layout.addLayout(vbox, 0, 3, 3, 1, Qt.AlignTop)
        
        layout.addWidget(parent.turnslip, 1, 0, Qt.AlignBottom)
        layout.addWidget(parent.dg, 1, 1, Qt.AlignBottom)
        layout.addWidget(parent.vario, 1, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.oil, 2, 0)
        layout.addWidget(parent.trim, 2, 1, Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(parent.vor, 2, 2, Qt.AlignTop)
        
        #layout.addWidget(parent.switch, 3, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        layout.addLayout(hbox, 3, 0, 1, 4, Qt.AlignTop | Qt.AlignLeft)

    elif (index == 3):

        parent.setBackground("/var/fspanel/images/metal3.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(30)
        
        layout.addWidget(parent.debug, 0, 0)
        parent.debug.setStyleSheet("background: rgba(0,0,0,90%); color: rgba(0,255,0,90%)")
        
