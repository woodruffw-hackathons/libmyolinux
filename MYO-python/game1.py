#Example game using input from Thalmic Myo

import pygame
import random
import sys
import os
import tempfile

from sys import stdin


#Import lib w/ myo gestures
from myo import Myo

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)

PI = 3.1415

#---Main Program Loop---
def game(myo):
    global last_pose
    pygame.init()

    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Myo Linux Driver Demo")


    x_coord = 0
    y_coord = 0
    height = 50
    width = 50

    x_speed = 0
    y_speed = 0
    out_speed = 0
    
    done = False
    pressed = False

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # User pressed down on a key
            if event.type == pygame.KEYDOWN:
                # Change Position
                if event.key == pygame.K_LEFT:
                    x_speed = -3
                if event.key == pygame.K_RIGHT:
                    x_speed = 3
                if event.key == pygame.K_UP:
                    y_speed = -3
                if event.key == pygame.K_DOWN:
                    y_speed = 3
                # Change Size
                if event.key == pygame.K_1:
                    out_speed = 3
                if event.key == pygame.K_2:
                    out_speed = -3
            # User let up on a key
            if event.type == pygame.KEYUP:
                # If it is an arrow key, reset vector back to zero
                if event.key == pygame.K_LEFT:
                    x_speed = 0
                if event.key == pygame.K_RIGHT:
                    x_speed = 0
                if event.key == pygame.K_UP:
                    y_speed = 0
                if event.key == pygame.K_DOWN:
                    y_speed = 0
                if event.key == pygame.K_1:
                    out_speed = 0
                if event.key == pygame.K_2:
                    out_speed = 0
                    
        #printData(myo)
        
        #---Drawing code should go here---
        #if (pose_str == "waveOut") and (last_pose != myo.getPose()):
        #    myo.vibrate(Myo.VIBE_MEDIUM)
  
        #last_pose = myo.getPose()
        #Clear Screen
        screen.fill(WHITE)
    
        # Move the object according to the speed vector.
        x_coord += x_speed
        y_coord += y_speed
        height += out_speed
        width += out_speed
        
        pygame.draw.rect(screen, BLUE, [x_coord, y_coord, width, height])
        #update screen
        pygame.display.flip()

        #limit to 60 frames per second
        clock.tick(60)
    pygame.quit()

def printData(myo):

    global last_pose
    pose_str = myo.getPoseString()

    print pose_str
    if (pose_str == "waveOut") and (last_pose != myo.getPose()):
        myo.vibrate(Myo.VIBE_MEDIUM)
  
    last_pose = myo.getPose()

def printstdin(myo):

    tmpdir = tempfile.mkdtemp()
    filename = os.path.join(tmpdir, 'myfifo')
    print filename
    try:
        os.mkfifo(filename)
    except OSError, e:
        print "Failed to create FIFO: %s" % e
    else:
        fifo = open(filename, 'w')
        for i in range(100):
            print >> fifo, "hello"
        fifo.close()
        os.remove(filename)
        os.rmdir(tmpdir)
        
def main():
    myMyo = Myo(callback=printstdin)
    myMyo.daemon = True
    myMyo.start()
    raw_input("Press enter to exit")
      
if __name__ == "__main__":
    main()
