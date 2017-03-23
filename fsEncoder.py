#!/usr/bin/python3
# -*- coding: utf-8 -*-

from RPi import GPIO
from functools import partial
import time

class fsEncoder():
  
  data = {
         "com": { "outer":  { "pinA": 11, "pinB": 12, "stateA": 0, "stateB": 0, "click": 0, "dt": 1  }, "inner": { "pinA": 15, "pinB": 16, "stateA": 0, "stateB": 0, "click": 0, "dt": 1  }, "button": { "pin": 13, "click": 0 } },
         "nav": { "outer":  { "pinA": 23, "pinB": 24, "stateA": 0, "stateB": 0, "click": 0, "dt": 1  }, "inner": { "pinA": 21, "pinB": 22, "stateA": 0, "stateB": 0, "click": 0, "dt": 1  }, "button": { "pin": 26, "click": 0 }, "coder": { "pinA": 31, "pinB": 29, "state": 0, "delta": 0, "stamp": 0 } },
         "adf": { "outer":  { "pinA": 36, "pinB": 35, "stateA": 0, "stateB": 0, "click": 0, "dt": 1  }, "inner": { "pinA": 38, "pinB": 37, "stateA": 0, "stateB": 0, "click": 0, "dt": 1  }, "button": { "pin": 40, "click": 0 }, "coder": { "pinA": 32, "pinB": 33, "state": 0, "delta": 0, "stamp": 0 } },
         "scr": { "switch": { "pinA": 18, "pinB": 19, "state": 0 } }
  }


  def __init__(self, trigger):
  
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
  
    for idx in self.data:
      
      info = self.data[idx]
      
      for ref in info:
      
        if ref == "outer" or ref == "inner":
          GPIO.setup(info[ref]["pinA"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          GPIO.setup(info[ref]["pinB"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          info[ref]["stateA"] = GPIO.input(info[ref]["pinA"])
          info[ref]["stateB"] = GPIO.input(info[ref]["pinB"])
          info[ref]["click"] = info[ref]["stateA"]
          GPIO.add_event_detect(info[ref]["pinA"], GPIO.BOTH, callback=partial(self.callback, idx, ref), bouncetime=25)
          GPIO.add_event_detect(info[ref]["pinB"], GPIO.BOTH, callback=partial(self.callback, idx, ref), bouncetime=25)
    
        if ref == "button":
          GPIO.setup(info[ref]["pin"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          info[ref]["click"] = GPIO.input(info[ref]["pin"])
          GPIO.add_event_detect(info[ref]["pin"], GPIO.BOTH, callback=partial(self.callback, idx, ref), bouncetime=25)
    
        if ref == "coder":
          GPIO.setup(info[ref]["pinA"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          GPIO.setup(info[ref]["pinB"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          info[ref]["state"] = self.sequence(info[ref]["pinA"], info[ref]["pinB"])
          GPIO.add_event_detect(info[ref]["pinA"], GPIO.BOTH, callback=partial(self.callback, idx, ref), bouncetime=25)
          GPIO.add_event_detect(info[ref]["pinB"], GPIO.BOTH, callback=partial(self.callback, idx, ref), bouncetime=25)
          
        if ref == "switch":
          GPIO.setup(info[ref]["pinA"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          GPIO.setup(info[ref]["pinB"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
          #info[ref]["click"] = 0
          GPIO.add_event_detect(info[ref]["pinA"], GPIO.FALLING, callback=partial(self.callback, idx, ref), bouncetime=75)
          GPIO.add_event_detect(info[ref]["pinB"], GPIO.FALLING, callback=partial(self.callback, idx, ref), bouncetime=75)
	
    self.trigger = trigger


  def sequence(self, a_pin, b_pin):
    a_state = GPIO.input(a_pin)
    b_state = GPIO.input(b_pin)
    seq = (a_state ^ b_state) | b_state << 1
    return seq


  def callback(self, idx, ref, channel):
    
    item = self.data[idx][ref]
    
    C = GPIO.input(channel)
    
    if ref == "button":
      
      if C != item["click"]:
        item["click"] = C
        if item["click"] == 0:
          self.trigger(idx, ref, item["click"])
    
    elif ref == "coder":
      state = self.sequence(item["pinA"], item["pinB"])
      delta = (state - item["state"]) % 4
      if delta != 0:
        if delta == 3:
          delta = -1
        elif delta == 2:
          delta = item["delta"]
        item["state"] = state
        item["delta"] = delta
        stamp = time.time()
        if (stamp - item["stamp"] < 0.25):
          delta = delta * 10
        item["stamp"] = stamp
        self.trigger(idx, ref, delta)

    elif ref == "switch":
      if channel == item["pinA"]:
        self.trigger(idx, ref, 1)
      elif channel == item["pinB"]:
        self.trigger(idx, ref, 2)
      
    else:
      
      if channel == item["pinA"]:
        if item["stateA"] == C:
          return
        item["stateA"] = C
      else:
        if item["stateB"] == C:
          return
        item["stateB"] = C

      if item["stateA"] != item["stateB"]:
        if channel == item["pinA"]:
          item["dt"] = -1
        else:
          item["dt"] = 1
      else:
        item["click"] = C
        self.trigger(idx, ref, item["dt"])

