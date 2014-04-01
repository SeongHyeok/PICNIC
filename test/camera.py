# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 20:14:26 2014

@author: sim
"""

############################################################################
# Imports
############################################################################

import pygame
import pygame.camera
from pygame.locals import *

import time

############################################################################
# Global variabless
############################################################################



############################################################################
# Main
############################################################################

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode([800,420])

cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_from_game = False
            running = False
            break
    # sleep between every frame
    time.sleep(0.05)
    # fetch the camera image
    image = cam.get_image()
    # flip image horizontally
    image = pygame.transform.flip(image, 1, 0)
    # blank out the screen
    screen.fill([0,0,0])
    # copy the camera image to the screen
    screen.blit(image, (100, 0))
    # update the screen to show the latest screen image

    pygame.display.update()