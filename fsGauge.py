#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtGui import QImage, QPixmap, QTransform, QFont, QBrush, QPen, QPainter, QPainterPath

class QGaugeView(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        self.param = {}
        
        self.scene = QGraphicsScene()

        self.setScene(self.scene)
        self.setStyleSheet("border: 0px; background: transparent;")

    def initialize(self, data):

        self.param = {}   
        self.scene.clear()
        
        for key in data:

          value = data[key]['value']

          self.param[key] = {}
          self.param[key]['value'] = value

          self.setValue({key:value})

    def getValue(self, key):
      
      if key in self.param:
        return self.param[key]['value']

    def setValue(self, data):

      for key in data:

        if key in self.param:

          value = data[key]
          self.param[key]['value'] = value


class airspeedGauge(QGaugeView):
  
    def initialize(self, data):
      
        self.param = {}   
        self.scene.clear()
        
        self.scene.setSceneRect(0,0,300,300)
        if 'scale' in data:
          scale = data['scale']['value']
        else:
          scale = 0.85
        self.setTransform(QTransform().scale(scale, scale), False)

        self.setRenderHint(QPainter.Antialiasing, True)
        
        pixmap = QPixmap('/var/fspanel/images/speed-plate.png')
        self.scene.addPixmap(pixmap)
        
        self.zeroAngle = -180
        
        key = 'speed'
        
        value = data[key]['value']
        self.param[key] = {}
        self.param[key]['value'] = value

        vs0 = data[key]['vs0']
        vs1 = data[key]['vs1']
        vfe = data[key]['vfe']
        vno = data[key]['vno']
        vne = data[key]['vne']
        self.maxspeed = data[key]['max']
        
        delta = 300 / (self.maxspeed - 50)
        
        path = QPainterPath()
        pen = QPen(Qt.white, 12, Qt.SolidLine)
        a1 = 270 - ((vfe - 50) * delta + 30)
        a2 = (vfe - vs0) * delta
        path.arcMoveTo(40, 40, 220, 220, a1)
        path.arcTo(40, 40, 220, 220, a1, a2)      
        self.scene.addPath(path, pen)
        
        path = QPainterPath()
        pen = QPen(Qt.green, 10, Qt.SolidLine)
        a1 = 270 - ((vno - 50) * delta + 30)
        a2 = (vno - vs1) * delta
        path.arcMoveTo(50, 50, 200, 200, a1)
        path.arcTo(50, 50, 200, 200, a1, a2)
        self.scene.addPath(path, pen)
      
        path = QPainterPath()
        pen = QPen(Qt.yellow, 10, Qt.SolidLine)
        a1 = 270 - ((vne - 50) * delta + 30)
        a2 = (vne - vno) * delta
        path.arcMoveTo(50, 50, 200, 200, a1)
        path.arcTo(50, 50, 200, 200, a1, a2)
        self.scene.addPath(path, pen)
        
        for a in range(50, self.maxspeed + 1, 10):

            alpha = self.zeroAngle + 30 + (a - 50) * delta
            dx = math.cos(math.radians(alpha - 90))
            dy = math.sin(math.radians(alpha - 90))

            if (a % 50 == 0):
              R = 75
              font = QFont('Verdana', 12, QFont.Light)
              text = self.scene.addSimpleText(str(a), font)
              text.setPos(135 + 50 * dx, 140 + 50 * dy)
              text.setBrush(Qt.white)
            else:
              R = 90
              
            if (a == vne):
              R = 75
              pen = QPen(Qt.red, 3, Qt.SolidLine)
            else:
              pen = QPen(Qt.white, 3, Qt.SolidLine)

            path = QPainterPath()
            path.moveTo(150 + 110 * dx, 150 + 110 * dy)
            path.lineTo(150 + R * dx, 150 + R * dy)
            self.scene.addPath(path, pen)
            
        pixmap = QPixmap('/var/fspanel/images/speed-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        font = QFont('Arial', 14, QFont.Light)
        self.speed = self.scene.addSimpleText('0', font)
        self.speed.setPos(135,230)
        self.speed.setBrush(Qt.yellow)
        
        self.setValue({key:value})

    def setValue(self, data):
      
      if "speed" in data:
	
        value = data["speed"]
        speed = int(value * 1.852)
        delta = 300 / (self.maxspeed - 50)
        if (speed < 50): angle = 0
        elif (speed <= self.maxspeed): angle = 30 + (speed - 50) * delta
        else: angle = 300
        
        self.needle.setRotation(self.zeroAngle + angle)
        self.speed.setText('{:>3}'.format(speed))

        self.param['speed']['value'] = speed


class accelerometerGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()
        
        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

        self.setRenderHint(QPainter.Antialiasing, True)
        
        self.zeroAngle = -90

        key = 'load'
        
        value = data[key]['value']
        self.param[key] = {}
        self.param[key]['value'] = value

        pixmap = QPixmap('/var/fspanel/images/g-unit-plate.png')
        self.scene.addPixmap(pixmap)
        
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
          dx = math.cos(math.radians(alpha - 90))
          dy = math.sin(math.radians(alpha - 90))
            
          if (a % 2 == 0):
            R = 75
            X = R * math.cos(math.radians(alpha - 90))
            Y = R * math.sin(math.radians(alpha - 90))
            font = QFont('Verdana', 12, QFont.Light)
            text = self.scene.addSimpleText(str(abs(g)), font)
            text.setPos(145 + R * dx, 142 + R * dy)
            text.setBrush(Qt.gray)
            g = g - 1
            	    
          path = QPainterPath()
          path.moveTo(150 + 110 * dx, 150 + 110 * dy)
          path.lineTo(150 + 90 * dx, 150 + 90 * dy)
          if (a % 2 == 0):
            pen = QPen(Qt.gray, 3, Qt.SolidLine)
          else:
            pen = QPen(Qt.white, 3, Qt.SolidLine)
          self.scene.addPath(path, pen)
        
        pixmap = QPixmap('/var/fspanel/images/speed-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        self.setValue({key:value})
        
    def setValue(self, data):
      
        if "load" in data:
	  
          load = data["load"]
          angle = load * 20
          
          self.needle.setRotation(self.zeroAngle + angle)
          
          self.param['load']['value'] = load

      
class manifoldGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()
        
        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

        self.setRenderHint(QPainter.Antialiasing, True)
        
        pixmap = QPixmap('/var/fspanel/images/speed-plate.png')
        self.gauge = self.scene.addPixmap(pixmap)
        
        for a in range(10, 36, 1):

            alpha = -175 + (a - 10) * 170 / 25
            dx = math.cos(math.radians(alpha - 90))
            dy = math.sin(math.radians(alpha - 90))

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
            path.moveTo(150 + 110 * dx, 150 + 110 * dy)
            path.lineTo(150 + R * dx, 150 + R * dy)
            self.scene.addPath(path, pen)
            
        for a in range(3, 19, 1):

            alpha = 175 - a * a / 2
            dx = math.cos(math.radians(alpha - 90))
            dy = math.sin(math.radians(alpha - 90))

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
            path.moveTo(150 + 110 * dx, 150 + 110 * dy)
            path.lineTo(150 + R * dx, 150 + R * dy)
            self.scene.addPath(path, pen)
            
        pixmap = QPixmap('/var/fspanel/images/speed-dial.png')
        self.pressure = self.scene.addPixmap(pixmap)
        self.pressure.setTransformOriginPoint(QPoint(150,150))
        self.fuelflow = self.scene.addPixmap(pixmap)
        self.fuelflow.setTransformOriginPoint(QPoint(150,150))
      
        for key in data:

          value = data[key]['value']

          self.param[key] = {}
          self.param[key]['value'] = value

          self.setValue({key:value})
        
    def setValue(self, data):
      
        if "man" in data:
          man = data["man"]
          if (man < 10): man = 10
          angle = -175 + (man - 10) * 170 / 25
          if (angle > -5): angle = -5
          self.pressure.setRotation(angle)
          self.param['man']['value'] = man
        
        if "flow" in data:
          flow = data["flow"]          
          angle = 175 - flow * flow / 2
          if (angle < 5): angle = 5
          self.fuelflow.setRotation(angle)
          self.param['flow']['value'] = flow

      
class attitudeGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()
        
        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

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
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "pitch" in data:
        pitch = data["pitch"]
        self.disc.setTransform(QTransform().translate(0, pitch * 1.5), False)
        self.param['pitch']['value'] = pitch

      if "roll" in data:
        roll = data["roll"]
        self.gear.setRotation(-roll)
        self.disc.setRotation(-roll)
        self.param['roll']['value'] = roll


class altitudeGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

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
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "alt" in data:
        altitude = data["alt"]
        self.needle100.setRotation((360 / 1000) * altitude)
        self.needle1000.setRotation((360 / 10000) * altitude)
        self.needle10000.setRotation((360 / 100000) * altitude)
        if (altitude > 10000): hatch = False
        else: hatch = True
        self.hatch.setVisible(hatch)
        self.param['alt']['value'] = altitude

      if "baro" in data:
        baro = int(data["baro"] * 33.863886)
        #self.baro.setText('%5s' % baro)
        self.baro.setText('{:>4}'.format(baro))
        self.param['baro']['value'] = baro

class turnslipGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)
        
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
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "slip" in data:
        slip = data["slip"]
        dx = int(slip * 12)
        self.ball.setTransform(QTransform().translate(-dx, 0), False)
        self.param['slip']['value'] = slip

      if "turn" in data:
        turn = data["turn"]
        if (turn <= -35): turn = -35
        elif (turn >= 35): turn = 35
        self.plane.setRotation(turn)
        self.param['turn']['value'] = turn


class dgGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

        pixmap = QPixmap('/var/fspanel/images/dg-disc.png')
        self.disc = self.scene.addPixmap(pixmap)
        self.disc.setTransformOriginPoint(QPoint(150,150))

        pixmap = QPixmap('/var/fspanel/images/dg-gear.png')
        self.gear = self.scene.addPixmap(pixmap)
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "cap" in data:
        cap = data["cap"]
        
        self.disc.setRotation(-cap)
        self.param['cap']['value'] = cap


class varioGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

        pixmap = QPixmap('/var/fspanel/images/verticalspeed.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/verticalspeed-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        self.zeroAngle = -90
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "vvi" in data:
        vvi = data["vvi"]
        
        if (vvi >= -500 and vvi <= 500):
          angle = int((vvi / 500) * 35)
        elif (vvi >= -1000 and vvi < 0):
          angle = int(((vvi + 500) / 500) * 46) - 35
        elif (vvi > 0 and vvi <= 1000):
          angle = int(((vvi - 500) / 500) * 46) + 35
        elif (vvi < 0):
          angle = int(((vvi + 1000)  / 2000) * 98) - 81
        else:
          angle = int(((vvi - 1000)  / 2000) * 98) + 81
          
        if (angle < -180): angle = -180
        elif (angle > 180): angle = 180
        
        self.needle.setRotation(self.zeroAngle + angle)
        self.param['vvi']['value'] = vvi


class vorGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

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
        
        font = QFont('Arial', 12, QFont.Light)
        self.dme = self.scene.addSimpleText('0', font)
        self.dme.setPos(90,175)
        self.dme.setBrush(Qt.yellow)
        
        pixmap = QPixmap('/var/fspanel/images/vor-glide.png')
        self.glide = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/vor-slope.png')
        self.needle = self.scene.addPixmap(pixmap)
        
        #self.setValue({"obs":0, "tofr":1, "dme": 0, "hdef":0, "vdef":0})
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
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

      if "dme" in value:
        dme = value["dme"]
        self.dme.setText('{:>3}'.format(dme))

      if "hdef" in value:
        hdef = value["hdef"]
        dx = int(hdef * 30)
        self.needle.setTransform(QTransform().translate(dx, 0), False)

      if "vdef" in value:
        vdef = value["vdef"]
        dy = int(vdef * 30)
        self.glide.setTransform(QTransform().translate(0, dy), False)



class adfGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

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
        
        #pixmap = QPixmap('/var/fspanel/images/adf-hdg.png')
        pixmap = QPixmap('/var/fspanel/images/adf-brg.png')
        self.brg = self.scene.addPixmap(pixmap)
        self.brg.setTransformOriginPoint(QPoint(150,150))
        
        pixmap = QPixmap('/var/fspanel/images/adf-airplane.png')
        self.airplane = self.scene.addPixmap(pixmap)
        
        font = QFont('Arial', 11, QFont.Light)
        self.freq = self.scene.addSimpleText('0', font)
        self.freq.setPos(135,195)
        self.freq.setBrush(Qt.white)
        
        #self.setValue({"frq":0, "card":0, "brg":0}) 
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, value):
      
      if "card" in value:
        card = value["card"]
        self.disc.setRotation(-card)

      if "brg" in value:
        #pass
        brg = value["brg"]
        #self.hdg.setRotation(hdg)
        self.brg.setRotation(brg)

      if "frq" in value:
        frq = value["frq"]
        self.freq.setText('{:>04}'.format(frq))



class engineGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()
        
        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.85, 0.85), False)

        pixmap = QPixmap('/var/fspanel/images/enginerpm.png')
        self.scene.addPixmap(pixmap)

        font = QFont('Arial', 14, QFont.Light)
        self.speed = self.scene.addSimpleText('0', font)
        self.speed.setPos(130,230)
        self.speed.setBrush(Qt.yellow)
        
        pixmap = QPixmap('/var/fspanel/images/enginerpm-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(150,150))
        
        self.zeroAngle = -123

        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
          
    def setValue(self, data):
      
      if "rpm" in data:

        rpm = data["rpm"]
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
        self.speed.setText('{:>3}'.format(rpm))
        self.param['rpm']['value'] = rpm


class vacuumGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,200,200)
        self.setTransform(QTransform().scale(0.9, 0.9), False)
 
        pixmap = QPixmap('/var/fspanel/images/vacuum-back.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/vacuum-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(100,100))
        
        self.zeroAngle = -90
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      if "vacuum" in data:
        vacuum = int(data["vacuum"] * 5)
        angle = vacuum * 18
        if (angle <= 0):
           angle = 0
        elif (angle >= 180):
           angle = 180
        self.needle.setRotation(self.zeroAngle + angle)
        self.param['vacuum']['value'] = vacuum


class fuelGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,200,200)
        self.setTransform(QTransform().scale(0.9, 0.9), False)
        
        pixmap = QPixmap('/var/fspanel/images/fuel-gear.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/fuel-dial.png')
        self.needle = self.scene.addPixmap(pixmap)
        self.needle.setTransformOriginPoint(QPoint(104,125))
        
        pixmap = QPixmap('/var/fspanel/images/fuel-glass.png')
        self.glass = self.scene.addPixmap(pixmap)

        self.zeroAngle = -60
        self.max = 115
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "fuel" in data:
        fuel = int((data["fuel"] * 0.4536) / 0.721)
        angle = int((fuel  / self.max) * 120)
        if (angle <= 0):
           angle = 0
        elif (angle >= 100):
           angle = 100
        self.needle.setRotation(self.zeroAngle + angle)
        self.param['fuel']['value'] = fuel


class oilGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,200,200)
        #self.setTransform(QTransform().scale(0.9, 0.9), False)
        
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
              
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.param[key]['max'] = data[key]['max']
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "temp" in data:
        temp = data["temp"]
        self.param['temp']['value'] = temp
        if (temp < 0):
           temp = 0
        elif (temp > self.param['temp']['max']):
           temp = self.param['temp']['max']
        angle = int((temp / self.param['temp']['max']) * 100)
        self.temp.setRotation(50 - angle)
        
      if "psi" in data:
        psi = data["psi"]
        self.param['psi']['value'] = psi
        if (psi < 0):
           psi = 0
        elif (psi > self.param['psi']['max']):
           psi = self.param['psi']['max']
        angle = int((psi / self.param['psi']['max']) * 100)
        self.psi.setRotation(angle - 50)


class trimGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,150,275)
        
        pixmap = QPixmap('/var/fspanel/images/trim.png')
        self.trim = self.scene.addPixmap(pixmap)
        
        pixmap = QPixmap('/var/fspanel/images/trim-handle.png')
        self.handle = self.scene.addPixmap(pixmap)
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "pitch" in data:
        pitch = data["pitch"]
        dy = int(pitch * 100)
        if (dy < -100): dy = -100
        elif (dy > 100): dy = 100
        self.handle.setTransform(QTransform().translate(0, dy), False)
        self.param['pitch']['value'] = pitch

      if "yaw" in data:
        pass


class switchPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)

        self.led = {}
        '''
        self.led['gray'] = QPixmap('/var/fspanel/images/led-gray.png')
        self.led['white'] = QPixmap('/var/fspanel/images/led-white.png')
        self.led['yellow'] = QPixmap('/var/fspanel/images/led-yellow.png')
        self.led['red'] = QPixmap('/var/fspanel/images/led-red.png')
        self.led['green'] = QPixmap('/var/fspanel/images/led-green.png')
        '''
        self.led['gray'] = QPixmap('/var/fspanel/images/warn-gray.png')
        self.led['white'] = QPixmap('/var/fspanel/images/warn-white.png')
        self.led['yellow'] = QPixmap('/var/fspanel/images/warn-yellow.png')
        self.led['red'] = QPixmap('/var/fspanel/images/warn-red.png')
        self.led['green'] = QPixmap('/var/fspanel/images/warn-green.png')
        self.led['blue'] = QPixmap('/var/fspanel/images/warn-blue.png')
        
    def initialize(self, data):
      
      self.param = {}   
      self.scene.clear()
        
      self.scene.setSceneRect(0,0,800,75)
        
      pixmap = QPixmap('/var/fspanel/images/switch-plate-1.png')
      self.gauge = self.scene.addPixmap(pixmap)
        
      font = QFont('Arial', 10, QFont.Light)
      bold = QFont('Arial', 15, QFont.Bold)
      
      for key in data:
  
        pos = data[key]['pos']
        
        self.param[key] = {}
        
        if (key == 'fps'):
          self.param[key]['text'] = self.scene.addSimpleText('', font)
          self.param[key]['text'].setPos(55+110*pos,50)
          self.param[key]['value'] = data[key]['value']
          continue

        self.param[key]['label'] = data[key]['label']
        self.param[key]['led'] = data[key]['led']
        self.param[key]['value'] = data[key]['value']

        label = self.scene.addSimpleText(self.param[key]['label'], font)
        x = 72 + 110 * pos - int(label.boundingRect().width() / 2)
        label.setPos(x,8)
        label.setBrush(Qt.white)
          
        self.param[key]['item'] = self.scene.addPixmap(self.led['gray'])
        self.param[key]['item'].setPos(55+110*pos,30)
        
        if ('text' in data[key]):
          self.param[key]['text'] = self.scene.addSimpleText(data[key]['text'], bold)
          self.param[key]['text'].setPos(67+110*pos,37)
          self.param[key]['text'].setBrush(Qt.black)

        self.setValue({key: data[key]['value']})

    def setValue(self, data):
      
      for key in data:
        
        if key in self.param:

          value = data[key]
          
          if ('item' in self.param[key]):
            item = self.param[key]['item']
            led = self.param[key]['led']
            
          if (key == 'fps'):

            self.param[key]['text'].setText(str(value))
            if (value < 10):
              self.param[key]['text'].setBrush(Qt.red)
            elif (value < 20):
              self.param[key]['text'].setBrush(Qt.yellow)
            elif (value < 30):
              self.param[key]['text'].setBrush(Qt.gray)
            else:
              self.param[key]['text'].setBrush(Qt.green)
              
          elif (key == 'flap'):

            if (value != self.param[key]['value']):
              delta = self.param[key]['value'] - value
              number = round(1 / abs(delta))
              if (value == 0):
                item.setPixmap(self.led['gray'])
                self.param[key]['text'].setText(' ')        
              elif (value == 1):
                item.setPixmap(self.led['red'])
                self.param[key]['text'].setText(str(number))
              else:
                item.setPixmap(self.led['yellow'])
                self.param[key]['text'].setText(str(round(number*value)))
              
          else:

            if (value == 1): item.setPixmap(self.led[led])
            else: item.setPixmap(self.led['gray'])

          self.param[key]['value'] = value
      
class lightPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)
        
        self.led = {}
        '''
        self.led['gray'] = QPixmap('/var/fspanel/images/led-gray.png')
        self.led['white'] = QPixmap('/var/fspanel/images/led-white.png')
        self.led['yellow'] = QPixmap('/var/fspanel/images/led-yellow.png')
        self.led['red'] = QPixmap('/var/fspanel/images/led-red.png')
        self.led['green'] = QPixmap('/var/fspanel/images/led-green.png')
        '''
        self.led['gray'] = QPixmap('/var/fspanel/images/warn-gray.png')
        self.led['white'] = QPixmap('/var/fspanel/images/warn-white.png')
        self.led['yellow'] = QPixmap('/var/fspanel/images/warn-yellow.png')
        self.led['red'] = QPixmap('/var/fspanel/images/warn-red.png')
        self.led['green'] = QPixmap('/var/fspanel/images/warn-green.png')
        self.led['blue'] = QPixmap('/var/fspanel/images/warn-blue.png')
        
    def initialize(self, data):
      
      self.param = {}   
      self.scene.clear()
        
      self.scene.setSceneRect(0,0,450,75)

      pixmap = QPixmap('/var/fspanel/images/switch-plate-2.png')
      self.gauge = self.scene.addPixmap(pixmap)
        
      font = QFont('Arial', 10, QFont.Light)
        
      for key in data:
  
        pos = data[key]['pos']
          
        self.param[key] = {}
        self.param[key]['label'] = data[key]['label']
        self.param[key]['led'] = data[key]['led']
        self.param[key]['value'] = data[key]['value']

        label = self.scene.addSimpleText(self.param[key]['label'], font)
        x = 57 + 110 * pos - int(label.boundingRect().width() / 2)
        label.setPos(x,8)
        label.setBrush(Qt.white)
          
        self.param[key]['item'] = self.scene.addPixmap(self.led['gray'])
        self.param[key]['item'].setPos(40+110*pos,30)
        
        self.setValue({key: data[key]['value']})

    def setValue(self, data):
      
      for key in data:
        
        if key in self.param:
	  
          item = self.param[key]['item']
          led = self.param[key]['led']
          value = data[key]
          self.param[key]['value'] = value
        
          if (value == 1): item.setPixmap(self.led[led])
          else: item.setPixmap(self.led['gray'])


class warnPanel(QGaugeView):
  
    def __init__(self):
        QGaugeView.__init__(self)
        
        self.led = {}
        self.led['gray'] = QPixmap('/var/fspanel/images/warn-gray.png')
        self.led['white'] = QPixmap('/var/fspanel/images/warn-white.png')
        self.led['yellow'] = QPixmap('/var/fspanel/images/warn-yellow.png')
        self.led['red'] = QPixmap('/var/fspanel/images/warn-red.png')
        self.led['green'] = QPixmap('/var/fspanel/images/warn-green.png')
        self.led['blue'] = QPixmap('/var/fspanel/images/warn-blue.png')
        
    def initialize(self, data):
      
      self.param = {}
      self.scene.clear()
        
      self.scene.setSceneRect(0,0,850,75)

      pixmap = QPixmap('/var/fspanel/images/warn-plate-2.png')
      self.scene.addPixmap(pixmap)
        
      font = QFont('Arial', 10, QFont.Light)
      bold = QFont('Arial', 15, QFont.Bold)
              
      self.battery = 0
      
      for key in data:
  
        pos = data[key]['pos']
          
        self.param[key] = {}
        self.param[key]['label'] = data[key]['label']
        self.param[key]['led'] = data[key]['led']
        self.param[key]['value'] = data[key]['value']

        label = self.scene.addSimpleText(self.param[key]['label'], font)
        #x = 57 + 110 * pos - int(label.boundingRect().width() / 2)
        label.setPos(95+110*pos,30)
        label.setBrush(Qt.gray)
        
        self.param[key]['item'] = self.scene.addPixmap(self.led['gray'])
        self.param[key]['item'].setPos(55+110*pos,20)
        
        if ('text' in data[key]):
          self.param[key]['text'] = self.scene.addSimpleText(data[key]['text'], bold)
          self.param[key]['text'].setPos(67+110*pos,27)
          self.param[key]['text'].setBrush(Qt.black)

        self.setValue({key: data[key]['value']})
      
    def setValue(self, data):
      
      if 'battery' in data:
        
        self.battery = data['battery']
        del data['battery']
        
      for key in data:
        
        if key in self.param:
  
          item = self.param[key]['item']
          led = self.param[key]['led']
          value = data[key]
        
          if self.battery:

            if (key == 'oil'):
              if (value < 5): item.setPixmap(self.led[led])
              else: item.setPixmap(self.led['gray'])
              
            elif (key == 'fuel'):
              if (value < 5): item.setPixmap(self.led[led])
              else: item.setPixmap(self.led['gray'])

            elif (key == 'flap'):

              if (value != self.param[key]['value']):
                delta = self.param[key]['value'] - value
                number = round(1 / abs(delta))
                if (value == 0):
                  item.setPixmap(self.led['gray'])
                  self.param[key]['text'].setText(' ')        
                elif (value == 1):
                  item.setPixmap(self.led['green'])
                  self.param[key]['text'].setText(str(number))
                  #self.param[key]['text'].setBrush(Qt.white)
                else:
                  item.setPixmap(self.led['yellow'])
                  self.param[key]['text'].setText(str(round(number*value)))
                  #self.param[key]['text'].setBrush(Qt.black)
              
            else:
    
              if (value == 1): item.setPixmap(self.led[led])
              else: item.setPixmap(self.led['gray'])

          else:
            item.setPixmap(self.led['gray'])
            
          self.param[key]['value'] = value
        

class radioPanel(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,505,425)
        self.setTransform(QTransform().scale(0.75, 0.75), False)

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
        self.button.setRotation(mode * 45)


class identPanel(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0, 0, 375, 75)
        #self.setTransform(QTransform().scale(0.75, 0.75), False)

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
        
        self.modele.setText('{:>3}'.format(data['ident']['modele']))
        self.indicatif.setText('{:>3}'.format(data['ident']['indicatif']))
        
        
class magnetoGauge(QGaugeView):
  
    def initialize(self, data):

        self.param = {}   
        self.scene.clear()

        self.scene.setSceneRect(0,0,300,300)
        self.setTransform(QTransform().scale(0.4, 0.4), False)
        
        pixmap = QPixmap('/var/fspanel/images/magneto-plate.png')
        self.gauge = self.scene.addPixmap(pixmap)

        pixmap = QPixmap('/var/fspanel/images/magneto-key.png')
        self.key = self.scene.addPixmap(pixmap)
        self.key.setTransformOriginPoint(QPoint(150,150))
        
        for key in data:
          value = data[key]['value']
          self.param[key] = {}
          self.param[key]['value'] = value
          self.setValue({key:value})
        
    def setValue(self, data):
      
      if "mag" in data:
        mag = data["mag"]
        angle = mag * 35
        self.key.setRotation(angle)
        self.param['mag']['value'] = mag

