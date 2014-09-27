#Sends data to Will
from myo import Myo
import sys
import socket

last_pose = None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
sock.connect(("10.200.66.157", 6969))

def printData(myo):
 
  #Get data stream
  
  #Send data stream
  sock.send(pose_str)
  

def main():
  myMyo = Myo(callback=printData)
  myMyo.daemon = True
  myMyo.start()
  raw_input("Press enter to exit")
      
if __name__ == "__main__":
    main()