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

import pygame, Buttons
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
g_marker_image_dir_path = os.path.join(os.curdir, "img/marker")

# Screen
g_screen_board_width = 850
g_screen_board_height = 850
g_screen_status_width = int(g_screen_board_width * 0.6)

g_screen_width = g_screen_board_width + g_screen_status_width   # DO NOT CHANGE
g_screen_height = g_screen_board_height # DO NOT CHANGE

g_line_width = 2

# Map
g_map_num_blocks_in_line = 10
g_map_num_blocks_in_line_max = 10   # DO NOT CHANGE
g_map_num_blocks_in_line_min = 5    # DO NOT CHANGE
assert \
    g_map_num_blocks_in_line_min <= g_map_num_blocks_in_line and \
    g_map_num_blocks_in_line_max <= g_map_num_blocks_in_line_max
g_map_block_width = g_screen_board_width / g_map_num_blocks_in_line     # DO NOT CHANGE
g_map_block_height = g_screen_board_height / g_map_num_blocks_in_line   # DO NOT CHANGE
g_map_block_initial_positions = [   # DO NOT CHANGE - 4 pairs of (x, y)
    (g_screen_board_width - g_map_block_width, g_screen_board_height - g_map_block_height),
    (0, g_screen_board_height - g_map_block_height),
    (0, 0),
    (g_screen_board_width - g_map_block_width, 0)
]

# Chance Card
g_chance_card_rect = (  # DO NOT CHANGE
    g_screen_board_width * 0.6,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.2
)
g_chance_card_num = 30
g_chance_card_position = [8, 14, 22, 30]

# Complete area (for completed markers)
g_complete_area_rect = (
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.3,
    g_screen_board_height * 0.2
)

# Button
g_button_rect = (
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.3,
    g_screen_board_width * 0.3,
    g_screen_board_height * 0.2
)

# Marker
g_marker_start_x = g_screen_board_width - g_map_block_width
g_marker_start_y = g_screen_board_height - g_map_block_height
g_marker_width = g_map_block_width / 2
g_marker_height = g_map_block_height / 3
g_marker_initial_positions = [  # DO NOT CHANGE - 4 pairs of (x, y)
    (g_screen_board_width + g_screen_status_width / 2, 0),
    (g_screen_board_width + g_screen_status_width * 3 / 4, 0),
    (g_screen_board_width + g_screen_status_width / 2, g_screen_board_height * 0.2 / 2),
    (g_screen_board_width + g_screen_status_width * 3 / 4, g_screen_board_height * 0.2 / 2)
]

# Game data
g_max_team_num = 4

############################################################################
# Model Classes
############################################################################

class OlinopolyModel:
    def __init__(self):
        self.enable_mouseover_map_block_info = True
        self.prev_mouseover_map_block = 0
        self.mouseover_map_block = 0  # 0 for indicating not-showing

        #self.num_of_teams = g_max_team_num
        self.num_of_teams = 1

        ##############################
        # Create map blocks

        # Powerful feature of our code is that it is generic for number!

        self.map_blocks = []
        num = 1
        for i in range(4):    # 0 ~ 3 (bottom, left, top and right)
            init_x, init_y = g_map_block_initial_positions[i]

            for j in range(g_map_num_blocks_in_line - 1):    # 0 ~ n-1
                if j == 0:
                    x = init_x
                    y = init_y
                else:
                    if i == 0:
                        x = init_x - j * g_map_block_width
                        y = init_y
                    elif i == 1:
                        x = init_x
                        y = init_y - j * g_map_block_height
                    elif i == 2:
                        x = init_x + j * g_map_block_width
                        y = init_y
                    elif i == 3:
                        x = init_x
                        y = init_y + j * g_map_block_height

                map_block_object = MapBlock(
                    (x, y, g_map_block_width, g_map_block_height), 'i', True, num
                )
                self.map_blocks.append(map_block_object)
                num += 1

        for i in range(0, len(self.map_blocks)):
            logger.debug("map block %02d - x: %3d / y: %3d / num: %2d",
                i + 1, self.map_blocks[i].rect[0], self.map_blocks[i].rect[1], self.map_blocks[i].num
            )

        ##############################
        # Create markers

        self.markers = []
        for i in range(g_max_team_num):
            self.markers.append([])

        for i in range(self.num_of_teams):
            for j in range(4):
                init_x, init_y = g_marker_initial_positions[j]
                marker = Marker(
                    (init_x, init_y, g_screen_status_width / 4, g_screen_board_height * 0.2 / 2),
                    'i', True, i + 1, j + 1, None
                )
                self.markers[i].append(marker)
        #self.createMarkerOnBoard(1, 1)

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

        ##############################
        # Create button

        self.Button1 = Buttons.Button()

        ##############################
        # Create Olin Logo
        #self.olinlogo = OlinLogo()

    def createMarkerOnBoard(self, team, player):
        self.team_one_markers_board = []
        new_marker = Marker(
                        (g_marker_start_x,g_marker_start_y,g_marker_height, g_marker_width),
                        "i", True, team, player, 1
                    )
        self.team_one_markers_board.append(new_marker)

class Drawable(object):
    def __init__(self, rect, c_or_i, is_visible):
        self.rect = rect
        self.c_or_i = c_or_i
        self.is_visible = is_visible

class MapBlock(Drawable):
    def __init__(self, rect, c_or_i, is_visible, num):
        super(MapBlock, self).__init__(rect, c_or_i, is_visible)
        # map block number
        self.num = num

        # count markers that are on a block
        self.marker_on_block = []   # pairs of (team, player)

        # image
        if c_or_i == 'i':
            if num in g_chance_card_position:
                img_path = os.path.join(g_image_dir_path, "chance.png")
            else:
                img_path = os.path.join(g_image_dir_path, "%d.png" % (num))
            self.img = pygame.transform.scale(
                pygame.image.load(img_path),
                (self.rect[2] - g_line_width * 2, self.rect[3] - g_line_width * 2)
            )
        else:
            self.img = None

class Marker(Drawable):
    def __init__(self, rect, c_or_i, is_visible, team, player, block_pos):
        super(Marker, self).__init__(rect, c_or_i, is_visible)
        self.team = team
        self.player = player
        self.block_pos = block_pos

        if self.c_or_i == "i":
            self.img = pygame.transform.scale(
                pygame.image.load(os.path.join(g_marker_image_dir_path, "%d.png" % (player))),
                (int(self.rect[2]),int(self.rect[3]))
            )
        else:
            self.img = None

    def moveMarker(self, dice_num, prev_block_num):
        self.block_pos = prev_block_num + dice_num
        if self.block_pos > 36:
            self.is_visible = False
        new_prev_block_num = self.block_pos
        return self.block_pos

class ChanceCard(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(ChanceCard, self).__init__(rect, c_or_i, is_visible)
        self.size = g_chance_card_num
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join(g_image_dir_path, "chance.png")),
            (int(self.rect[2] - g_line_width * 2), int(self.rect[3] - g_line_width * 2))
        )

class CompleteArea(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(CompleteArea, self).__init__(rect, c_or_i, is_visible)

class OlinLogo(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(OlinLogo, self).__init__(rect, c_or_i, is_visible)

############################################################################
# View Classes
############################################################################

class OlinopolyView:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        #fill in background color
        self.screen.fill(pygame.Color(236, 245, 235))

        # Map block
        for map_block in self.model.map_blocks:
            if map_block.c_or_i == 'c':
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(19, 110, 13),
                    map_block.rect,
                    1
                )
            elif map_block.c_or_i == 'i':
                # image
                self.screen.blit(
                    map_block.img,
                    (map_block.rect[0] + g_line_width, map_block.rect[1] + g_line_width)
                )
                # rectangle
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(19, 110, 13),
                    map_block.rect,
                    1
                )

        # Chance card
        self.screen.blit(
            self.model.chance_card.img,
            (self.model.chance_card.rect[0] + g_line_width, self.model.chance_card.rect[1] + g_line_width)
        )
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.chance_card.rect,
            1
        )

        # Complete area
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.complete_area.rect,
            1
        )

        # Button
        self.model.Button1.create_button(self.screen, (107,142,35),  g_screen_board_width * 0.4,  g_screen_board_height * 0.2,  g_screen_board_width * 0.2,     g_screen_board_height * 0.2,    0,        "Roll Dice!", (255,255,255))

        # Mouseover Map Block Information
        if self.model.enable_mouseover_map_block_info:
            if self.model.mouseover_map_block != 0:
                msg = 'Map Block Number: %d' % (self.model.mouseover_map_block)
                w, h = font_map_block_info.size(msg)
                x, y = pygame.mouse.get_pos()
                title = font_map_block_info.render(msg, True, (10, 10, 115))

                pygame.draw.rect(
                    self.screen,
                    pygame.Color(0, 0, 0),
                    (x - 5, y - 5, w + 10, h + 10),
                    1
                )
                self.screen.blit(title, (x, y))

        # Marker
        for i in range(self.model.num_of_teams):
            for marker in self.model.markers[i]:
                self.screen.blit(
                    marker.img,
                    (marker.rect[0], marker.rect[1])
                )
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(19, 110, 13),
                    marker.rect,
                    1
                )

        pygame.display.flip()

############################################################################
# Controller Classes
############################################################################

class OlinopolyMouseController:
    """ """
    def __init__(self, model):
        self.model = model

    def handleMouseEvent(self, event):
        if event.type == MOUSEMOTION:
            pass

class OlinopolyMouseOverController:
    """ """
    def __init__(self, model):
        self.model = model

    def onMapBlock(self, num):
        #logger.debug("On map block %d" % num)
        self.model.prev_mouseover_map_block = self.model.mouseover_map_block
        self.model.mouseover_map_block = num

    def check(self):
        self.model.mouseover_map_block = 0

        x, y = pygame.mouse.get_pos()
        if g_map_block_width < x < g_screen_board_width - g_map_block_width:
            #logger.debug("middle")
            if 0 <= y <= g_map_block_height:
                self.onMapBlock(g_map_num_blocks_in_line * 2 - 1 + x / g_map_block_width)
            elif g_screen_board_height - g_map_block_height <= y:
                self.onMapBlock(g_map_num_blocks_in_line - x / g_map_block_width)
            else:
                pass
            pass
        elif x <= g_map_block_width:
            #logger.debug("left")
            self.onMapBlock(g_map_num_blocks_in_line - 1 + (g_map_num_blocks_in_line - y / g_map_block_height))
        elif g_screen_board_width - g_map_block_width <= x <= g_screen_board_width:
            #logger.debug("right")
            num = g_map_num_blocks_in_line * 3 - 2 + (y / g_map_block_height)
            if num == g_map_num_blocks_in_line * 4 - 3:
                num = 1
            self.onMapBlock(num)
        else:
            pass

'''class MarkerController:
    def __init__(self, model):
        self.model = model

    def markerclicked(self):
        x,y = pygame.mouse.get_pos()
        if'''

############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    # Initialize screen
    size = (g_screen_width, g_screen_height)
    screen = pygame.display.set_mode(size)

    font_map_block_info = pygame.font.SysFont('Verdana', 16, False)

    # MVC objects
    model = OlinopolyModel()
    view = OlinopolyView(model, screen)
    controller_mouse = OlinopolyMouseController(model)
    controller_mouse_over = OlinopolyMouseOverController(model)

    # Timer for events
    # - Mouse over
    pygame.time.set_timer(USEREVENT + 1, 500)

    running = True
    ####################
    # While start
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

            if event.type == MOUSEMOTION:
                controller_mouse.handleMouseEvent(event)

            if event.type == USEREVENT + 1:
                controller_mouse_over.check()

            if event.type == MOUSEBUTTONDOWN:
                if model.Button1.pressed(pygame.mouse.get_pos()):
                    dice_num = random.randint(1,6)
                    logger.debug("dice number: %d" % (dice_num))
#                    if len(model.team_one_markers_board) >= 1:
#                        if event.type == MOUSEBUTTONDOWN:
#                            a,b = pygame.mouse.get_pos()
#                            for marker_board in model.team_one_markers_board:
#                                if marker_board.rect[0] < a < marker_board.rect[0] + g_marker_width:
#                                    if marker_board.rect[1] < b < marker_board.rect[1] + g_marker_height:
#                                        marker_board.moveMarker(dice_num, marker_board.board_pos)

                x,y = pygame.mouse.get_pos()
                # print x, y
                for marker in model.markers:
                    if marker.rect[0] < x < marker.rect[0] + g_screen_status_width/4:
                        if marker.rect[1] < y < marker.rect[1] + g_screen_height*0.2/2:
                            marker.is_visible = False
                            model.createMarkerOnBoard(marker.team, marker.player)

        view.draw()
        time.sleep(.001)
    # While end
    ####################
    pygame.quit()
