#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import json, string, math, socket, select
from struct import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from fsEncoder import *


XPVER = "1.0"
UDP_PORT = 49003
UDP_SENDTO_PORT = 49000
UDP_SENDTO_IP = "192.168.1.10"

'''
class fsWorker(QObject):
    layout = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
      super().__init__()
      
    @pyqtSlot()
    def run(self):
       self.running = True
       print ('fsWorker running')
       
       while self.running:
          value = input("> ")
          if (value != ''):
             self.layout.emit(int(value))
             
'''

class fsSocket(QObject):

    airspeed = pyqtSignal([dict])	# speed
    attitude = pyqtSignal([dict])	# pitch, roll
    altitude = pyqtSignal([dict])	# alt, baro
    turnslip = pyqtSignal([dict])	# turn, slip
    dg = pyqtSignal([dict])		# cap
    vario = pyqtSignal([dict])		# vvi
    load = pyqtSignal([dict])		# load
    vor = pyqtSignal([dict])		# obs, tofr, dme, hdef, vdef
    adf = pyqtSignal([dict])		# frq, card, brg
    engine = pyqtSignal([dict])		# rpm
    radio = pyqtSignal([dict])		# com.active, com.stby, nav.active, nav.stby, xpdr.mode, xpdr.code
    oil = pyqtSignal([dict])		# temp, pres
    vacuum = pyqtSignal([dict])		# vac
    flow = pyqtSignal([dict])		# man, flow
    fuel = pyqtSignal([dict])		# fuel
    switch = pyqtSignal([dict])		# batt, inter, mixt, pump, carb, gear, flap
    warn = pyqtSignal([dict])		# battery, gene, oil, fuel, flap, brake, gear, stall
    trim = pyqtSignal([dict])		# trim
    light = pyqtSignal([dict])		# nav, strobe, land, taxi
    propeller = pyqtSignal([dict])	# prop
    magneto = pyqtSignal([dict])	# magneto

    panel = pyqtSignal([int])
    debug = pyqtSignal([str,str])
    
    finished = pyqtSignal()
    
    dataref = {}
    

    def __init__(self):
      super().__init__()
      
      self.gauge = { 
         "airspeed": { "signal": self.airspeed, "speed": { "code": 3, "index": 0, "data": 0 } },
         "attitude": { "signal": self.attitude, "pitch": { "code": 17, "index": 0, "data": 0 }, "roll": { "code": 17, "index": 1, "data": 0 } },
         # lat 0 / lon 1 / alt QNH 2 / alt QFE 3 / alt ind 5 / 
         "altitude": { "signal": self.altitude, "alt": { "code": 20, "index": 5, "data": 0 }, "baro": { "code": 7, "index": 0, "data": 0, "float": 0 } },
         "turnslip": { "signal": self.turnslip, "turn": { "code": 17, "index": 1, "data": 0 }, "slip": { "code": 18, "index": 7, "data": 0, "float": 0 } },
         "dg": { "signal": self.dg, "cap": { "code": 17, "index": 3, "data": 0 } },
         "vario": { "signal": self.vario, "vvi": { "code": 4, "index": 2, "data": 0 } },
         "load": { "signal": self.load, "load": { "code": 4, "index": 4, "data": 0, "float": 0 } },
         "vor": { "signal": self.vor, "obs": { "code": 98, "index": 0, "data": 0 }, "tofr": { "code": 99, "index": 1, "data": 0 }, "dme": { "code": 99, "index": 4, "data": 0, "float": 0 }, "hdef": { "code": 99, "index": 5, "data": 0, "float": 0 }, "vdef": { "code": 99, "index": 6, "data": 0, "float": 0 } },
         "adf": { "signal": self.adf, "frq": { "code": 101, "index": 0, "data": 0 }, "card": { "code": 101, "index": 1, "data": 0 }, "brg": { "code": 101, "index": 2, "data": 0 } },
         "engine": { "signal": self.engine, "rpm": { "code": 37, "index": 0, "data": 0 } },
         "radio": { "signal": self.radio, "power": { "code": 57, "index": 0, "data": 0 }, "com.active": { "code": 96, "index": 0, "data": 0 }, "com.stby": { "code": 96, "index": 1, "data": 0 }, "nav.active": { "code": 97, "index": 0, "data": 0 }, "nav.stby": { "code": 97, "index": 1, "data": 0}, "xpdr.mode": { "code": 104, "index": 0, "data": 0 }, "xpdr.code": { "code": 104, "index": 1, "data": 0 } },
         "oil": { "signal": self.oil, "power": { "code": 57, "index": 0, "data": 0 }, "heat": { "code": 50, "index": 0, "data": 0, "float": 0 }, "psi": { "code": 49, "index": 0, "data": 0, "float": 0 } },
         "vacuum": { "signal": self.vacuum, "vacuum": { "code": 7, "index": 2, "data": 0 } },
         "flow": { "signal": self.flow, "man": { "code": 43, "index": 0, "data": 0, "float": 0 }, "flow": { "code": 45, "index": 0, "data": 0, "float": 0 } },
         "fuel": { "signal": self.fuel, "power": { "code": 57, "index": 0, "data": 0 }, "fuel": { "code": 63, "index": 2, "data": 0 } },
         "switch": { "signal": self.switch, "power": { "code": 57, "index": 0, "data": 0 }, "gene": { "code": 58, "index": 0, "data": 0 }, "mixt": { "code": 29, "index": 0, "data": 0 }, "pump": { "code": 55, "index": 0, "data": 0 }, "carbheat": { "code": 30, "index": 0, "data": 0 }, "fps": { "code": 0, "index": 0, "data": 0, "float": 0 } },
         "light": { "signal": self.light, "power": { "code": 57, "index": 0, "data": 0 }, "nav": { "code": 106, "index": 1, "data": 0 }, "strobe": { "code": 106, "index": 3, "data": 0 }, "landing": { "code": 106, "index": 4, "data": 0 }, "taxi": { "code": 106, "index": 5, "data": 0 }, "speedbrake": { "code": 13, "index": 6, "data": 0 } },
         "warn": { "signal": self.warn, "power": { "code": 57, "index": 0, "data": 0 }, "gene": { "code": 115, "index": 4, "data": 0 }, "oil": { "code": 49, "index": 0, "data": 0, "float": 0 }, "fuel": { "code": 51, "index": 0, "data": 0, "float": 0 }, "flap": { "code": 13, "index": 3, "data": 0, "float": 0 }, "brake": { "code": 14, "index": 1, "data": 0 }, "gear": { "code": 14, "index": 0, "data": 0 }, "stall": { "code": 127, "index": 6, "data": 0 } },
         "magneto": { "signal": self.magneto, "mag": { "code": 32, "index": 0, "data": 0 } },
         "trim": { "signal": self.trim, "pitch": { "code": 13, "index": 0, "data": 0, "float": 0 }, "yaw": { "code": 13, "index": 2, "data": 0, "float": 0 } },
         #"gear": { "signal": self.gear, "N": { "code": 67, "index": 0, "data": 0 }, "R": { "code": 67, "index": 1, "data": 0 }, "L": { "code": 67, "index": 2, "data": 0 } },
         #"propeller": { "signal": self.propeller, "prop": { "code": 28, "index": 0, "data": 0 } }
      }

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Create Datagram Socket (UDP)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make Socket Reusable
      #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # Make Socket Reusable
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow incoming broadcasts
      self.sock.setblocking(True)                                      # Set socket to non-blocking mode (does not work: error)
      self.sock.bind(('', UDP_PORT))

      sel = bytes("DSEL0", "utf-8")
      code = [0,3,4,7,13,14,17,18,20,29,30,32,37,43,45,49,50,51,55,57,58,63,96,97,98,99,101,104,106,115,127]
      data_selection_packet = pack('<5s', sel)
      for i in code:
        data_selection_packet += pack('<i', i)
      #print (unpack('<5s{:d}i'.format(len(code)), data_selection_packet))
      
      try:
        #pass
        self.sock.sendto(data_selection_packet, (UDP_SENDTO_IP, UDP_SENDTO_PORT))
      except:
        self.debug.emit('initialization code select', 'exception')
        #pass

      rotary = fsEncoder(self.send)
      #self.params()
      

    @pyqtSlot()
    def run(self):
       self.running = True
       print ('fsSocket running')
       self.debug.emit('fsSocket running', 'info')
       
       while self.running:
         self.listen()
         
       #print ('[run] exited')
    
    
    def stop(self):
        self.running = False
        #print ('xplane stopped')
        self.finished.emit()
        #time.sleep(2)
    
    
    def listen(self):
         #try:
            data, addr = self.sock.recvfrom(8192)
            if data:
               self.unpack(data)
         #except Exception as exc:
         #   self.debug.emit('socket (%s)' % exc, 'exception')
         
         
    def parse(self, key):
      values = self.gauge[key]
      liste = {}
      #changed = True
      for value in values:
        if (value == "signal"): continue
        item = values[value]
        if (item["code"] in self.dataref):
          if ("float" in item):
            data = int(self.dataref[item["code"]][item["index"]] * 100) / 100
          else:
            data = int(self.dataref[item["code"]][item["index"]])
          '''
          if (data != item["data"]):
            changed = True
            self.gauge[key][value]["data"] = data
            liste[value] = data
          '''
          self.gauge[key][value]["data"] = data
          liste[value] = data
          
      '''
      if (changed):
        self.gauge[key]["signal"].emit(liste)
      '''
      self.gauge[key]["signal"].emit(liste)
        
      
    def unpack(self, raw):
      count = int((len(raw) - 5) / 36)
      for n in range(count):
        data = []
        offset = 5+(n*36)
        code = int(unpack_from('<i', raw, offset)[0])

        for p in range(1,9):
           data.append( unpack_from('<f', raw, offset+(p*4))[0] )

        self.dataref[code] = data
        
        if code == 150:
          print (data)

      for key in self.gauge:
        self.parse(key)


    def log(self, msg):
        print(msg)


    def send(self, idx, ref, dat):
      
      #self.debug.emit("GPIO: %s %s %d" % (idx, ref, dat))
      
      sel = bytes("CMND0", "utf-8")
      data_selection_packet = pack('<5s', sel)

      liste = {}
      loop = 1
      
      if (idx == "com"):
        if ref == "outer":
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/stby_com1_coarse_up", "utf-8")
            self.gauge["radio"]["com.stby"]["data"] += 100
          else:
            data_selection_packet += bytes("sim/radios/stby_com1_coarse_down", "utf-8")
            self.gauge["radio"]["com.stby"]["data"] -= 100
        elif ref == "inner":
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/stby_com1_fine_up", "utf-8")
            self.gauge["radio"]["com.stby"]["data"] += 2.5
          else:
            data_selection_packet += bytes("sim/radios/stby_com1_fine_down", "utf-8")
            self.gauge["radio"]["com.stby"]["data"] -= 2.5
        elif ref == "button":
          data_selection_packet += bytes("sim/radios/com1_standy_flip", "utf-8")
          tmp = self.gauge["radio"]["com.stby"]["data"]
          self.gauge["radio"]["com.stby"]["data"] = self.gauge["radio"]["com.active"]["data"]
          self.gauge["radio"]["com.active"]["data"] = tmp
        
        liste["com.active"] = self.gauge["radio"]["com.active"]["data"]
        liste["com.stby"] = self.gauge["radio"]["com.stby"]["data"]
        self.gauge["radio"]["signal"].emit(liste)
        
      elif (idx == "nav"):
        if ref == "outer":
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/stby_nav1_coarse_up", "utf-8")
            self.gauge["radio"]["nav.stby"]["data"] += 100
          else:
            data_selection_packet += bytes("sim/radios/stby_nav1_coarse_down", "utf-8")
            self.gauge["radio"]["nav.stby"]["data"] -= 100
        elif ref == "inner":
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/stby_nav1_fine_up", "utf-8")
            self.gauge["radio"]["nav.stby"]["data"] += 5
          else:
            data_selection_packet += bytes("sim/radios/stby_nav1_fine_down", "utf-8")
            self.gauge["radio"]["nav.stby"]["data"] -= 5
        elif ref == "button":
          data_selection_packet += bytes("sim/radios/nav1_standy_flip", "utf-8")
          tmp = self.gauge["radio"]["nav.stby"]["data"]
          self.gauge["radio"]["nav.stby"]["data"] = self.gauge["radio"]["nav.active"]["data"]
          self.gauge["radio"]["nav.active"]["data"] = tmp
        elif ref == "coder":
          #print ("coder %s" % dat)
          loop = abs(dat)
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/obs1_up", "utf-8")
          else:
            data_selection_packet += bytes("sim/radios/obs1_down", "utf-8")

        liste["nav.active"] = self.gauge["radio"]["nav.active"]["data"]
        liste["nav.stby"] = self.gauge["radio"]["nav.stby"]["data"]
        self.gauge["radio"]["signal"].emit(liste)
        
      elif (idx == "adf"):
        if ref == "outer":
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/actv_adf1_hundreds_up", "utf-8")
            self.gauge[idx]["frq"]["data"] += 100
          else:
            data_selection_packet += bytes("sim/radios/actv_adf1_hundreds_down", "utf-8")
            self.gauge[idx]["frq"]["data"] -= 100
        elif ref == "inner":
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/actv_adf1_ones_tens_up", "utf-8")
            self.gauge[idx]["frq"]["data"] += 1
          else:
            data_selection_packet += bytes("sim/radios/actv_adf1_ones_tens_down", "utf-8")
            self.gauge[idx]["frq"]["data"] -= 1
        #elif ref == "button":
        #  data_selection_packet += bytes("sim/radios/adf1_standy_flip", "utf-8")
        elif ref == "coder":
          #print ("coder %s" % dat)
          loop = abs(dat)
          if (dat > 0):
            data_selection_packet += bytes("sim/radios/adf1_card_up", "utf-8")
          else:
            data_selection_packet += bytes("sim/radios/adf1_card_down", "utf-8")
        
        liste["frq"] = self.gauge[idx]["frq"]["data"]
        self.gauge[idx]["signal"].emit(liste)
        
      elif (idx == "scr"):
        #print ("scr: %s" % dat)
        if ref == "switch":
          if (dat == 1):
            direction = 1
          else:
            direction = -1
          self.panel.emit(direction)
        
      #sel = bytes("CMND0", "utf-8")
      #data_selection_packet = pack('<5s{:d}s'.format(len(data)), sel, data)

      #for i in range(abs(n)):
      #  self.sock.sendto(data_selection_packet, (UDP_SENDTO_IP, UDP_SENDTO_PORT))
      for i in range(loop):
        self.sock.sendto(data_selection_packet, (UDP_SENDTO_IP, UDP_SENDTO_PORT))


    def datarref(self, index, dataref):
      dataref += '\0'
      nr_trailing_spaces = 400 - len(dataref)

      msg = "RREF" + '\0'
      packedindex = pack('<i', index)
      packedfrequency = pack('<i', 30)
      msg += packedfrequency
      msg += packedindex
      msg += dataref
      msg += ' ' * nr_trailing_spaces

      print(msg)
      
    def params(self):
      
      r = bytes("RREF0", "utf-8")
      a = 30
      b = 150
      c = bytes("sim/cockpit/gyros/dg_drift_ele_deg", "utf-8")

      data_selection_packet = pack('<5sii{:d}s'.format(len(c)), r, a, b, c)
      
      self.sock.sendto(data_selection_packet, (UDP_SENDTO_IP, UDP_SENDTO_PORT))
      
      #print (unpack('<5sii{:d}s'.format(len(c)), data_selection_packet))
      


      '''
      liste = {}
      if (dat > 0):
        self.gauge[idx]["stby"]["data"] += 10
      else:
        self.gauge[idx]["stby"]["data"] -= 10
      liste["active"] = self.gauge[idx]["active"]["data"]
      liste["stby"] = self.gauge[idx]["stby"]["data"]
      self.gauge[idx]["signal"].emit(liste)
      
      self.debug.emit("GPIO: %s %d" % (idx, self.gauge[idx]["stby"]["data"]))
      '''


      '''
      r = bytes("RREF0", "utf-8")
      a = 5
      b = 150
      c = bytes("sim/cockpit/gyros/dg_drift_vac_deg", "utf-8")

      #data_selection_packet = pack('<5sii20s', r, a, b, c)
      data_selection_packet = pack('<5sii{:d}s'.format(len(c)), r, a, b, c)
      print (data_selection_packet)

      print (unpack('<5sii20s', data_selection_packet))
      # unpack_from ?
      '''

      '''
      data_selection_packet = "RREF0"
      data_selection_packet += "\x03\x00\x00\x00"
      data_selection_packet += "\x03\x00\x00\x00"
      data_selection_packet += "sim/radios/obs1_up"

      data_selection_packet = "DREF0"
      data_selection_packet += "\x03\x00\x00\x00"
      data_selection_packet += "sim/radios/obs1_up"

      data_selection_packet = "RREF0"
      data_selection_packet += pack('<i', 1)
      data_selection_packet += pack('<i', 97)
      data_selection_packet += "sim/radios/obs1_down"

      outgoing.write("RREF\0");
      outgoing.writeInt32LE(1, 5);
      outgoing.writeInt32LE(97, 9);
      outgoing.write(dataref + "\0", 13);

      outgoing.write("DREF\0");
      outgoing.writeFloatLE(value, 5);
      outgoing.write(dataref + "\0", 9);
      '''
