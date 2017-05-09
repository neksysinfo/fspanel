#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtGui import QImage, QPixmap, QTransform, QFont, QBrush, QPen, QPainter, QPainterPath

class QGaugeView(QGraphicsView):
  
    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene()
        
        self.setScene(self.scene)
        self.setStyleSheet("border: 0px; background: transparent;")
        
class airspeedGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        self.setRenderHint(QPainter.Antialiasing, True)
        
        self.zeroAngle = -180
        
    def initialize(self, data):
      
        self.vso = data['vs0']
        self.vne = data['vne']
        self.max = data['max']
        
        delta = 300 / (self.max - 50)
        
        self.scene.clear()
        
        pixmap = QPixmap('/var/fspanel/images/speed-plate.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        path = QPainterPath()
        pen = QPen(Qt.white, 12, Qt.SolidLine)
        a1 = 270 - ((data['vfe']-50) * delta + 30)
        a2 = (data['vfe'] - data['vs0']) * delta
        path.arcMoveTo(40, 40, 220, 220, a1)
        path.arcTo(40, 40, 220, 220, a1, a2)      
        self.scene.addPath(path, pen)
        
        path = QPainterPath()
        pen = QPen(Qt.green, 10, Qt.SolidLine)
        a1 = 270 - ((data['vno']-50) * delta + 30)
        a2 = (data['vno'] - data['vs1']) * delta
        path.arcMoveTo(50, 50, 200, 200, a1)
        path.arcTo(50, 50, 200, 200, a1, a2)
        self.scene.addPath(path, pen)
      
        path = QPainterPath()
        pen = QPen(Qt.yellow, 10, Qt.SolidLine)
        a1 = 270 - ((data['vne']-50)*delta + 30)
        a2 = (data['vne'] - data['vno']) * delta
        path.arcMoveTo(50, 50, 200, 200, a1)
        path.arcTo(50, 50, 200, 200, a1, a2)
        self.scene.addPath(path, pen)
        
        for a in range(50, data['max']+1, 10):

            alpha = self.zeroAngle + 30 + (a - 50) * delta
            dx = math.cos(math.radians(alpha-90))
            dy = math.sin(math.radians(alpha-90))

            if (a % 50 == 0):
              R = 75
              font = QFont('Verdana', 12, QFont.Light)
              text = self.scene.addSimpleText(str(a), font)
              text.setPos(135+50*dx,140+50*dy)
              text.setBrush(Qt.white)
            else:
              R = 90
              
            if (a == self.vne):
              R = 75
              pen = QPen(Qt.red, 3, Qt.SolidLine)
            else:
              pen = QPen(Qt.white, 3, Qt.SolidLine)

            path = QPainterPath()
            path.moveTo(150+110*dx, 150+110*dy)
            path.lineTo(150+R*dx, 150+R*dy)
            self.scene.addPath(path, pen)
            
        pixmap = QPixmap('/var/fspanel/images/speed-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        font = QFont('Arial', 14, QFont.Light)
        self.speed = self.scene.addSimpleText('0', font)
        self.speed.setPos(135,185)
        self.speed.setBrush(Qt.yellow)
        
        self.setValue({"speed":0})

    def setValue(self, value):
      if "speed" in value:
        speed = int(value["speed"] * 1.852)
        delta = 300 / (self.max - 50)
        if (speed < 50): angle = 0
        elif (speed <= self.max): angle = 30 + (speed - 50) * delta
        else: angle = 300
        self.needle.setRotation(self.zeroAngle + angle)
        self.speed.setText('{:>3}'.format(speed))


class accelerometerGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        self.setRenderHint(QPainter.Antialiasing, True)
        
        pixmap = QPixmap('/var/fspanel/images/g-unit-plate.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        path = QPainterPath()
        pen = QPen(Qt.red, 15, Qt.SolidLine)
        a1 = 55
        a2 = 5
        path.arcMoveTo(45, 45, 210, 210, a1)
        path.arcTo(45, 45, 210, 210, a1, a2)
        self.scene.addPath(path, pen)
      
        path = QPainterPath()
        pen = QPen(Qt.yellow, 15, Qt.SolidLine)
        a1 = 65
        a2 = 20
        path.arcMoveTo(45, 45, 210, 210, a1)
        path.arcTo(45, 45, 210, 210, a1, a2)
        self.scene.addPath(path, pen)
      
        path = QPainterPath()
        pen = QPen(Qt.green, 15, Qt.SolidLine)
        a1 = 85
        a2 = 170
        path.arcMoveTo(45, 45, 210, 210, a1)
        path.arcTo(45, 45, 210, 210, a1, a2)
        self.scene.addPath(path, pen)
      
        path = QPainterPath()
        pen = QPen(Qt.yellow, 15, Qt.SolidLine)
        a1 = 255
        a2 = 20
        path.arcMoveTo(45, 45, 210, 210, a1)
        path.arcTo(45, 45, 210, 210, a1, a2)
        self.scene.addPath(path, pen)
      
        path = QPainterPath()
        pen = QPen(Qt.red, 15, Qt.SolidLine)
        a1 = 275
        a2 = 30
        path.arcMoveTo(45, 45, 210, 210, a1)
        path.arcTo(45, 45, 210, 210, a1, a2)
        self.scene.addPath(path, pen)
     
        g = 6
        
        for a in range(25):

          alpha = 30 - (a * 10)
          dx = math.cos(math.radians(alpha-90))
          dy = math.sin(math.radians(alpha-90))
            
          if (a % 2 == 0):
            R = 75
            X = R * math.cos(math.radians(alpha-90))
            Y = R * math.sin(math.radians(alpha-90))
            font = QFont('Verdana', 12, QFont.Light)
            text = self.scene.addSimpleText(str(abs(g)), font)
            text.setPos(145+R*dx,142+R*dy)
            text.setBrush(Qt.gray)
            g = g - 1
            	    
          path = QPainterPath()
          path.moveTo(150+110*dx, 150+110*dy)
          path.lineTo(150+90*dx, 150+90*dy)
          if (a % 2 == 0):
            pen = QPen(Qt.gray, 3, Qt.SolidLine)
          else:
            pen = QPen(Qt.white, 3, Qt.SolidLine)
          self.scene.addPath(path, pen)
        
        pixmap = QPixmap('/var/fspanel/images/speed-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        self.zeroAngle = -90
        self.setValue({"load":0})
        
    def setValue(self, value):
        if "load" in value:
          load = value["load"]
        angle = load * 20
        self.needle.setRotation(self.zeroAngle + angle)

      
class manifoldGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        self.setRenderHint(QPainter.Antialiasing, True)
        
        pixmap = QPixmap('/var/fspanel/images/speed-plate.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        for a in range(10, 36, 1):

            alpha = -175 + (a - 10) * 170 / 25
            dx = math.cos(math.radians(alpha-90))
            dy = math.sin(math.radians(alpha-90))

            if (a % 5 == 0):
              R = 90
              font = QFont('Verdana', 12, QFont.Light)
              text = self.scene.addSimpleText(str(a), font)
              text.setPos(135 + 65 * dx, 140 + 65 * dy)
              text.setBrush(Qt.white)
            else:
              R = 100
              
            pen = QPen(Qt.white, 3, Qt.SolidLine)

            path = QPainterPath()
            path.moveTo(150+110*dx, 150+110*dy)
            path.lineTo(150+R*dx, 150+R*dy)
            self.scene.addPath(path, pen)
            
        for a in range(3, 19, 1):

            alpha = 175 - a * a / 2
            dx = math.cos(math.radians(alpha-90))
            dy = math.sin(math.radians(alpha-90))

            if (a % 2 == 0):
              R = 95
              font = QFont('Verdana', 10, QFont.Light)
              text = self.scene.addSimpleText('{:2d}'.format(a), font)
              text.setPos(138 + 80 * dx, 142 + 80 * dy)
              text.setBrush(Qt.white)
            else:
              R = 100
              
            pen = QPen(Qt.white, 3, Qt.SolidLine)

            path = QPainterPath()
            path.moveTo(150+110*dx, 150+110*dy)
            path.lineTo(150+R*dx, 150+R*dy)
            self.scene.addPath(path, pen)
            
        pixmap = QPixmap('/var/fspanel/images/speed-dial.png')
        self.pressure = self.scene.addPixmap(pixmap)
        self.pressure.setTransformOriginPoint(QPoint(150,150))
        self.fuelflow = self.scene.addPixmap(pixmap)
        self.fuelflow.setTransformOriginPoint(QPoint(150,150))
      
        self.setValue({"man":0, "flow":0})
        
    def setValue(self, value):
        if "man" in value:
          man = value["man"]
          if (man < 10): man = 10
        if "flow" in value:
          flow = value["flow"]
          
        angle = -175 + (man - 10) * 170 / 25
        if (angle > -5): angle = -5
        self.pressure.setRotation(angle)
        
        angle = 175 - flow * flow / 2
        if (angle < 5): angle = 5
        self.fuelflow.setRotation(angle)

      
class attitudeGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/attitude-backplate.png')
        self.back = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/attitude-disc.png')
        self.disc = self.scene.addPixmap(pixmap)
        self.disc.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/attitude-background.png')
        self.mask = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/attitude-gear.png')
        self.gear = self.scene.addPixmap(pixmap)
        self.gear.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/attitude-planeshape.png')
        self.plane = self.scene.addPixmap(pixmap)
        self.plane.setTransformOriginPoint(QPoint(150,150))        
        
        self.zeroAngle = 0
        self.setValue({"roll":0, "pitch":0})
        
    def setValue(self, value):
      
      if "pitch" in value:
        pitch = value["pitch"]
        self.disc.setTransform(QTransform().translate(0, pitch * 1.5), False)

      if "roll" in value:
        roll = value["roll"]
        self.gear.setRotation(-roll)
        self.disc.setRotation(-roll)


class altitudeGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/altitude.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/altitude-dial-10000.png')
        self.needle10000 = self.scene.addPixmap(pixmap)
        self.needle10000.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/altitude-dial-1000.png')
        self.needle1000 = self.scene.addPixmap(pixmap)
        self.needle1000.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/altitude-dial-100.png')
        self.needle100 = self.scene.addPixmap(pixmap)
        self.needle100.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/altitude-hatch.png')
        self.hatch = self.scene.addPixmap(pixmap)
       
        font = QFont('Arial', 10, QFont.Light)
        self.baro = self.scene.addSimpleText('0', font)
        self.baro.setPos(226,142)
        self.baro.setBrush(Qt.white)
        
        self.zeroAngle = 0
        self.setValue({"alt":0, "baro":0})
        
    def setValue(self, value):
      
      if "alt" in value:
        altitude = value["alt"]
        self.needle100.setRotation((360 / 1000) * altitude)
        self.needle1000.setRotation((360 / 10000) * altitude)
        self.needle10000.setRotation((360 / 100000) * altitude)
        if (altitude > 10000): hatch = False
        else: hatch = True
        self.hatch.setVisible(hatch)

      if "baro" in value:
        baro = int(value["baro"] * 33.863886)
        #self.baro.setText('%5s' % baro)
        self.baro.setText('{:>4}'.format(baro))

class turnslipGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)
        
        pixmap = QPixmap('/var/fspanel/images/turnslip-disc.png')
        self.disc = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/turnslip-ball.png')
        self.ball = self.scene.addPixmap(pixmap)
        self.ball.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/turnslip-gear.png')
        self.gear = self.scene.addPixmap(pixmap)
        self.gear.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/turnslip-planeshape.png')
        self.plane = self.scene.addPixmap(pixmap)
        self.plane.setTransformOriginPoint(QPoint(150,150))

        self.zeroAngle = 0
        self.setValue({"slip":0, "turn":0})
        
    def setValue(self, value):
      
      if "slip" in value:
        slip = value["slip"]
        dx = int(slip * 12)
        self.ball.setTransform(QTransform().translate(-dx, 0), False)

      if "turn" in value:
        turn = value["turn"]
        if (turn <= -35): turn = -35
        elif (turn >= 35): turn = 35
        self.plane.setRotation(turn)


class dgGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/dg-disc.png')
        self.disc = self.scene.addPixmap(pixmap)
        self.disc.setTransformOriginPoint(QPoint(150,150))

        pixmap = QPixmap('/var/fspanel/images/dg-gear.png')
        self.gear = self.scene.addPixmap(pixmap)
        
        self.setValue({"cap":0})
        
    def setValue(self, value):
      
      if "cap" in value:
        cap = value["cap"]
        self.disc.setRotation(-cap)


class varioGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/verticalspeed.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/verticalspeed-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        self.zeroAngle = -90
        self.setValue({"vvi":0})
        
    def setValue(self, value):
      
      if "vvi" in value:
        vvi = value["vvi"]
        if (vvi >= -500 and vvi <= 500):
          angle = int((vvi / 500) * 35)
        elif (vvi >= -1000 and vvi <= 1000):
          angle = int(((vvi - 500) / 500) * 46) + 35
        else:
          angle = int(((vvi - 1000)  / 2000) * 98) + 81
        if (angle < -180): angle = -180
        elif (angle > 180): angle = 180
        self.needle.setRotation(self.zeroAngle + angle)


class vorGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/vor-disc.png')
        self.disc = self.scene.addPixmap(pixmap)
        self.disc.setTransformOriginPoint(QPoint(150,150))

        pixmap = QPixmap('/var/fspanel/images/vor-glass.png')
        self.glass = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/vor-to.png')
        self.to = self.scene.addPixmap(pixmap)
        self.to.setPos(175,100)
        self.to.setVisible(True)
        
        pixmap = QPixmap('/var/fspanel/images/vor-from.png')
        self.fr = self.scene.addPixmap(pixmap)
        self.fr.setPos(175,175)
        self.fr.setVisible(False)
        
        pixmap = QPixmap('/var/fspanel/images/vor-needle.png')
        self.needle = self.scene.addPixmap(pixmap)
        
        self.setValue({"obs":0, "tofr":1, "hdef":0})
        
    def setValue(self, value):
      
      if "obs" in value:
        obs = value["obs"]
        self.disc.setRotation(-obs)

      if "tofr" in value:
        tofr = value["tofr"]
        if (tofr == 1):
          self.fr.setVisible(False)
          self.to.setVisible(True)
        else:
          self.fr.setVisible(True)
          self.to.setVisible(False)
	
      if "hdef" in value:
        hdef = value["hdef"]
        dx = int(hdef * 30)
        self.needle.setTransform(QTransform().translate(dx, 0), False)



class adfGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/adf-disc.png')
        self.disc = self.scene.addPixmap(pixmap)
        self.disc.setTransformOriginPoint(QPoint(150,150))

        pixmap = QPixmap('/var/fspanel/images/adf-plate.png')
        self.plate = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/adf-grade.png')
        self.grade = self.scene.addPixmap(pixmap)
        
        #pixmap = QPixmap('/var/fspanel/images/adf-hdg.png')
        #self.hdg = self.scene.addPixmap(pixmap)
        #self.hdg.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/adf-card.png')
        self.brg = self.scene.addPixmap(pixmap)
        self.brg.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/adf-airplane.png')
        self.airplane = self.scene.addPixmap(pixmap)
        
        font = QFont('Arial', 11, QFont.Light)
        self.freq = self.scene.addSimpleText('0', font)
        self.freq.setPos(135,195)
        self.freq.setBrush(Qt.white)
        
        self.setValue({"frq":0, "card":0, "brg":0})
        
    def setValue(self, value):
      
      if "card" in value:
        card = value["card"]
        self.disc.setRotation(card)

      if "brg" in value:
        #pass
        brg = value["brg"]
        #self.hdg.setRotation(hdg)
        self.brg.setRotation(brg)

      if "frq" in value:
        frq = value["frq"]
        self.freq.setText('{:>04}'.format(frq))



class engineGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), True)

        pixmap = QPixmap('/var/fspanel/images/enginerpm.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/enginerpm-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        self.zeroAngle = -123
        self.setValue({"rpm":0})
        
    def setValue(self, value):
      if "rpm" in value:
        rpm = value["rpm"]
        if (rpm <= 0):
           angle = 0
        elif (rpm <= 1000):
           angle = rpm * 0.06
        elif (rpm <= 2500):
           angle = 60 + (rpm - 1000) * 0.08
        elif (rpm <= 3500):
           angle = 180 + (rpm - 2500) * 0.07
        else:
           angle = 250
        self.needle.setRotation(self.zeroAngle + angle)


class vacuumGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,200,200)
        self.setTransform(QTransform().scale(0.9, 0.9), True)
 
        pixmap = QPixmap('/var/fspanel/images/vacuum-back.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/vacuum-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(100,100))
        
        self.zeroAngle = -90
        self.setValue({"vacuum":0})
        
    def setValue(self, value):
      if "vacuum" in value:
        vacuum = int(value["vacuum"] * 5)
        angle = vacuum * 18
        if (angle <= 0):
           angle = 0
        elif (angle >= 180):
           angle = 180
        self.needle.setRotation(self.zeroAngle + angle)


class fuelGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,200,200)
        self.setTransform(QTransform().scale(0.9, 0.9), True)
        
        pixmap = QPixmap('/var/fspanel/images/fuel-gear.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/fuel-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(104,125))
        
        pixmap = QPixmap('/var/fspanel/images/fuel-glass.png')
        self.glass = self.scene.addPixmap(pixmap)

        self.zeroAngle = -60
        self.max = 115
        self.setValue({"fuel":0})
        
    def setValue(self, value):
      
      if "fuel" in value:
        fuel = int((value["fuel"] * 0.4536) / 0.721)
        angle = int((fuel  / self.max) * 120)
        if (angle <= 0):
           angle = 0
        elif (angle >= 100):
           angle = 100
        self.needle.setRotation(self.zeroAngle + angle)


class oilGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,200,200)
        #self.setTransform(QTransform().scale(0.9, 0.9), True)
        
        pixmap = QPixmap('/var/fspanel/images/oil-disc.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/oil-temp-dial.png')
        self.temp = self.scene.addPixmap(pixmap)
        self.temp.setTransformOriginPoint(QPoint(40,100))
        
        pixmap = QPixmap('/var/fspanel/images/oil-psi-dial.png')
        self.psi = self.scene.addPixmap(pixmap)
        self.psi.setTransformOriginPoint(QPoint(160,100))
        
        pixmap = QPixmap('/var/fspanel/images/oil-glass.png')
        self.glass = self.scene.addPixmap(pixmap)
        
        self.setValue({"temp":0, "psi":0})
        
    def setValue(self, value):
      
      if "temp" in value:
        temp = value["temp"]
        angle = int((temp / 130) * 100)
        if (temp <= 0):
           angle = 0
        elif (temp >= 100):
           angle = 100
        self.temp.setRotation(50 - angle)
        
      if "psi" in value:
        psi = value["psi"]
        angle = int((psi / 115) * 100)
        if (psi <= 0):
           angle = 0
        elif (psi >= 100):
           angle = 100
        self.psi.setRotation(angle - 50)


class trimGauge(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,150,275)
        
        pixmap = QPixmap('/var/fspanel/images/trim.png')
        self.trim = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/trim-handle.png')
        self.handle = self.scene.addPixmap(pixmap)
        
        self.setValue({"pitch":0})
        
    def setValue(self, value):
      
      if "pitch" in value:
        pitch = value["pitch"]
        dy = int(pitch * 100)
        if (dy < -100): dy = -100
        elif (dy > 100): dy = 100
        self.handle.setTransform(QTransform().translate(0, dy), False)

      if "yaw" in value:
        pass


class switchPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,800,75)
        
        pixmap = QPixmap('/var/fspanel/images/switch-plate-1.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        font = QFont('Arial', 10, QFont.Light)
        
        self.grayLed = QPixmap('/var/fspanel/images/led-gray.png')
        self.whiteLed = QPixmap('/var/fspanel/images/led-white.png')
        self.greenLed = QPixmap('/var/fspanel/images/led-green.png')
        self.yellowLed = QPixmap('/var/fspanel/images/led-yellow.png')
        self.redLed = QPixmap('/var/fspanel/images/led-red.png')
        
        # 25
        
        label = self.scene.addSimpleText('Batterie', font)
        label.setPos(45,8)
        label.setBrush(Qt.white)
        self.battery = self.scene.addPixmap(self.grayLed)
        self.battery.setPos(50,30)
        
        label = self.scene.addSimpleText('Altern', font)
        label.setPos(160,8)
        label.setBrush(Qt.white)
        self.altern = self.scene.addPixmap(self.grayLed)
        self.altern.setPos(160,30)
        
        # 250
        
        label = self.scene.addSimpleText('Mixture', font)
        label.setPos(380,8)
        label.setBrush(Qt.white)
        self.mixture = self.scene.addPixmap(self.grayLed)
        self.mixture.setPos(380,30)
        
        label = self.scene.addSimpleText('Carbu', font)
        label.setPos(490,8)
        label.setBrush(Qt.white)
        self.carbu = self.scene.addPixmap(self.grayLed)
        self.carbu.setPos(490,30)
        
        label = self.scene.addSimpleText('Pompe', font)
        label.setPos(600,8)
        label.setBrush(Qt.white)
        self.pump = self.scene.addPixmap(self.grayLed)
        self.pump.setPos(600,30)
        
        # 550
        
        label = self.scene.addSimpleText('Volets', font)
        label.setPos(710,8)
        label.setBrush(Qt.white)
        self.flap = self.scene.addPixmap(self.grayLed)
        self.flap.setPos(710,30)
        bold = QFont('Arial', 15, QFont.Bold)
        self.flaps = self.scene.addSimpleText(' ', bold)
        self.flaps.setPos(722,37)
        self.flaps.setBrush(Qt.black)
                
        self.setSwitch({"batt":0})
        self.setSwitch({"inter":0})
        self.setSwitch({"mixt":0})
        self.setSwitch({"carbu":0})
        self.setSwitch({"pump":0})
        self.setSwitch({"flap":0})
   
    def setSwitch(self, data):
      
      if "batt" in data:
        value = data["batt"]
        if (value == 1): self.battery.setPixmap(self.greenLed)
        else: self.battery.setPixmap(self.grayLed)

      if "inter" in data:
        value = data["inter"]
        if (value == 1): self.altern.setPixmap(self.greenLed)
        else: self.altern.setPixmap(self.grayLed)

      if "mixt" in data:
        value = data["mixt"]
        if (value == 1): self.mixture.setPixmap(self.redLed)
        else: self.mixture.setPixmap(self.grayLed)

      if "carbu" in data:
        value = data["carbu"]
        if (value == 1): self.carbu.setPixmap(self.redLed)
        else: self.carbu.setPixmap(self.grayLed)

      if "pump" in data:
        value = data["pump"]
        if (value == 1): self.pump.setPixmap(self.greenLed)
        else: self.pump.setPixmap(self.grayLed)

      if "gear" in data:
        pass

      if "flap" in data:
        value = int(data["flap"] * 2)
        #print (value)
        if (value == 1):
          self.flap.setPixmap(self.yellowLed)
          self.flaps.setText('1')
        elif (value == 2):
          self.flap.setPixmap(self.redLed)
          self.flaps.setText('2')
        else:
          self.flap.setPixmap(self.grayLed)
          self.flaps.setText(' ')        


class lightPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,450,75)
        
        pixmap = QPixmap('/var/fspanel/images/switch-plate-2.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        font = QFont('Arial', 10, QFont.Light)
        
        self.grayLed = QPixmap('/var/fspanel/images/led-gray.png')
        self.whiteLed = QPixmap('/var/fspanel/images/led-white.png')
        self.greenLed = QPixmap('/var/fspanel/images/led-green.png')
        self.yellowLed = QPixmap('/var/fspanel/images/led-yellow.png')
        self.redLed = QPixmap('/var/fspanel/images/led-red.png')
        
        label = self.scene.addSimpleText('Nav', font)
        label.setPos(45,8)
        label.setBrush(Qt.white)
        self.nav = self.scene.addPixmap(self.grayLed)
        self.nav.setPos(40,30)
        
        label = self.scene.addSimpleText('Strobe', font)
        label.setPos(150,8)
        label.setBrush(Qt.white)
        self.strobe = self.scene.addPixmap(self.grayLed)
        self.strobe.setPos(150,30)
        
        label = self.scene.addSimpleText('Landing', font)
        label.setPos(255,8)
        label.setBrush(Qt.white)
        self.land = self.scene.addPixmap(self.grayLed)
        self.land.setPos(260,30)
        
        label = self.scene.addSimpleText('Taxi', font)
        label.setPos(375,8)
        label.setBrush(Qt.white)
        self.taxi = self.scene.addPixmap(self.grayLed)
        self.taxi.setPos(370,30)
        
        self.setLight({"nav":0})
        self.setLight({"strobe":0})
        self.setLight({"land":0})
        self.setLight({"taxi":0})
   
    def setLight(self, data):
      
      if "nav" in data:
        value = data["nav"]
        if (value == 1): self.nav.setPixmap(self.whiteLed)
        else: self.nav.setPixmap(self.grayLed)
        
      if "strobe" in data:
        value = data["strobe"]
        if (value == 1): self.strobe.setPixmap(self.whiteLed)
        else: self.strobe.setPixmap(self.grayLed)
        
      if "land" in data:
        value = data["land"]
        if (value == 1): self.land.setPixmap(self.whiteLed)
        else: self.land.setPixmap(self.grayLed)

      if "taxi" in data:
        value = data["taxi"]
        if (value == 1): self.taxi.setPixmap(self.whiteLed)
        else: self.taxi.setPixmap(self.grayLed)
        

class radioPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0,0,505,425)
        self.setTransform(QTransform().scale(0.75, 0.75), True)

        pixmap = QPixmap('/var/fspanel/images/radio-back.png')
        self.panel = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/radio-plate.png')
        self.panel = self.scene.addPixmap(pixmap)
        self.panel.setPos(5,25)
        
        self.red = []
        self.red.append(QPixmap('/var/fspanel/images/digit-red-0.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-1.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-2.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-3.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-4.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-5.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-6.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-7.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-8.png'))
        self.red.append(QPixmap('/var/fspanel/images/digit-red-9.png'))

        self.white = []
        self.white.append(QPixmap('/var/fspanel/images/digit-white-0.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-1.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-2.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-3.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-4.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-5.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-6.png'))
        self.white.append(QPixmap('/var/fspanel/images/digit-white-7.png'))

        font = QFont('Arial', 12, QFont.Light)
        label = self.scene.addSimpleText('COM', font)
        label.setPos(40,25)
        label.setBrush(Qt.white)

        self.comfreq1 = self.scene.addPixmap(self.red[0])
        self.comfreq1.setPos(55,65)
        self.comfreq2 = self.scene.addPixmap(self.red[0])
        self.comfreq2.setPos(90,65)
        self.comfreq3 = self.scene.addPixmap(self.red[0])
        self.comfreq3.setPos(125,65)
        self.comfreq4 = self.scene.addPixmap(self.red[0])
        self.comfreq4.setPos(170,65)
        self.comfreq5 = self.scene.addPixmap(self.red[0])
        self.comfreq5.setPos(205,65)
        
        self.comstby1 = self.scene.addPixmap(self.red[0])
        self.comstby1.setPos(265,65)
        self.comstby2 = self.scene.addPixmap(self.red[0])
        self.comstby2.setPos(300,65)
        self.comstby3 = self.scene.addPixmap(self.red[0])
        self.comstby3.setPos(335,65)
        self.comstby4 = self.scene.addPixmap(self.red[0])
        self.comstby4.setPos(380,65)
        self.comstby5 = self.scene.addPixmap(self.red[0])
        self.comstby5.setPos(415,65)
        
        font = QFont('Arial', 12, QFont.Light)
        label = self.scene.addSimpleText('NAV', font)
        label.setPos(40,150)
        label.setBrush(Qt.white)

        self.navfreq1 = self.scene.addPixmap(self.red[0])
        self.navfreq1.setPos(55,185)
        self.navfreq2 = self.scene.addPixmap(self.red[0])
        self.navfreq2.setPos(90,185)
        self.navfreq3 = self.scene.addPixmap(self.red[0])
        self.navfreq3.setPos(125,185)
        self.navfreq4 = self.scene.addPixmap(self.red[0])
        self.navfreq4.setPos(170,185)
        self.navfreq5 = self.scene.addPixmap(self.red[0])
        self.navfreq5.setPos(205,185)
        
        self.navstby1 = self.scene.addPixmap(self.red[0])
        self.navstby1.setPos(265,185)
        self.navstby2 = self.scene.addPixmap(self.red[0])
        self.navstby2.setPos(300,185)
        self.navstby3 = self.scene.addPixmap(self.red[0])
        self.navstby3.setPos(335,185)
        self.navstby4 = self.scene.addPixmap(self.red[0])
        self.navstby4.setPos(380,185)
        self.navstby5 = self.scene.addPixmap(self.red[0])
        self.navstby5.setPos(415,185)
        
        font = QFont('Arial', 12, QFont.Light)
        label = self.scene.addSimpleText('TRANSPONDEUR', font)
        label.setPos(40,275)
        label.setBrush(Qt.white)

        self.xpdr1 = self.scene.addPixmap(self.white[0])
        self.xpdr1.setPos(60,300)
        self.xpdr2 = self.scene.addPixmap(self.white[0])
        self.xpdr2.setPos(110,300)
        self.xpdr3 = self.scene.addPixmap(self.white[0])
        self.xpdr3.setPos(160,300)
        self.xpdr4 = self.scene.addPixmap(self.white[0])
        self.xpdr4.setPos(210,300)
        
        font = QFont('Arial', 9, QFont.Light)
        label = self.scene.addSimpleText('OFF', font)
        label.setPos(305,345)
        label.setBrush(Qt.white)
        label = self.scene.addSimpleText('STBY', font)
        label.setPos(310,315)
        label.setBrush(Qt.white)
        label = self.scene.addSimpleText('ON', font)
        label.setPos(355,300)
        label.setBrush(Qt.white)
        label = self.scene.addSimpleText('ALT', font)
        label.setPos(395,315)
        label.setBrush(Qt.white)
        label = self.scene.addSimpleText('TEST', font)
        label.setPos(405,345)
        label.setBrush(Qt.white)

        pixmap = QPixmap('/var/fspanel/images/radio-button.png')
        self.button = self.scene.addPixmap(pixmap)
        self.button.setPos(345,325)
        self.button.setTransformOriginPoint(QPoint(22,22))
        
        self.setCom({"active":0, "stby":0})
        self.setNav({"active":0, "stby":0})
        self.setXpdr({"mode":0, "sett":0})
        
    def setCom(self, value):
      
      if "active" in value:
        active = value["active"]
        sett = "%05d" % active
        n = int(sett[:1])
        self.comfreq1.setPixmap(self.red[n])
        n = int(sett[1:2])
        self.comfreq2.setPixmap(self.red[n])
        n = int(sett[2:3])
        self.comfreq3.setPixmap(self.red[n])
        n = int(sett[3:4])
        self.comfreq4.setPixmap(self.red[n])
        n = int(sett[4:5])
        self.comfreq5.setPixmap(self.red[n])

      if "stby" in value:
        stby = value["stby"]
        sett = "%05d" % stby
        n = int(sett[:1])
        self.comstby1.setPixmap(self.red[n])
        n = int(sett[1:2])
        self.comstby2.setPixmap(self.red[n])
        n = int(sett[2:3])
        self.comstby3.setPixmap(self.red[n])
        n = int(sett[3:4])
        self.comstby4.setPixmap(self.red[n])
        n = int(sett[4:5])
        self.comstby5.setPixmap(self.red[n])


    def setNav(self, value):
      if "active" in value:
        active = value["active"]
        sett = "%05d" % active
        n = int(sett[:1])
        self.navfreq1.setPixmap(self.red[n])
        n = int(sett[1:2])
        self.navfreq2.setPixmap(self.red[n])
        n = int(sett[2:3])
        self.navfreq3.setPixmap(self.red[n])
        n = int(sett[3:4])
        self.navfreq4.setPixmap(self.red[n])
        n = int(sett[4:5])
        self.navfreq5.setPixmap(self.red[n])

      if "stby" in value:
        stby = value["stby"]
        sett = "%05d" % stby
        n = int(sett[:1])
        self.navstby1.setPixmap(self.red[n])
        n = int(sett[1:2])
        self.navstby2.setPixmap(self.red[n])
        n = int(sett[2:3])
        self.navstby3.setPixmap(self.red[n])
        n = int(sett[3:4])
        self.navstby4.setPixmap(self.red[n])
        n = int(sett[4:5])
        self.navstby5.setPixmap(self.red[n])


    def setXpdr(self, value):
      if "sett" in value:
        sett = value["sett"]
        sett = "{:04d}".format(sett)
        n = int(sett[:1])
        self.xpdr1.setPixmap(self.white[n])
        n = int(sett[1:2])
        self.xpdr2.setPixmap(self.white[n])
        n = int(sett[2:3])
        self.xpdr3.setPixmap(self.white[n])
        n = int(sett[3:4])
        self.xpdr4.setPixmap(self.white[n])

      if "mode" in value:
        mode = value["mode"]
        self.button.setRotation(mode *45)


class identPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.scene.setSceneRect(0, 0, 375, 75)
        #self.setTransform(QTransform().scale(0.75, 0.75), True)

        pixmap = QPixmap('/var/fspanel/images/ident-plate.png')
        self.panel = self.scene.addPixmap(pixmap)
        
        font = QFont('Verdana', 20, QFont.Light)
        self.modele = self.scene.addSimpleText('', font)
        self.modele.setPos(35,15)
        self.modele.setBrush(Qt.white)
       
        font = QFont('Verdana', 26, QFont.Bold)
        self.indicatif = self.scene.addSimpleText('', font)
        self.indicatif.setPos(185,10)
        self.indicatif.setBrush(Qt.white)
        
    def initialize(self, data):

        self.modele.setText('{:>3}'.format(data['modele']))
        self.indicatif.setText('{:>3}'.format(data['indicatif']))
        
