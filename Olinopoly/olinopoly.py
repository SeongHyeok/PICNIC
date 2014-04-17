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
g_image_dir_path = os.path.join(os.curdir, "img")
g_map_block_dir_path = os.path.join(g_image_dir_path, "map")
g_marker_image_dir_path = os.path.join(g_image_dir_path, "marker")
g_olin_logo_dir_path = os.path.join(g_image_dir_path, "logo")

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
g_map_num_blocks = g_map_num_blocks_in_line * 4 - 4    # DO NOT CHANGE
g_map_block_width = g_screen_board_width / g_map_num_blocks_in_line     # DO NOT CHANGE
g_map_block_height = g_screen_board_height / g_map_num_blocks_in_line   # DO NOT CHANGE
g_map_block_initial_positions = [   # DO NOT CHANGE - 4 pairs of (x, y)
    (g_screen_board_width - g_map_block_width, g_screen_board_height - g_map_block_height),
    (0, g_screen_board_height - g_map_block_height),
    (0, 0),
    (g_screen_board_width - g_map_block_width, 0)
]
g_map_enable_softdsg_blinking = True

# Button
g_button_rect = (
    g_screen_board_width * 0.4,
    g_screen_board_height * 0.2,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.2,
)

# Olin Logo
g_olin_logo_rect = (
    g_screen_board_width * 0.4,
    g_screen_board_height * 0.4,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.2,

)

# Chance Card
g_chance_card_rect = (  # DO NOT CHANGE
    g_screen_board_width * 0.6,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.2
)
g_chance_card_num = 30
g_chance_card_position = [7, 13, 21, 29]
g_softdsg_card_position = [35]

# Complete area (for completed markers)
g_complete_area_rect = (
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.6,
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
        # Current state of game board
        # 0: Wait for other player
        # 1: Ready for rolling dice
        # 2: Wait for choosing marker
        # N: ...
        self.current_state = 1

        self.my_team_number = 0
        self.current_marker = 0

        self.enable_mouseover_map_block_info = True
        self.prev_mouseover_map_block = 0
        self.mouseover_map_block = -1  # -1 for indicating not-showing

        #self.num_of_teams = g_max_team_num
        self.num_of_teams = 1

        ##############################
        # Create map blocks

        # Powerful feature of our code is that it is generic for number!

        self.map_blocks = []
        num = 0
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
                i, self.map_blocks[i].rect[0], self.map_blocks[i].rect[1], self.map_blocks[i].num
            )

        ##############################
        # Create markers

        self.markers = []
        for i in range(g_max_team_num):
            self.markers.append([]) # for each team

        for i in range(self.num_of_teams):
            for j in range(4):
                init_x, init_y = g_marker_initial_positions[j]
                marker = Marker(
                    (init_x, init_y, g_screen_status_width / 4, g_screen_board_height * 0.2 / 2),
                    'i', True, i, j, None
                )
                self.markers[i].append(marker)
            self.moveMarker(i, 0, 0)

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

        self.olin_logo = OlinLogo(
            g_olin_logo_rect, 'i', True
        )

    def moveMarker(self, team, player, target_pos):
        if target_pos >= g_map_num_blocks:
            target_pos = -1 # -1 means completed
        prev_pos = self.markers[team][player].block_pos

        # add to current map block
        if target_pos != -1:
            self.map_blocks[target_pos].markers_on_block.append([team, player])

        # remove from previous map block
        if prev_pos != None:
            for marker in self.map_blocks[prev_pos].markers_on_block:
                t, p = marker
                if t == team and p == player:
                    self.map_blocks[prev_pos].markers_on_block.remove([t, p])
                    break
        self.markers[team][player].block_pos = target_pos
        self.markers[team][player].prev_block_pos= prev_pos

        logger.debug("team: %d / player: %d / target: %d / prev: %s" % (team, player, target_pos, str(prev_pos)))

    def blinkSoftDsg(self):
        if g_map_enable_softdsg_blinking:
            for i in g_softdsg_card_position:
                if i < len(self.map_blocks):
                    map_block = self.map_blocks[i]
                    if map_block.current_color == 'r':
                        map_block.current_color = 'g'
                    elif map_block.current_color == 'g':
                        map_block.current_color = 'b'
                    elif map_block.current_color == 'b':
                        map_block.current_color = 'r'
                    img_path = os.path.join(g_map_block_dir_path, "%d%c.png" % (i, map_block.current_color))
                    logger.debug("next image: %s" % (img_path))
                    map_block.img = pygame.transform.scale(
                        pygame.image.load(img_path),
                        (map_block.rect[2] - g_line_width * 2, map_block.rect[3] - g_line_width * 2)
                    )

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
        self.markers_on_block = []   # pairs of [team, player]

        # image
        if c_or_i == 'i':
            if num in g_chance_card_position:
                img_path = os.path.join(g_map_block_dir_path, "chance.png")
            elif num in g_softdsg_card_position:
                self.current_color = 'r'
                img_path = os.path.join(g_map_block_dir_path, "%d%c.png" % (num, self.current_color))
            else:
                img_path = os.path.join(g_map_block_dir_path, "%d.png" % (num))
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

    def reloadImage(self):
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join(g_marker_image_dir_path, "%d.png" % (self.player))),
            (int(self.rect[2]),int(self.rect[3]))
        )

    def pressed(self, x, y):
        if x > self.rect[0]:
            if y > self.rect[1]:
                if x < self.rect[0] + self.rect[2]:
                    if y < self.rect[1] + self.rect[3]:
                        print "%d Marker chosen for team %d " % (self.player, self.team)
                        return True
                    else:
                        return False
                else:
                   return False
            else:
               return False
        else:
            return False


class ChanceCard(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(ChanceCard, self).__init__(rect, c_or_i, is_visible)
        self.size = g_chance_card_num
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join(g_map_block_dir_path, "chance.png")),
            (int(self.rect[2] - g_line_width * 2), int(self.rect[3] - g_line_width * 2))
        )

class CompleteArea(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(CompleteArea, self).__init__(rect, c_or_i, is_visible)

class OlinLogo(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(OlinLogo, self).__init__(rect, c_or_i, is_visible)
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join(g_olin_logo_dir_path, "olinopoly_logo.png")),
            (int(self.rect[2]),int(self.rect[3]))
        )

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
            # Update marker position
            for marker in map_block.markers_on_block:
                team, player = marker
                # [TODO] Consider multiple blocks
                self.model.markers[team][player].rect = (
                    map_block.rect[0],
                    map_block.rect[1],
                    map_block.rect[2] / 2,
                    map_block.rect[3] / 2
                )
                if self.model.markers[team][player].prev_block_pos == None:
                    self.model.markers[team][player].reloadImage()

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
        self.model.Button1.create_button(
            self.screen,
            (107,142,35),
            g_button_rect[0],
            g_button_rect[1],
            g_button_rect[2],
            g_button_rect[3],
            20,
            "Roll Dice!",
            (255,255,255)
        )

        # Olinopoly Logo
        self.screen.blit(
            self.model.olin_logo.img,
            (self.model.olin_logo.rect[0], self.model.olin_logo.rect[1])
        )
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.olin_logo.rect,
            1
        )

        # Mouseover Map Block Information
        if self.model.enable_mouseover_map_block_info:
            if self.model.mouseover_map_block >= 0:
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
        self.model.mouseover_map_block = -1

        x, y = pygame.mouse.get_pos()
        if g_map_block_width < x < g_screen_board_width - g_map_block_width:
            #logger.debug("middle")
            if 0 <= y <= g_map_block_height:
                self.onMapBlock(g_map_num_blocks_in_line * 2 - 2 + x / g_map_block_width)
            elif g_screen_board_height - g_map_block_height <= y:
                self.onMapBlock(g_map_num_blocks_in_line - 1 - x / g_map_block_width)
            else:
                pass
            pass
        elif x <= g_map_block_width:
            #logger.debug("left")
            self.onMapBlock(g_map_num_blocks_in_line - 2 + (g_map_num_blocks_in_line - y / g_map_block_height))
        elif g_screen_board_width - g_map_block_width <= x <= g_screen_board_width:
            #logger.debug("right")
            num = g_map_num_blocks_in_line * 3 - 3 + (y / g_map_block_height)
            if num == g_map_num_blocks_in_line * 4 - 4:
                num = 0
            self.onMapBlock(num)
        else:
            pass

class OlinopolyDiceController:
    """ """
    def __init__(self, model):
        self.model = model

    def rollDice(self):
        dice_num = random.randint(1, 6)
        logger.debug("dice number: %d" % (dice_num))

        team = self.model.my_team_number
        player = self.model.current_marker
        self.model.moveMarker(team, player, self.model.markers[team][player].block_pos + dice_num)

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
    controller_dice = OlinopolyDiceController(model)

    # Timer for events
    # 1 - Mouse over
    # 2 - Blinking SoftDsg
    pygame.time.set_timer(USEREVENT + 1, 500)
    pygame.time.set_timer(USEREVENT + 2, 300)

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

            if event.type == USEREVENT + 2:
                model.blinkSoftDsg()

            if event.type == MOUSEBUTTONDOWN:
                if model.Button1.pressed(pygame.mouse.get_pos()):
                    controller_dice.rollDice()
                x,y = pygame.mouse.get_pos()
                for team in model.markers:
                    for player in team:
                        player.pressed(x,y)

                # print x, y
#                for marker in model.markers:
#                    if marker.rect[0] < x < marker.rect[0] + g_screen_status_width/4:
#                        if marker.rect[1] < y < marker.rect[1] + g_screen_height*0.2/2:
#                            marker.is_visible = False
#                            model.createMarkerOnBoard(marker.team, marker.player)

        view.draw()
        time.sleep(.001)
    # While end
    ####################
    pygame.quit()
