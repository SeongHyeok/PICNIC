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
import time
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

############################################################################
# Debug options
############################################################################

g_debug_dice = False

############################################################################
# Global variabless
############################################################################
# Path
g_image_dir_path = os.path.join(os.curdir, "img")
g_map_block_dir_path = os.path.join(g_image_dir_path, "map")
g_marker_image_dir_path = os.path.join(g_image_dir_path, "marker")
g_olin_logo_dir_path = os.path.join(g_image_dir_path, "logo")
g_profile_dir_path = os.path.join(g_image_dir_path, "profile")
g_dice_dir_path = os.path.join(g_image_dir_path, "dice")

g_txt_dir_path = os.path.join(os.curdir, "txt")
g_map_block_game_txt_dir_path = os.path.join(g_txt_dir_path, "map_block_desc/game")
g_map_block_olin_txt_dir_path = os.path.join(g_txt_dir_path, "map_block_desc/olin")

# Screen
g_screen_board_width = 800
g_screen_board_height = 800
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
g_button_roll_dice_rect = (
    g_screen_board_width * 0.6,
    g_screen_board_height * 0.12,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.06
)

# Olin Logo
g_olin_logo_rect = (
    g_screen_board_width * 0.4,
    g_screen_board_height * 0.4,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.2,

)

# Game Description
g_game_des_rect = (
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.3,
    g_screen_board_height * 0.2
)

# Place Description
g_place_des_rect = (
    g_screen_board_width * 0.5,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.3,
    g_screen_board_height * 0.2
)

# Chance Card
g_chance_card_num = 30
g_chance_card_position = [7, 13, 21, 29]

g_softdsg_card_position = [35]

# Current turn information area
g_current_turn_area_rect = (
    g_screen_board_width * 0.15,
    g_screen_board_height * 0.12,
    g_screen_board_width * 0.35,
    g_screen_board_height * 0.06
)
g_current_turn_str = "Current Turn - %s"

# Complete area (for completed markers)
g_complete_area_rect = (
    g_screen_board_width * 0.15,
    g_screen_board_height * 0.2,
    g_screen_board_width * 0.35,
    g_screen_board_height * 0.2
)
g_complete_area_marker_width = g_map_block_width / 2
g_complete_area_max_in_row = g_complete_area_rect[2] / g_complete_area_marker_width

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

# Profile Area
g_profile_main_rect = (
    g_screen_board_width,
    0,
    g_screen_status_width * 0.5,
    g_screen_height * 0.3
)

g_profile_other_first_rect = (
    g_screen_board_width,
    g_screen_board_height * 0.3,
    g_screen_status_width / 3.0,
    g_screen_board_height * 0.2
)

# StatusArea Area
g_status_main_rect = (
    g_screen_board_width + g_screen_status_width * 0.5,
    g_screen_board_height * 0.2,
    g_screen_status_width * 0.5,
    g_screen_height * 0.1
)

g_status_other_first_rect = (
    g_screen_board_width,
    g_screen_board_height * 0.5,
    g_screen_status_width / 3.0,
    g_screen_board_height * 0.1
)

# Dice Image Area
g_dice_image_rect = (
    g_screen_board_width * 0.6,
    g_screen_board_height * 0.2,
    g_screen_board_width * 0.2,
    g_screen_board_height * 0.2,
)

# Game data
g_max_team_num = 4
g_max_marker_on_map_block = 3

assert 2 <= g_max_team_num <= 4
assert 1 <= g_max_marker_on_map_block <= 4

g_default_name = ["Steven", "Inseong", "Danny", "Paul"]
g_default_money = 500
g_tuition = 100

g_is_local_version = True

############################################################################
# Model Classes
############################################################################

class OlinopolyModel:
    def __init__(self):

        self.num_of_teams = g_max_team_num
        assert self.num_of_teams <= g_max_team_num

        # Current state of game board
        # 0: Wait for other player
        # 1: Ready for rolling dice
        # 2: Wait for choosing marker
        # N: ...
        self.current_state = 1

        self.current_team_number = 0

        self.my_team_number = 0

        self.completed_markers = []

        self.enable_mouseover_map_block_info = True
        self.mouseover_map_block = -1  # -1 for indicating not-showing
        self.map_block_info_game = GameDescrip(g_game_des_rect, "c", True)
        self.map_block_info_place = PlaceDescrip(g_place_des_rect, "c", True)

        self.dice_number = None

        # Set initial player data
        self.playerdata = []
        for i in range(self.num_of_teams):
            playerdata = PlayerData(g_default_name[i], g_default_money, i)
            self.playerdata.append(playerdata)


        ##############################
        # Create map blocks

        # Powerful feature of our code is that it is generic!

        self.map_blocks = []
        num = 0
        for i in range(4):    # 0 ~ 3 (bottom, left, top and right)
            init_x, init_y = g_map_block_initial_positions[i]

            for j in range(g_map_num_blocks_in_line - 1):    # 0 ~ n-2
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

        for i in range(self.num_of_teams):  # for each team
            visible = True if i == self.my_team_number else False
            for j in range(4):  # for each class
                init_x, init_y = g_marker_initial_positions[j]
                marker = Marker(
                    (init_x, init_y, g_screen_status_width / 4, g_screen_board_height * 0.2 / 2),
                    'i', visible, i, j, None
                )
                self.markers[i].append(marker)

        ##############################
        # Current turn information area
        self.current_turn_area = CurrentTurnArea(
            g_current_turn_area_rect, 'c', True
        )
        self.current_turn_area.font_pos = (
            g_current_turn_area_rect[0] + 10,
            g_current_turn_area_rect[1] + 10
        )

        ##############################
        # Create complete area

        self.complete_area = CompleteArea(
            g_complete_area_rect, 'c', True
        )

        ##############################
        # Create roll dice button

        self.button_roll_dice = Buttons.Button()

        ##############################
        # Create Olin Logo

        self.olin_logo = OlinLogo(
            g_olin_logo_rect, 'i', True
        )

        ##############################
        # Game Description

        self.game_descrip = GameDescrip(
            g_game_des_rect, 'c', True
        )

        ##############################
        # Place Description

        self.place_descrip = PlaceDescrip(
            g_place_des_rect, 'c', True
        )

        ##############################
        # Create Profile and status

        self.user_profiles = []
        self.user_status = []

        for i in range(4):
            profile = ProfileArea((0, 0, 0, 0), 'i', True, i)
            status = StatusArea((0, 0, 0, 0), 'c', True, i)
            self.user_profiles.append(profile)
            self.user_status.append(status)

        self.updateProfilePosition()

        ##############################
        # Create Rolling Dice "Animation"

        self.rolling_dice = DiceImage(
            g_dice_image_rect, 'i', True, self.dice_number
        )


    def setState(self, target_state):
        self.current_state = target_state

    def changeToNextTeam(self):
        logger.debug("Previous team: %d" % (self.current_team_number))

        if self.current_team_number == self.num_of_teams - 1:   # if: last team
            self.changeCurrentTeam(0)
        else:
            self.changeCurrentTeam(self.current_team_number + 1)    # change to next team

        logger.debug("Current team: %d" % (self.current_team_number))

    def changeCurrentTeam(self, target_team):
        self.current_team_number = target_team
        if g_is_local_version:
            self.my_team_number = self.current_team_number

        if g_is_local_version:
            self.updateProfilePosition()
        self.updateMarkerVisibility()

    def updateMarkerVisibility(self):
        for i in range(self.num_of_teams):
            for marker in self.markers[i]:
                if 0 <= marker.block_pos < g_map_num_blocks:
                    marker.is_visible = True
                # if marker is my marker
                elif marker.block_pos == None:
                    if i == self.my_team_number:
                        marker.is_visible = True
                    else:
                        marker.is_visible = False

    def moveMarker(self, team, player, target_pos, move_other_together=False):
        logger.debug("#########################")
        logger.debug("moveMarker() Enter")
        logger.debug("=== Input values ===")
        logger.debug("team    : %d" % (team))
        logger.debug("player  : %d" % (player))
        logger.debug("target  : %d" % (target_pos))
        logger.debug("together: %d" % (move_other_together))
        logger.debug("====================")

        if target_pos >= g_map_num_blocks:
            target_pos = -1 # -1 means completed
        else:
            # Check availabiltiy
            if len(self.map_blocks[target_pos].markers_on_block) == g_max_marker_on_map_block:
                logger.debug("Failed to move marker: max reached")
                logger.debug("moveMarker() Leave")
                logger.debug("#########################")
                return False

        prev_pos = self.markers[team][player].block_pos
        logger.debug("prev: %s" % (str(prev_pos)))

        self.markers[team][player].block_pos = target_pos
        self.markers[team][player].prev_block_pos = prev_pos

        if target_pos == -1:    # add to completed area
            current_len = len(self.completed_markers)
            if current_len < g_complete_area_max_in_row:
                x = g_complete_area_rect[0] + g_map_block_width / 2 * current_len
                y = g_complete_area_rect[1]
                w = g_complete_area_marker_width
                h = g_map_block_height
            else:
                x = g_complete_area_rect[0] + g_map_block_width * current_len
                y = g_complete_area_rect[1] + g_complete_area_rect[4] / 2
                w = g_complete_area_marker_width
                h = g_map_block_height
            self.markers[team][player].rect = (x, y, w, h)
            self.markers[team][player].reloadImage()
            self.completed_markers.append((team, player))

        else:   # add to current map block
            map_block = self.map_blocks[target_pos]
            markers = map_block.markers_on_block
            current_len = len(markers)

            # if there is another player's markers, they are caught by current marker
            if current_len > 0:
                if markers[0][0] != team:
                    markers = []
                    for marker in map_block.markers_on_block:
                        markers.append(marker)
                    for marker in markers:
                        t, p = marker
                        logger.debug("marker %d,%d is moved to the beginning" % (t, p))
                        prev = self.markers[t][p].block_pos
                        self.markers[t][p].block_pos = None

                        x, y = g_marker_initial_positions[p]
                        w = g_screen_status_width / 4
                        h = g_screen_board_height * 0.2 / 2
                        self.markers[t][p].rect = (
                            x, y, w, h
                        )
                        self.markers[t][p].reloadImage()

                        # remove other markers from the map block
                        self.map_blocks[prev].markers_on_block.remove([t, p])
                    self.updateMarkerVisibility()

            self.map_blocks[target_pos].markers_on_block.append([team, player])

            map_block = self.map_blocks[target_pos]
            markers = map_block.markers_on_block
            current_len = len(markers)

            # change x, y position of marker based on target map block
            logger.debug("current length of markers in the target map block: [%d]" % (current_len))
            for i in range(current_len):
                marker = markers[i]
                team, player = marker
                logger.debug("i: %d / t:%d, p:%d" % (i, team, player))

                x = map_block.rect[0] + (g_map_block_width / current_len) * i
                y = map_block.rect[1]

                self.markers[team][player].rect = (
                    x, y,
                    map_block.rect[2] / 2,
                    map_block.rect[3]
                )
                if self.markers[team][player].prev_block_pos == None:
                    self.markers[team][player].reloadImage()

        logger.debug("final target: %d" % (target_pos))


        if prev_pos == None:    # pay tuition
            self.playerdata[team].money -= g_tuition
        else:   # remove from previous map block
            self.map_blocks[prev_pos].markers_on_block.remove([team, player])

            # move others in the same map block
            if (move_other_together):
                logger.debug("other markers / len: %d" % (len(self.map_blocks[prev_pos].markers_on_block)))
                markers = []
                for marker in self.map_blocks[prev_pos].markers_on_block:
                    markers.append(marker)
                for marker in markers:
                    t, p = marker
                    logger.debug("t: %d / p: %d" % (t, p))
                    self.moveMarker(t, p, target_pos)
                #self.map_blocks.sort()

        logger.debug("moveMarker() Leave")
        logger.debug("#########################")

        return True

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
                    #logger.debug("next image: %s" % (img_path))
                    map_block.img = pygame.transform.scale(
                        pygame.image.load(img_path),
                        (map_block.rect[2] - g_line_width * 2, map_block.rect[3] - g_line_width * 2)
                    )

    def updateProfilePosition(self):
        other_profile_x = g_profile_other_first_rect[0]
        other_name_x = g_status_other_first_rect[0] + g_status_other_first_rect[2] * 0.1
        for i in range(self.num_of_teams):
            if i == self.my_team_number:
                self.user_profiles[i].rect = g_profile_main_rect
                self.user_status[i].rect = g_status_main_rect
                self.user_status[i].name_pos = (
                    g_status_main_rect[0] + g_status_main_rect[2] * 0.1,
                    g_status_main_rect[1] + g_status_main_rect[3] * 0.05
                )
                self.user_status[i].money_pos = (
                    g_status_main_rect[0] + g_status_main_rect[2] * 0.1,
                    g_status_main_rect[1] + g_status_main_rect[3]/2 + g_status_main_rect[3] * 0.05
                )
            else:
                x = other_profile_x
                y = g_profile_other_first_rect[1]
                w = g_profile_other_first_rect[2]
                h = g_profile_other_first_rect[3]
                self.user_profiles[i].rect = (x, y, w, h)

                x = other_profile_x
                y = g_status_other_first_rect[1]
                w = g_status_other_first_rect[2]
                h = g_status_other_first_rect[3]
                self.user_status[i].rect = (x, y, w, h)

                y = y + g_status_other_first_rect[3] * 0.05
                self.user_status[i].name_pos = (
                    other_name_x,
                    y
                )
                self.user_status[i].money_pos = (
                    other_name_x,
                    y + g_status_other_first_rect[3] * 0.5
                )

                other_profile_x += g_screen_status_width / (self.num_of_teams - 1)
                other_name_x += g_screen_status_width / (self.num_of_teams - 1)

            self.user_profiles[i].reloadImage()


class Drawable(object):
    def __init__(self, rect, c_or_i, is_visible):
        self.rect = rect    # rect is (x, y, width, height)
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

        self.prev_block_pos = None

        if self.c_or_i == "i":
            self.img = pygame.transform.scale(
                pygame.image.load(os.path.join(g_marker_image_dir_path, "%d%d.png" % (team, player))),
                (int(self.rect[2]),int(self.rect[3]))
            )
        else:
            self.img = None

    def reloadImage(self):
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join(g_marker_image_dir_path, "%d%d.png" % (self.team, self.player))),
            (int(self.rect[2]),int(self.rect[3]))
        )

    def pressed(self, x, y):
        if x > self.rect[0]:
            if y > self.rect[1]:
                if x < self.rect[0] + self.rect[2]:
                    if y < self.rect[1] + self.rect[3]:
                        logger.debug("Pressed: Marker %d %d" % (self.team, self.player))
                        return True
                    else:
                        return False
                else:
                   return False
            else:
               return False
        else:
            return False

class CurrentTurnArea(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(CurrentTurnArea, self).__init__(rect, c_or_i, is_visible)
        self.font = pygame.font.SysFont('Verdana', 16, False)
        self.font_pos = (0, 0)

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

class GameDescrip(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(GameDescrip, self).__init__(rect, c_or_i, is_visible)
        self.txt_list = []
        for i in range(g_map_num_blocks):
            if i in g_chance_card_position:
                path = os.path.join(g_map_block_game_txt_dir_path, "%d.txt" % (i))
            else:
                path = os.path.join(g_map_block_game_txt_dir_path, "%d.txt" % (i))
            text = open(path, 'r')
            txt = [str(txt).strip() for txt in text.readlines()]
            text.close()
            self.txt_list.append(txt)

#    def render_text_rect(self, msg, txt_font, txt_color, background_color):
#        for info_list in self.txt_list:
#            for lines in info_list:
#                if txt_font.size(lines)[0] > self.rect[2]:
#                    split_words = lines.split(' ')
#                    accum_line = " "
#                    for word in split_words:
#                        if txt_font.size(word)[0] < self.rect[2]:
#                            new_line = accum_line + word + " "
#                            if txt_font.size(new_line)[0] < self.rect[2]:
#                                accum_line = new_line
#                            else:
#                                self.txt_list.append(accum_line)
#                                accum_line = word + " "
#                            self.txt_list.append(accum_line)
#                        self.txt_list.append(accum_line)
#                    else:
#                        self.txt_list.append(accum_line)

class PlaceDescrip(Drawable):
    def __init__(self, rect, c_or_i, is_visible):
        super(PlaceDescrip, self).__init__(rect, c_or_i, is_visible)
        self.txt_list = []
        for i in range(g_map_num_blocks):
            if i in g_chance_card_position:
                path = os.path.join(g_map_block_olin_txt_dir_path, "%d.txt" % (i))
            else:
                path = os.path.join(g_map_block_olin_txt_dir_path, "%d.txt" % (i))
            text = open(path, 'r')
            txt = [str(txt).strip() for txt in text.readlines()]
            text.close()
            self.txt_list.append(txt)

class ProfileArea(Drawable):
    def __init__(self, rect, c_or_i, is_visible, team):
        super(ProfileArea, self).__init__(rect, c_or_i, is_visible)
        self.team = team
        self.reloadImage()

    def reloadImage(self):
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join(g_profile_dir_path, "t%d.png" % (self.team))),
            (int(self.rect[2]), int(self.rect[3]))
        )

class StatusArea(Drawable):
    def __init__(self, rect, c_or_i, is_visible, team):
        super(StatusArea, self).__init__(rect, c_or_i, is_visible)
        self.team = team
        self.font_name = pygame.font.SysFont('Verdana', 16, False)
        self.font_money = pygame.font.SysFont('Verdana', 16, False)
        self.name_pos = (0, 0)
        self.money_pos = (0, 0)

class PlayerData:
    def __init__(self, name, money, team):
        self.name = name
        self.money = money
        self.team = team

class DiceImage(Drawable):
    def __init__(self, rect, c_or_i, is_visible, dice_num):
        super(DiceImage, self).__init__(rect, c_or_i, is_visible)
        #self.dice_num = dice_num
        self.renderDiceImg(dice_num)
        #self.realDiceImg()

    def renderDiceImg(self, dice_num):
        if dice_num == None:
            self.img = pygame.transform.scale(
                pygame.image.load(os.path.join(g_dice_dir_path, "1.gif")),
                (int(self.rect[2]), int(self.rect[3])))
        else:
            self.img = pygame.transform.scale(
                pygame.image.load(os.path.join(g_dice_dir_path, "%d.gif" % (dice_num))),
                (int(self.rect[2]), int(self.rect[3]))
            )

#    def realDiceImg(self):
#        if self.dice_num == None:
#            self.img = pygame.transform.scale(
#                pygame.image.load(os.path.join(g_dice_dir_path, "0.gif")),
#                ((int(self.rect[2])), int(self.rect[3]))
#            )
#
#        else:
#            self.img = pygame.transform.scale(
#            pygame.image.load(os.path.join(g_dice_dir_path, "%d.gif" % (self.dice_num))),
#            (int(self.rect[2]), int(self.rect[3]))
#        )

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

        # Marker
        for i in range(self.model.num_of_teams):
            for marker in self.model.markers[i]:
                if marker.is_visible:
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

        # Current turn informatoin area
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.current_turn_area,
            1
        )
        msg = g_current_turn_str % (
            self.model.playerdata[self.model.current_team_number].name
        )
        current_turn = self.model.current_turn_area.font.render(
            msg,
            True,
            (10, 10, 115)
        )
        self.screen.blit(
            current_turn,
            self.model.current_turn_area.font_pos
        )

        # Complete area
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.complete_area.rect,
            1
        )

        # Button
        self.model.button_roll_dice.create_button(
            self.screen,
            (107,142,35),
            g_button_roll_dice_rect[0],
            g_button_roll_dice_rect[1],
            g_button_roll_dice_rect[2],
            g_button_roll_dice_rect[3],
            20,
            "Roll Dice!",
            (255,255,255)
        )

        # Olinopoly Logo
        self.screen.blit(
            self.model.olin_logo.img,
            (self.model.olin_logo.rect[0], self.model.olin_logo.rect[1])
        )

        # Mouseover Map Block Information
        if self.model.enable_mouseover_map_block_info:
            if self.model.mouseover_map_block >= 0:
                l = len(self.model.map_block_info_game.txt_list[self.model.mouseover_map_block])
                for i in range(l):
                    msg_game = self.model.map_block_info_game.txt_list[self.model.mouseover_map_block][i]
                    title_game = font_map_block_info.render(msg_game, True, (10, 10, 115))
                    self.screen.blit(title_game, (g_game_des_rect[0] + 5, g_game_des_rect[1] + 5 + i*20))

                l = len(self.model.map_block_info_place.txt_list[self.model.mouseover_map_block])
                for i in range(l):
                    msg_place = self.model.map_block_info_place.txt_list[self.model.mouseover_map_block][i]
                    title_place = font_map_block_info.render(msg_place, True, (10, 10, 115))
                    self.screen.blit(title_place, (g_place_des_rect[0] + 5, g_place_des_rect[1] + 5 + i*20))

                # Game Description
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(19, 110, 13),
                    self.model.game_descrip.rect,
                    1
                )

                # Place Description
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(19, 110, 13),
                    self.model.place_descrip.rect,
                    1
                )


        # Profile
        for i in range(self.model.num_of_teams):
            self.screen.blit(
                self.model.user_profiles[i].img,
                (self.model.user_profiles[i].rect[0], self.model.user_profiles[i].rect[1])
            )
            pygame.draw.rect(
                self.screen,
                pygame.Color(19, 110, 13),
                self.model.user_profiles[i].rect,
                1
            )
            pygame.draw.rect(
                self.screen,
                pygame.Color(19, 110, 13),
                self.model.user_status[i].rect,
                1
            )
            name = self.model.user_status[i].font_name.render(
                str(self.model.playerdata[i].name),
                True,
                (10, 10, 115)
            )
            money = self.model.user_status[i].font_money.render(
                str(self.model.playerdata[i].money),
                True,
                (10, 10, 115)
            )

            self.screen.blit(
                name,
                self.model.user_status[i].name_pos
            )
            self.screen.blit(
                money,
                self.model.user_status[i].money_pos
            )

        # Rolling Dice Image
        self.screen.blit(
            self.model.rolling_dice.img,
            (self.model.rolling_dice.rect[0], self.model.rolling_dice.rect[1])
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
        if g_debug_dice:
            n = int(raw_input("[DEBUG MODE] input dice num: "))
            self.model.dice_number = n
        else:
            self.model.dice_number = random.randint(1, 6)
        logger.debug("set dice num: %d" % (self.model.dice_number))

class DiceAnimationController:
    def __init__(self, model):
        self.model = model

    def randomDice(self):
        if self.randomdice_count == 0: # 0 : start animation
            current_random_dice_num = random.randint(1,6)
            self.model.rolling_dice.renderDiceImg(current_random_dice_num)

            self.random_state += 1
            if self.random_state == 10:
                self.randomdice_count = 1

        elif self.randomdice_count == 1: # 1 : stop animation and show real dice num
            current_random_dice_num = self.model.dice_number
            self.model.rolling_dice.renderDiceImg(current_random_dice_num)

############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    # Initialize screen
    size = (g_screen_width, g_screen_height)
    screen = pygame.display.set_mode(size)

    font_map_block_info = pygame.font.SysFont('Verdana', 16, False)
    font_temporary_dice = font_map_block_info

    # MVC objects
    model = OlinopolyModel()
    view = OlinopolyView(model, screen)
    controller_mouse = OlinopolyMouseController(model)
    controller_mouse_over = OlinopolyMouseOverController(model)
    controller_dice = OlinopolyDiceController(model)
    controller_dice_animation = DiceAnimationController(model)

    # initialize
    controller_dice_animation.randomdice_count = 1

    # Timer for events
    # 1 - Mouse over
    # 2 - Blinking SoftDsg
    # 3 - Random Dice Image
    pygame.time.set_timer(USEREVENT + 1, 500)
    pygame.time.set_timer(USEREVENT + 2, 300)
    pygame.time.set_timer(USEREVENT + 3, 250)

    running = True
    ####################
    # While start
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

            if event.type == USEREVENT + 1:
                controller_mouse_over.check()

            if event.type == USEREVENT + 2:
                model.blinkSoftDsg()

            if event.type == USEREVENT + 3:
                controller_dice_animation.randomDice()

            if event.type == MOUSEMOTION:
                controller_mouse.handleMouseEvent(event)

            if event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if model.current_state == 1 and model.button_roll_dice.pressed((x, y)):
                    controller_dice.rollDice()
                    controller_dice_animation.randomdice_count = 0
                    controller_dice_animation.random_state = 0
                    model.setState(2)
                elif model.current_state == 2:
                    result = False
                    #for player in model.markers[model.my_team_number]:
                    for player in model.markers[model.current_team_number]:
                        if player.pressed(x, y) and player.block_pos != -1:
                            team = player.team
                            player = player.player
                            logger.debug("Dice Num: %d" % (model.dice_number))
                            if model.markers[team][player].block_pos == None:
                                target_pos = model.dice_number
                            else:
                                target_pos = model.markers[team][player].block_pos + model.dice_number
                            result = model.moveMarker(
                                team, player, target_pos, True
                            )
                            break
                    if result:
                        model.setState(1)
                        # Change to next team
                        model.changeToNextTeam()

        view.draw()
        time.sleep(.001)
    # While end
    ####################
    pygame.quit()
