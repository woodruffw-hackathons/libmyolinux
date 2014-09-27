# Communicates with PyMyo.exe to enable Python support of Myo armband
# Paul Lutz
# Scott Martin
# Fabricate.IO

import time
import subprocess
import sys
import struct
import math
import threading
import platform

class Myo(threading.Thread):
  """ Wrapper for PyMyo.exe - handles event data via callback, and can vibrate the myo """
  
  POSES = {
    0 : "rest",
    1 : "fist",
    2 : "waveIn",
    3 : "waveOut",
    4 : "fingersSpread",
    5 : "reserved1",
    6 : "thumbToPinky",
  }
  OSCOMMANDS = {
    "Darwin" : "./PyMyo",
    "Windows": "PyMyo.exe",
  }
  # These durations are specified by Thalmic
  VIBE_LONG = 2
  VIBE_MEDIUM = 1
  VIBE_SHORT = 0

  cmd = "nope"
  
  # PyMyo.exe prints a packet (followed by a newline) every time the myo has new event data
  PACKET_LEN = 30
  PACKET_FORMAT = "fffffffBB"
  
  def __init__(self, callback):
    threading.Thread.__init__(self)
    
    self.cmd = self.OSCOMMANDS.get(platform.system())
    
    self.proc = subprocess.Popen(self.cmd, bufsize=0, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    
    self.pose = None
    self.quat = None
    self.rot = None
    self.accel = None
    
    self.callback = callback
    
  def run(self):
    while True:
      # This will hang until the next data event is read
      newdata = self.proc.stdout.readline().strip()

      if len(newdata) != Myo.PACKET_LEN:
        continue
      
      # Extract data from the packet
      data = struct.unpack(Myo.PACKET_FORMAT,newdata)
      (self.accel, self.quat, self.pose, self.which_arm) = (data[0:3], data[3:7], data[7], data[8])
      
      # Update Euler rotation if valid
      self.rot = self.calculateEuler(self.quat) or self.rot
      
      # Callback to user code
      self.callback(self)
        
  def calculateEuler(self, quat):
    # Convert quaternion to (roll, pitch, yaw) rotation
    (w, x, y, z) = quat
    try:
      roll = math.atan2(2*y*w - 2*x*z, 1 - 2*y*y - 2*z*z)
      pitch = math.atan2(2*x*w - 2*y*z, 1 - 2*x*x - 2*z*z)
      yaw = math.asin(2*x*y + 2*z*w)
      return (roll, pitch, yaw)
    except: 
      return None

  def vibrate(self, duration):
    # Vibrates the Myo (must be one of VIBE_*)
    assert duration in [Myo.VIBE_LONG, Myo.VIBE_MEDIUM, Myo.VIBE_SHORT]
    self.proc.stdin.write(chr(1) + "\n")
    self.proc.stdin.flush()
    
  def getAcceleration(self):
    # Return [x, y, z] acceleration
    return self.accel
   
  def getRotation(self):
    # Return [roll, pitch, yaw]
    return self.rot
   
  def getRotationScaled(self, scale):
    # Returns [x, y, z] accel scaled between 0 and scale.
    return [(x+math.pi)/(math.pi*2.0)*scale for x in self.rot]
   
  def getArm(self):
    # Returns 0 for right arm, 1 for left arm
    return self.which_arm
    
  def getArmString(self):
    # Return "R" for right arm, "L" for left arm, or "?" if no arm
    return {
      0: "R",
      1: "L"
    }.get(self.getArm(), "?")
    
  def getPoseString(self):
    # Return string representing pose, or "unknown" if unknown
    return self.POSES.get(self.getPose(), "unknown")
    
  def getPose(self):
    # Return integer pose state
    return self.pose
  