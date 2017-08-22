#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QSpacerItem

NUM_LAYOUT = 5
DEFAULT_LAYOUT = 2

def populateLayout(parent, layout, index):
    
    if (index == 0):
      
        parent.setBackground("/var/fspanel/images/metal3.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(30)
        
        layout.addWidget(parent.debug, 0, 0)
        
    elif (index == 1):

        parent.setBackground("/var/fspanel/images/metal3.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(10)
        
        layout.addWidget(parent.warn, 0, 0, 1, 3, Qt.AlignTop | Qt.AlignLeft)
        #parent.warn.initialize({'gene': {'pos':0, 'label':'Charge', 'led':'red', 'value':1}, 'oil': {'pos':1, 'label':'Huile', 'led':'red', 'value':1}, 'fuel': {'pos':2, 'label':'Essence', 'led':'red', 'value':1}, 'brake': {'pos':3, 'label':'Frein', 'led':'white', 'value':0}, 'stall': {'pos':4, 'label':'Stall', 'led':'red', 'value':0}, 'flap': {'pos':6, 'label':'Volets', 'led':'gray', 'text': '0', 'value':0}})
        parent.warn.initialize({'gene': {'pos':0, 'label':'Charge', 'led':'red', 'value':1}, 'oil': {'pos':1, 'label':'Huile', 'led':'red', 'value':1}, 'fuel': {'pos':2, 'label':'Essence', 'led':'red', 'value':1}, 'brake': {'pos':3, 'label':'Park', 'led':'white', 'value':0}, 'stall': {'pos':4, 'label':'Stall', 'led':'red', 'value':0}, 'flap': {'pos':6, 'label':'Volets', 'led':'gray', 'text': '2', 'value':0}})

        vbox = QGridLayout()
        vbox.setSpacing(20)
        vbox.addWidget(parent.radio, 0, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.ident, 1, 0, 1, 2, Qt.AlignTop)
        #parent.ident.initialize({'ident': {'modele': 'EA 330', 'indicatif': 'F-GDTZ'}})
        parent.ident.initialize({'ident': {'modele': 'CAP 10', 'indicatif': 'F-GDTZ'}})
        vbox.addWidget(parent.fuel, 2, 0, Qt.AlignBottom)
        vbox.addWidget(parent.vacuum, 2, 1, Qt.AlignBottom)
        vbox.addWidget(parent.vor, 3, 0, 1, 2, Qt.AlignBottom)
        layout.addLayout(vbox, 0, 3, 4, 1, Qt.AlignTop)
        
        layout.addWidget(parent.airspeed, 1, 0, Qt.AlignBottom)
        #parent.airspeed.initialize({'speed': {'vs0': 0, 'vs1': 120, 'vfe': 0, 'vno': 285, 'vne': 410, 'max': 410}})
        #parent.airspeed.init({'speed': {'vs0': 0, 'vs1': 65, 'vfe': 0, 'vno': 155, 'vne': 220, 'max': 220}})
        parent.airspeed.init({'speed': {'vs0': 46, 'vs1': 53, 'vfe': 86, 'vno': 162, 'vne': 183, 'max': 190}})
        layout.addWidget(parent.accelerometer, 1, 1, Qt.AlignBottom)
        layout.addWidget(parent.altitude, 1, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.turnslip, 2, 0, Qt.AlignBottom)
        layout.addWidget(parent.manifold, 2, 1, Qt.AlignBottom)
        layout.addWidget(parent.vario, 2, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.engine, 3, 0, Qt.AlignBottom)
        layout.addWidget(parent.oil, 3, 1, Qt.AlignCenter)
        layout.addWidget(parent.dg, 3, 2, Qt.AlignBottom)
        
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        parent.switch.initialize({'power': {'pos':0, 'label':'Batterie', 'led':'white', 'value':0}, 'gene': {'pos':1, 'label':'Altern', 'led':'white', 'value':0}, 'fps': {'pos':2, 'value':0}, 'mixt': {'pos':3, 'label':'Mixture', 'led':'white', 'value':0}, 'pump': {'pos':5, 'label':'Pompe', 'led':'white', 'value':0}})
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        parent.light.initialize({'nav': {'pos':0,'label':'Nav','led':'white','value':0}, 'strobe': {'pos':1,'label':'Strobe','led':'white','value':0}})
        layout.addLayout(hbox, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
        
    elif (index == 2):
      
        #parent.setBackground("/var/fspanel/images/metal4.jpg")
        parent.setBackground("/var/fspanel/images/leather1.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(10)
        
        #spacer = QSpacerItem(1200, 25)
        #layout.addItem(spacer, 0, 0, 1, 4)
        
        layout.addWidget(parent.warn, 0, 0, 1, 3, Qt.AlignTop | Qt.AlignLeft)
        parent.warn.initialize({'gene': {'pos':0, 'label':'Charge', 'led':'red', 'value':1}, 'oil': {'pos':1, 'label':'Huile', 'led':'red', 'value':1}, 'fuel': {'pos':2, 'label':'Essence', 'led':'red', 'value':1}, 'brake': {'pos':3, 'label':'Park', 'led':'white', 'value':0}, 'stall': {'pos':4, 'label':'Stall', 'led':'red', 'value':0}, 'flap': {'pos':6, 'label':'Volets', 'led':'gray', 'text': '3', 'value':0}})

        vbox = QGridLayout()
        vbox.setSpacing(20)
        vbox.addWidget(parent.radio, 0, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.ident, 1, 0, 1, 2, Qt.AlignTop)
        #parent.ident.initialize({'ident': {'modele': 'DR 400', 'indicatif': 'F-GJDN'}})
        parent.ident.initialize({'ident': {'modele': 'PA 28', 'indicatif': 'F-GIEK'}})
        vbox.addWidget(parent.engine, 2, 0, 1, 2, Qt.AlignBottom)
        vbox.addWidget(parent.fuel, 3, 0, Qt.AlignBottom)
        vbox.addWidget(parent.vacuum, 3, 1, Qt.AlignBottom)
        layout.addLayout(vbox, 0, 3, 4, 1, Qt.AlignTop)
        
        layout.addWidget(parent.airspeed, 1, 0, Qt.AlignBottom)
        #parent.airspeed.initialize({'speed': {'vs0': 85, 'vs1': 100, 'vfe': 170, 'vno': 260, 'vne': 310, 'max': 310, 'unit': 'kmh', 'value': 0}})
        parent.airspeed.init({'unit': 'kt', 'speed': {'vs0': 49, 'vs1': 60, 'vfe': 102, 'vno': 125, 'vne': 154, 'max': 160}})
        layout.addWidget(parent.attitude, 1, 1, Qt.AlignBottom)
        layout.addWidget(parent.altitude, 1, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.turnslip, 2, 0, Qt.AlignBottom)
        layout.addWidget(parent.dg, 2, 1, Qt.AlignBottom)
        layout.addWidget(parent.vario, 2, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.adf, 3, 0, Qt.AlignBottom)
        layout.addWidget(parent.oil, 3, 1, Qt.AlignCenter)
        layout.addWidget(parent.vor, 3, 2, Qt.AlignBottom)
        
        #layout.addWidget(parent.switch, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        parent.switch.initialize({'power': {'pos':0, 'label':'Batterie', 'led':'white', 'value':0}, 'gene': {'pos':1, 'label':'Altern', 'led':'white', 'value':0}, 'fps': {'pos':2, 'value':0}, 'mixt': {'pos':3, 'label':'Mixture', 'led':'white', 'value':0}, 'carbheat': {'pos':4, 'label':'Carbu', 'led':'white', 'value':0}, 'pump': {'pos':5, 'label':'Pompe', 'led':'white', 'value':0}})
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        parent.light.initialize({'nav': {'pos':0,'label':'Nav','led':'white','value':0}, 'strobe': {'pos':1,'label':'Strobe','led':'white','value':0}, 'landing': {'pos':2,'label':'Landing','led':'white','value':0}, 'taxi': {'pos':3,'label':'Taxi','led':'white','value':0}})
        layout.addLayout(hbox, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
      
    elif (index == 3):
      
        #parent.setBackground("/var/fspanel/images/metal4.jpg")
        parent.setBackground("/var/fspanel/images/leather3.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(10)
        
        #spacer = QSpacerItem(1200, 25)
        #layout.addItem(spacer, 0, 0, 1, 4)
        
        layout.addWidget(parent.warn, 0, 0, 1, 3, Qt.AlignTop | Qt.AlignLeft)
        parent.warn.initialize({'gene': {'pos':0, 'label':'Charge', 'led':'red', 'value':1}, 'oil': {'pos':1, 'label':'Huile', 'led':'red', 'value':1}, 'fuel': {'pos':2, 'label':'Essence', 'led':'red', 'value':1}, 'brake': {'pos':3, 'label':'Park', 'led':'white', 'value':0}, 'stall': {'pos':4, 'label':'Stall', 'led':'red', 'value':0}, 'flap': {'pos':6, 'label':'Volets', 'led':'gray', 'text': '2', 'value':0}})

        vbox = QGridLayout()
        vbox.setSpacing(20)
        vbox.addWidget(parent.radio, 0, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.ident, 1, 0, 1, 2, Qt.AlignTop)
        parent.ident.initialize({'ident': {'modele': 'DR 400', 'indicatif': 'F-GJDN'}})
        vbox.addWidget(parent.engine, 2, 0, 1, 2, Qt.AlignBottom)
        vbox.addWidget(parent.fuel, 3, 0, Qt.AlignBottom)
        vbox.addWidget(parent.vacuum, 3, 1, Qt.AlignBottom)
        layout.addLayout(vbox, 0, 3, 4, 1, Qt.AlignTop)
        
        layout.addWidget(parent.airspeed, 1, 0, Qt.AlignBottom)
        #parent.airspeed.initialize({'speed': {'vs0': 85, 'vs1': 100, 'vfe': 170, 'vno': 260, 'vne': 310, 'max': 310}})
        parent.airspeed.init({'speed': {'vs0': 47, 'vs1': 53, 'vfe': 92, 'vno': 140, 'vne': 166, 'max': 170}})
        layout.addWidget(parent.attitude, 1, 1, Qt.AlignBottom)
        layout.addWidget(parent.altitude, 1, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.turnslip, 2, 0, Qt.AlignBottom)
        layout.addWidget(parent.dg, 2, 1, Qt.AlignBottom)
        layout.addWidget(parent.vario, 2, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.adf, 3, 0, Qt.AlignBottom)
        layout.addWidget(parent.oil, 3, 1, Qt.AlignCenter)
        layout.addWidget(parent.vor, 3, 2, Qt.AlignBottom)
        
        #layout.addWidget(parent.switch, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        parent.switch.initialize({'power': {'pos':0, 'label':'Batterie', 'led':'white', 'value':0}, 'gene': {'pos':1, 'label':'Altern', 'led':'white', 'value':0}, 'fps': {'pos':2, 'value':0}, 'mixt': {'pos':3, 'label':'Mixture', 'led':'white', 'value':0}, 'carbheat': {'pos':4, 'label':'Carbu', 'led':'white', 'value':0}, 'pump': {'pos':5, 'label':'Pompe', 'led':'white', 'value':0}})
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        parent.light.initialize({'nav': {'pos':0,'label':'Nav','led':'white','value':0}, 'strobe': {'pos':1,'label':'Strobe','led':'white','value':0}, 'landing': {'pos':2,'label':'Landing','led':'white','value':0}, 'taxi': {'pos':3,'label':'Taxi','led':'white','value':0}})
        layout.addLayout(hbox, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
      
    elif (index == 4):

        parent.setBackground("/var/fspanel/images/metal1.jpg")

        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(10)
        
        #spacer = QSpacerItem(1200, 25)
        #layout.addItem(spacer, 0, 0, 1, 4)
        
        layout.addWidget(parent.warn, 0, 0, 1, 3, Qt.AlignTop | Qt.AlignLeft)
        parent.warn.initialize({'gene': {'pos':0, 'label':'Charge', 'led':'red', 'value':1}, 'oil': {'pos':1, 'label':'Huile', 'led':'red', 'value':1}, 'fuel': {'pos':2, 'label':'Essence', 'led':'red', 'value':1}, 'brake': {'pos':3, 'label':'Park', 'led':'white', 'value':0}, 'stall': {'pos':4, 'label':'Stall', 'led':'red', 'value':0}, 'flap': {'pos':6, 'label':'Volets', 'led':'gray', 'text': '2', 'value':0}})

        vbox = QGridLayout()
        vbox.setSpacing(20)
        vbox.addWidget(parent.radio, 0, 0, 1, 2, Qt.AlignTop)
        vbox.addWidget(parent.ident, 1, 0, 1, 2, Qt.AlignTop)
        parent.ident.initialize({'ident': {'modele': 'DR 221', 'indicatif': 'F-BOZK'}})
        vbox.addWidget(parent.fuel, 2, 0, Qt.AlignBottom)
        vbox.addWidget(parent.vacuum, 2, 1, Qt.AlignBottom)
        vbox.addWidget(parent.engine, 3, 0, 1, 2, Qt.AlignBottom)
        layout.addLayout(vbox, 0, 3, 4, 1, Qt.AlignTop)
        
        layout.addWidget(parent.airspeed, 1, 0, Qt.AlignBottom)
        #parent.airspeed.initialize({'scale': {'value': 0.85}, 'speed': {'vs0': 80, 'vs1': 90, 'vfe': 150, 'vno': 210, 'vne': 240, 'max': 250}})
        parent.airspeed.init({'scale': {'value': 0.85}, 'speed': {'vs0': 44, 'vs1': 51, 'vfe': 81, 'vno': 116, 'vne': 145, 'max': 150}})
        layout.addWidget(parent.attitude, 1, 1, Qt.AlignBottom)
        layout.addWidget(parent.altitude, 1, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.turnslip, 2, 0, Qt.AlignBottom)
        layout.addWidget(parent.dg, 2, 1, Qt.AlignBottom)
        layout.addWidget(parent.vario, 2, 2, Qt.AlignBottom)
        
        layout.addWidget(parent.oil, 3, 0, Qt.AlignCenter)
        #layout.addWidget(parent.trim, 3, 1, Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(parent.magneto, 3, 1, Qt.AlignCenter)
        layout.addWidget(parent.vor, 3, 2, Qt.AlignBottom)
        
        #layout.addWidget(parent.switch, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)
        hbox = QGridLayout()
        hbox.setSpacing(0)
        hbox.addWidget(parent.switch, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignRight)
        parent.switch.initialize({'power': {'pos':0, 'label':'Batterie', 'led':'white', 'value':0}, 'gene': {'pos':1, 'label':'Altern', 'led':'white', 'value':0}, 'fps': {'pos':2, 'value':0}, 'mixt': {'pos':3, 'label':'Mixture', 'led':'white', 'value':0}, 'carbheat': {'pos':4, 'label':'Carbu', 'led':'white', 'value':0}, 'pump': {'pos':5, 'label':'Pompe', 'led':'white', 'value':0}})
        hbox.addWidget(parent.light, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        parent.light.initialize({'nav': {'pos':0,'label':'Nav','led':'white','value':0}, 'strobe': {'pos':1,'label':'Strobe','led':'white','value':0}, 'speedbrake': {'pos':3,'label':'Cockpit','led':'white','value':0}})
        layout.addLayout(hbox, 4, 0, 1, 4, Qt.AlignBottom | Qt.AlignLeft)

