# Test of PyMyo - same functionality as hello-myo.exe
# Paul Lutz
# Scott Martin

from myo import Myo
import sys
import socket

last_pose = None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
sock.connect(("10.200.49.112", 6969))

def printData(myo):
  global last_pose
  
  # Rotation is represented by number of stars (as in hello-myo.exe)
  (roll_str, pitch_str, yaw_str) = ["*" * int(r) for r in myo.getRotationScaled(18.0)]
  x
  
  pose_str = myo.getPoseString()
  
  sock.send(pose_str)
  
  # Print out the rotation and arm state on the same line each update
  sys.stdout.write('\r[{:17s}][{:17s}][{:17s}][{:1s}][{:15s}]'.format(
      roll_str,
      pitch_str,
      yaw_str,
      arm_str, 
      pose_str,
    )
  )
  
  if (pose_str == "fist") and (last_pose != myo.getPose()):
    myo.vibrate(Myo.VIBE_MEDIUM)
  
  last_pose = myo.getPose()

def main():
  myMyo = Myo(callback=printData)
  myMyo.daemon = True
  myMyo.start()
  raw_input("Press enter to exit")
      
if __name__ == "__main__":
    main()