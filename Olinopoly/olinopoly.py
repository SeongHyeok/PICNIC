# -*- coding: utf-8 -*-
"""
Olinopoly: A board game for Olin!
SoftwareDesign Project 2014 Spring

Created on Sun Apr  6 21:34:32 2014

@author: SeongHyeok Im, Inseong Joe and Dongyoung Kang

@note:
    Code-style:
        - Camelcase for function and class.
        - Underscore for variable.
        - Prefix 'g_' for global viarlable.
"""

############################################################################
# Imports
############################################################################

import pygame
from pygame.locals import *
import random
import math
import time
import sys, traceback

############################################################################
# Global variabless
############################################################################

# Screen
g_screen_board_width = 850
g_screen_board_height = 850
g_screen_status_width = 200

g_screen_width = g_screen_board_width + g_screen_status_width
g_screen_height = g_screen_board_height

# Map
#g_map_num_blocks_in_line = 3
g_map_num_blocks_in_line = 10
g_map_block_width = g_screen_board_width / g_map_num_blocks_in_line
g_map_block_height = g_screen_board_height / g_map_num_blocks_in_line

############################################################################
# Model Classes
############################################################################

class OlinopolyModel:
    def __init__(self):
        # Create map data
        self.map_blocks = []
        for i in range(1, 5, 1):    # 1 ~ 4
            print "===== i: %d" % (i)
            if i == 1:
                init_x = g_screen_board_width - g_map_block_width
                init_y = g_screen_board_height - g_map_block_height
            elif i == 2:
                init_x = 0
                init_y = g_screen_board_height - g_map_block_height
            elif i == 3:
                init_x = 0
                init_y = 0
            elif i == 4:
                init_x = g_screen_board_width - g_map_block_width
                init_y = 0

            for j in range(g_map_num_blocks_in_line - 1):    # 0 ~ n-1
                print "== j: %d" % (j)
                if j == 0:
                    x = init_x
                    y = init_y
                else:
                    if i == 1:
                        x = init_x - j * g_map_block_width
                        y = init_y
                    elif i == 2:
                        x = init_x
                        y = init_y - j * g_map_block_height
                    elif i == 3:
                        x = init_x + j * g_map_block_width
                        y = init_y
                    elif i == 4:
                        x = init_x
                        y = init_y + j * g_map_block_height

                print "x: %d / y: %d" % (x, y)
                map_block_object = MapBlock(
                    x, y, g_map_block_width, g_map_block_height, 'c', True
                )
                self.map_blocks.append(map_block_object)

        for i in range(0, len(self.map_blocks)):
            print "%02d - x: %3d / y: %3d" % (i + 1, self.map_blocks[i].x, self.map_blocks[i].y)

class Drawable(object):
    def __init__(self, x, y, width, height, c_or_i, is_visible):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.c_or_i = c_or_i
        self.is_visible = is_visible

class MapBlock(Drawable):
    def __init__(self, x, y, width, height, c_or_i, is_visible):
        super(MapBlock, self).__init__(x, y, width, height, c_or_i, is_visible)

class Marker(Drawable):
    def __init__(self):
        pass

############################################################################
# View Classes
############################################################################

class OlinopolyView:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        #fill in background color
        self.screen.fill(pygame.Color(236,245,235))
        
        for map_block in self.model.map_blocks:
            pygame.draw.rect(self.screen, pygame.Color(19,110,13), (map_block.x, map_block.y, map_block.width, map_block.height),3)
        
        pygame.display.flip()
############################################################################
# Controller Classes
############################################################################



############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    # Initialize screen
    size = (g_screen_width, g_screen_height)
    screen = pygame.display.set_mode(size)

    # MVC objects
    model = OlinopolyModel()
    view = OlinopolyView(model, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

        view.draw()
        time.sleep(.001)

    pygame.quit()
