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
import os, sys, traceback

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

############################################################################
# Global variabless
############################################################################
# Path
g_image_dir_path = os.path.join(os.curdir, "img/map")

# Screen
g_screen_board_width = 850
g_screen_board_height = 850
g_screen_status_width = 300

g_screen_width = g_screen_board_width + g_screen_status_width
g_screen_height = g_screen_board_height

# Map
g_map_num_blocks_in_line = 10
assert g_map_num_blocks_in_line >= 5
g_map_block_width = g_screen_board_width / g_map_num_blocks_in_line
g_map_block_height = g_screen_board_height / g_map_num_blocks_in_line

# Chance Card
g_chance_card_rect = (
    g_screen_board_width * 0.6,
    g_screen_board_height * 0.5,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.3
)
g_chance_card_num = 30
g_chance_card_position = [8, 14, 22, 30]

# Complete area (for completed markers)
g_complete_area_rect = (
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.5,
    g_screen_board_width * 0.3,
    g_screen_board_height * 0.3
)

############################################################################
# Model Classes
############################################################################

class OlinopolyModel:
    def __init__(self):

        ##############################
        # Create map data
        # Following code for generating map blocks is generic
        self.map_blocks = []
        num = 1
        for i in range(1, 5, 1):    # 1 ~ 4
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

                if num == 2:
                    map_block_object = MapBlock(
                        (x, y, g_map_block_width, g_map_block_height), 'i', True, num
                    )
                else:
                    map_block_object = MapBlock(
                        (x, y, g_map_block_width, g_map_block_height), 'c', True, num
                    )
                self.map_blocks.append(map_block_object)
                num += 1

        for i in range(0, len(self.map_blocks)):
            logger.debug("%02d - x: %3d / y: %3d / num: %2d",
                i + 1, self.map_blocks[i].rect[0], self.map_blocks[i].rect[1], self.map_blocks[i].num
            )

        ##############################
        # Create markers

        ##############################
        # Create chance card
        self.chance_card = ChanceCard(
            g_chance_card_rect, 'c', True
        )

        ##############################
        # Create complete area
        self.complete_area = CompleteArea(
            g_complete_area_rect, 'c', True
        )


class Drawable(object):
    def __init__(self, rect, c_or_i, is_visible):
        self.rect = rect
        self.c_or_i = c_or_i
        self.is_visible = is_visible

class MapBlock(Drawable):
    def __init__(self, rect, c_or_i, is_visible, num):
        super(MapBlock, self).__init__(rect, c_or_i, is_visible)
        self.num = num  # map block number
        if c_or_i == 'i':
            img_path = os.path.join(g_image_dir_path, "%d.png" % (num))
            self.img = pygame.transform.scale(pygame.image.load(img_path), (self.rect[2], self.rect[3]))
        else:
            self.img = None

class Marker(Drawable):
    def __init__(self, rect, c_or_i, is_visible, team):
        super(Marker, self).__init__(rect, c_or_i, is_visible)
        self.team = team

class ChanceCard(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(ChanceCard, self).__init__(rect, c_or_i, is_visible)
        self.size = g_chance_card_num

class CompleteArea(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(CompleteArea, self).__init__(rect, c_or_i, is_visible)

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

        # Map block
        for map_block in self.model.map_blocks:
            if map_block.c_or_i == 'c':
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(19,110,13),
                    map_block.rect,
                    3
                )
            elif map_block.c_or_i == 'i':
                self.screen.blit(map_block.img, (map_block.rect[0], map_block.rect[1]))

        # Chance card
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.chance_card.rect,
            3
        )

        # Complete area
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.complete_area.rect,
            3
        )

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
