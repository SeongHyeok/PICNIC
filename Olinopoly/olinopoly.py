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
import time
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import Buttons
import textbox

############################################################################
# Debug options
############################################################################

g_debug_dice = True

############################################################################
# Global variabless
############################################################################

MAPBLOCK_TYPE_LOCATION = 0
MAPBLOCK_TYPE_COURSE = 1
MAPBLOCK_TYPE_EVENT = 2
MAPBLOCK_TYPE_CHANCE = 3

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
g_screen_board_width = 700
g_screen_board_height = 700
g_screen_status_width = int(g_screen_board_width * 0.6)

g_screen_width = g_screen_board_width + g_screen_status_width   # DO NOT CHANGE
g_screen_height = g_screen_board_height # DO NOT CHANGE

g_line_width = 2

# Popup Screen
g_popup_screen_rect = (
    g_screen_width * 0.2,
    g_screen_height * 0.25,
    g_screen_width * 0.6,
    g_screen_height * 0.6
)

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
    g_screen_board_width * 0.15,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.35,
    g_screen_board_height * 0.25
)

# Place Description
g_place_des_rect = (
    g_screen_board_width * 0.5,
    g_screen_board_height * 0.6,
    g_screen_board_width * 0.35,
    g_screen_board_height * 0.25
)

# Chance Card
g_chance_card_num = 30
g_chance_card_position = [7, 13, 21, 29]

# Card Feature
g_location_position = [1, 5, 12, 16, 20, 22, 25, 28, 31] # 9
g_course_position = [2, 3, 11, 23, 30]  # 5
g_event_position = [4, 6, 8, 9, 10, 14, 15, 17, 18, 19, 24, 26, 27, 32, 33, 34] # 16
g_softdsg_card_position = [35]

g_tips_position = [6]
g_sibb_position = [8]
g_career_fair_position = [24]
g_study_abroad_position = [15]

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

# Chat Box Area
g_chat_box_rect = (
    g_screen_board_width,
    g_screen_board_height * 0.6,
    g_screen_status_width,
    g_screen_board_height * 0.35
)

# Text Box Area
g_text_box_rect = (
    g_screen_board_width,
    g_screen_board_height - g_map_block_height * 0.5,
    g_screen_status_width,
    g_map_block_height * 0.5
)

#Owned mapblock Area
g_owned_mapblock_size = (
    g_map_block_width*0.3,
    g_map_block_height*0.25
)


# Mapblocks and money

g_mapblock_price = [None, 10000, 10000, 10000, None, # ~  4
                    15000, None, None, None, None,   # ~  9
                    None, 15000, 23000, None, None,  # ~ 14
                    None, 21000, None, None, None,   # ~ 19
                    25000, None, 18000, 20000, None, # ~ 24
                    28000, None, None, 30000, None,  # ~ 29
                    25000, 28000, None, None, None, 30000]
g_mapblock_return = [None, 5000, 7000, 7000, None,   # ~  4
                     10000, None, None, None, None,  # ~  9
                     None, 10000, 18000, None, None, # ~ 14
                     None, 8000, None, None, 5000,   # ~ 19
                     15000, None, 13000, 15000, None,# ~ 24
                     16000, None, None, 15000, None, # ~ 29
                     20000, 14000, None, None, None, 20000]

g_mapblock_name = ["Start/End", "West Hall", "OIE", "Design Nature", "Study Break",
                   "Parcel B", "TIPS", "Chance", "SIBB", "Room Draw",
                   "Spring Formal", "UOCD", "Academic Center", "Chance", "Olin Van",
                   "Exchange Student", "Library", "Honor Code", "SERV", "Man Hall",
                   "East Hall", "Chance", "Dining Hall", "POE", "Career Fair",
                   "Parking lot B", "Ninja Hours", "Study Break", "LPB", "Chance",
                   "SCOPE", "The O", "Internship", "Graduation", "SERV donation", "Software Design"]

# Game data
g_max_team_num = 4
g_max_marker_on_one_map_block = 3

assert 2 <= g_max_team_num <= 4
assert 1 <= g_max_marker_on_one_map_block <= 4

g_default_name = ["Steven", "Inseong", "Danny", "Paul"]
g_default_money = 200000
g_tuition = 40000 / 2   # half tuition

g_max_popup_option_number = 4

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

        self.role_dice_only = False

        self.current_land_block = None

        self.was_chance = False

        self.bought_block = None
        self.possess_team = None
        self.owned_blocks = []

        self.updateOwnedMapblocks()
        # Popup dialog
        self.popup_state = False
        self.popup_option_area = []
        for i in range(g_max_popup_option_number):
            self.popup_option_area.append(None)
        self.popup_options = [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]
        self.popup_questions = [
            "Q: "
        ]
        self.popup_team = None  # team which made popup
        self.popup_player = None    # player which made popup

        self.winner = None

        # Set initial player data
        self.player_data = []
        for i in range(self.num_of_teams):
            player_data = PlayerData(g_default_name[i], g_default_money, i)
            self.player_data.append(player_data)

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
                    (x, y, g_map_block_width, g_map_block_height), 'i',
                    True, num, None, None
                )
                self.map_blocks.append(map_block_object)
                num += 1

        for i in range(0, len(self.map_blocks)):
            if (i in g_location_position) or (i in g_softdsg_card_position):
                self.map_blocks[i].type = MAPBLOCK_TYPE_LOCATION
            elif i in g_course_position:
                self.map_blocks[i].type = MAPBLOCK_TYPE_COURSE
            elif i in g_event_position:
                self.map_blocks[i].type = MAPBLOCK_TYPE_EVENT
            elif i in g_chance_card_position:
                self.map_blocks[i].type = MAPBLOCK_TYPE_CHANCE
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
        # Chat box

        self.chat_box = textbox.ChatBox(g_chat_box_rect, 1)

        ##############################
        # Text box

        self.text_box = textbox.TextBox(g_text_box_rect, 1)

        ##############################
        # Create Rolling Dice "Animation"

        self.rolling_dice = DiceImage(
            g_dice_image_rect, 'i', True, self.dice_number
        )

        ###############################




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

        self.current_land_block = None

        if target_pos >= g_map_num_blocks:
            target_pos = -1 # -1 means completed
        else:
            # Check availabiltiy
            if len(self.map_blocks[target_pos].markers_on_block) == g_max_marker_on_one_map_block:
                if self.map_blocks[target_pos].markers_on_block[0][0] == team:
                    logger.debug("Failed to move marker: max reached")
                    logger.debug("moveMarker() Leave")
                    logger.debug("#########################")
                    return False
            if len(self.map_blocks[target_pos].markers_on_block) > 0:
                if self.map_blocks[target_pos].markers_on_block[0][0] == team:
                    if not self.player_data[self.current_team_number].is_sibb:
                        logger.debug("is_sibb is False, so cannot piggy-back")
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
                y = g_complete_area_rect[1] + g_complete_area_rect[3] / 2
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

                    c = 's' if len(markers) > 1 else ''
                    self.add_system_msg("%s caught %s's marker%s." % (
                        self.get_current_player_name(), self.get_player_name(markers[0][0]), c)
                    )

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

            self.current_land_block = self.map_blocks[target_pos]

        logger.debug("final target: %d" % (target_pos))


        if prev_pos == None:    # pay tuition
            self.player_data[team].money -= g_tuition
            self.add_system_msg("%s paid tuition, %d." % (self.get_current_player_name(), g_tuition))
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

        self.check_winner()

        logger.debug("moveMarker() Leave")
        logger.debug("#########################")

        return True

    def check_winner(self):
        for i in range(self.num_of_teams):
            chk = True
            for j in range(4):
                if self.markers[i][j].block_pos != -1:
                    chk = False
                    break
            if chk:
                self.winner = i
                self.add_system_msg("%s is winner!!" % (self.get_player_name(i)))
                break

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

    def get_current_player_name(self):
            return self.get_player_name(self.current_team_number)

    def get_player_name(self, n):
        return self.player_data[n].name

    def add_system_msg(self, s):
        self.chat_box.add_sentence("Olinopoly- " + s)

    ###############################################
    # Implement Mapblock Features
    ###############################################

    def mapblockPopup(self, current_pos, current_pos_type, current_pos_team, current_pos_num, player):
        logger.debug("block type is: %d" % (current_pos_type))

        self.popup_state = True

        if (current_pos_type == MAPBLOCK_TYPE_LOCATION) or (current_pos_type == MAPBLOCK_TYPE_COURSE):
            if current_pos_team == None:
                self.popup_state = True
                self.popup_options = [
                    "Yes",
                    "No",
                ]
                self.popup_questions = ["Q: Would you like to buy for %d ?" % (g_mapblock_price[current_pos_num])]
            else:
                self.popup_state = False
                if current_pos_team != self.current_team_number:
                    # pay money
                    self.player_data[current_pos_team].money += g_mapblock_price[current_pos_num]
                    self.player_data[self.current_team_number].money -= g_mapblock_price[current_pos_num]
                    self.add_system_msg("%s paid %s, %d" % (
                            self.get_current_player_name(), self.get_player_name(current_pos_team), g_mapblock_price[current_pos_num]
                        )
                    )
        elif current_pos_type == MAPBLOCK_TYPE_EVENT:
            if current_pos_num == 4:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "You miss a turn.",
                    "Go take a study break!"]
                self.player_data[self.current_team_number].remaining_miss_turn = 1
            elif current_pos_num == 6:
                self.popup_options = ["Close"]
                if self.player_data[self.current_team_number].is_tips:
                    self.popup_questions = [
                        "You have already taken tips."]
                else:
                    self.popup_questions = [
                        "Congratulations.",
                        "You can now enter ManHall!"]
            elif current_pos_num == 8:
                self.popup_options = ["Close"]
                self.popup_questions = ["Now you can piggy-back your markers."]
                self.player_data[self.current_team_number].is_sibb = True
            elif current_pos_num == 9:
                self.popup_options = ["Roll Dice"]
                self.popup_questions = ["Roll the dice and earn times 5000"]
                self.player_data[self.current_team_number].is_one_more = True
                self.role_dice_only = True
            elif current_pos_num == 10:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "You lose money.",
                    "Go enjoy the spring formal."]
            elif current_pos_num == 14:
                self.popup_options = ["Take Olin Van!"]
                self.popup_questions = ["You can roll the dice one more time."]
                self.player_data[self.current_team_number].is_one_more = True
            elif current_pos_num == 15:
                self.popup_options = [
                    "Belgium",
                    "Korea",
                    "France",
                    "Singapore"]
                self.popup_questions = ["Choose a country to study abroad"]
            elif current_pos_num == 17:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "You got caught by the Honor Board!",
                    "You lose money."]
            elif current_pos_num == 18:
                self.popup_options = ["Collect Money"]
                self.popup_questions = [
                    "Congratulations!",
                    "You are the winner of the SERV money"]
            elif current_pos_num == 19:
                if self.player_data[self.current_team_number].is_tips:
                    self.player_data[self.current_team_number].is_one_more = True
                    self.popup_questions = [
                        "Welcome to ManHall Party!",
                        "Enjoy and roll the dice one more time!"]
                    self.popup_options = ["Whooray!!!! :-)"]
                else:
                    self.popup_questions = [
                        "You cannot enjoy ManHall Party",
                        "because you didn't take TIPS!"
                    ]
                    self.popup_options = ["Okay..... T.T"]
                # if landed on tips: has to pay but can party(roll dice one more time)
                # if did not land on tips: has to pay but cannot party
                self.player_data[self.current_team_number].money -= g_mapblock_return[19]
            elif current_pos_num == 24:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "You can now get a better internship"
                ]
            elif current_pos_num == 26:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "You miss a turn.",
                    "Go to NINJA hours."
                ]
                self.player_data[self.current_team_number].remaining_miss_turn = 1
            elif current_pos_num == 27:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "It's spring break!",
                    "Go enjoy your break for 2 turns."
                ]
                self.player_data[self.current_team_number].remaining_miss_turn = 2
            elif current_pos_num == 32:
                self.popup_options = ["Close"]
                self.popup_questions = [
                    "You got an internship!",
                    "Go do work for a turn and earn money."
                ]
                self.player_data[self.current_team_number].remaining_miss_turn = 1
            #elif current_pos_num == 33:
             #   if not senior
                #self.popup_options = ["Pay Senior"]
                #self.popup_questions = ["Give a present to the seniors"]
            #   if senior
                #self.popup_options = ["Graduate"]
                #self.popup_quesitons = ["Congratulations!", "You now have earned your bachelor's degree!"]
            elif current_pos_num == 34:
                self.popup_options = ["Donate"]
                self.popup_questions = ["Donate to SERV!"]

        elif current_pos_type == MAPBLOCK_TYPE_CHANCE:
            self.popup_options = ["Draw Chance Card"]
            self.popup_questions = ["Chance Card!"]

        self.popup_team = self.current_team_number
        self.popup_player = player

    def updateOwnedMapblocks(self):
        for i in range(g_max_team_num):
            if self.bought_block == None:
                pass
            else:
                if self.bought_block.num <= g_map_num_blocks_in_line - 1:
                    rect = (
                        self.bought_block.rect[0],
                        self.bought_block.rect[1] - g_map_block_height * 0.25,
                        g_map_block_width * 0.3,
                        g_map_block_height * 0.25
                    )
                elif g_map_num_blocks_in_line -1 < self.bought_block.num <= (g_map_num_blocks_in_line-1) * 2:
                    rect = (
                        self.bought_block.rect[0] + g_map_block_height,
                        self.bought_block.rect[1],
                        g_map_block_height * 0.25,
                        g_map_block_width * 0.3
                    )
                elif (g_map_num_blocks_in_line-1) * 2 <self.bought_block.num <= (g_map_num_blocks_in_line - 1) * 3:
                    rect = (
                        self.bought_block.rect[0],
                        self.bought_block.rect[1] + g_map_block_height,
                        g_map_block_width * 0.3,
                        g_map_block_height * 0.25
                    )
                elif (g_map_num_blocks_in_line - 1) * 3 < self.bought_block.num:
                    rect = (
                        self.bought_block.rect[0] - g_map_block_height * 0.25,
                        self.bought_block.rect[1],
                        g_map_block_height * 0.25,
                        g_map_block_width * 0.3
                    )
                owns_mapblock = OwnsMapblock(
                    rect,
                    'c',
                    True,
                    self.possess_team,
                    self.bought_block
                )
                self.owned_blocks.append(owns_mapblock)

class Drawable(object):
    def __init__(self, rect, c_or_i, is_visible):
        self.rect = rect    # rect is (x, y, width, height)
        self.c_or_i = c_or_i
        self.is_visible = is_visible

class MapBlock(Drawable):
    def __init__(self, rect, c_or_i, is_visible, num, team, mapblock_type):
        super(MapBlock, self).__init__(rect, c_or_i, is_visible)
        # map block number
        self.num = num

        # count markers that are on a block
        self.markers_on_block = []   # pairs of [team, player]

        # Which team possesses mapblock
        self.team = team

        #type of mapblock
        self.type = mapblock_type

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
            pygame.image.load(os.path.join(g_profile_dir_path, "%s.png" % (g_default_name[self.team]))),
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

        self.remaining_miss_turn = 0
        self.is_one_more = False

        # Map block switch
        self.is_tips = False
        self.is_sibb = False
        self.is_career_fair = False

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
            path = os.path.join(g_dice_dir_path, "%d.gif" % (dice_num))
            if os.path.exists(path):
                self.img = pygame.transform.scale(
                    pygame.image.load(path),
                    (int(self.rect[2]), int(self.rect[3]))
                )

class OwnsMapblock(Drawable):
    def __init__(self, rect, c_or_i, is_visible, team, bought_map_block):
        super(OwnsMapblock, self).__init__(rect, c_or_i, is_visible)
        self.team = team
        self.bought_map_block = bought_map_block
        if self.bought_map_block.num <= g_map_num_blocks_in_line - 1:
            self.rect = (
                    self.bought_map_block.rect[0],
                    self.bought_map_block.rect[1] - g_map_block_height * 0.25,
                    g_map_block_width * 0.3,
                    g_map_block_height * 0.25
            )
        elif g_map_num_blocks_in_line -1 < self.bought_map_block.num <= (g_map_num_blocks_in_line-1) * 2:
            self.rect = (
                self.bought_map_block.rect[0] + g_map_block_height,
                self.bought_map_block.rect[1],
                g_map_block_height * 0.25,
                g_map_block_width * 0.3
            )
        elif (g_map_num_blocks_in_line-1) * 2 <self.bought_map_block.num <= (g_map_num_blocks_in_line - 1) * 3:
            self.rect = (
                self.bought_map_block.rect[0],
                self.bought_map_block.rect[1] + g_map_block_height,
                g_map_block_width * 0.3,
                g_map_block_height * 0.25
            )
        elif (g_map_num_blocks_in_line - 1) * 3 < self.bought_map_block.num:
            self.rect = (
                self.bought_map_block.rect[0] - g_map_block_height * 0.25,
                self.bought_map_block.rect[1],
                g_map_block_height * 0.25,
                g_map_block_width * 0.3
            )



############################################################################
# View Classes
############################################################################

class OlinopolyView:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

        self.font_question = pygame.font.SysFont('Courier New', 27, True)
        self.font_option = pygame.font.SysFont('Arial', 30, True)

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
            self.model.get_current_player_name()
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
                str(self.model.player_data[i].name),
                True,
                (10, 10, 115)
            )
            money = self.model.user_status[i].font_money.render(
                str(self.model.player_data[i].money),
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

        # Chat box
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.chat_box.rect,
            self.model.chat_box.width
        )
        for i in range(len(self.model.chat_box.str_list)):
            sentence = self.model.chat_box.font.render(
                self.model.chat_box.str_list[i],
                True,
                (10, 10, 115)
            )
            self.screen.blit(sentence, (self.model.chat_box.rect[0] + 5, self.model.chat_box.rect[1] + 5 + i * 24))

        # Text box
        pygame.draw.rect(
            self.screen,
            pygame.Color(19, 110, 13),
            self.model.text_box.rect,
            self.model.text_box.width
        )
        rect = (
            self.model.text_box.rect[0] + 5,
            self.model.text_box.rect[1] + 5,
            self.model.text_box.rect[2],
            self.model.text_box.rect[3],
        )
        if self.model.text_box.label:
            self.screen.blit(self.model.text_box.label, rect)

        # Rolling Dice Image
        self.screen.blit(
            self.model.rolling_dice.img,
            (self.model.rolling_dice.rect[0], self.model.rolling_dice.rect[1])
        )

        # Owned Mapblock
        for i in range(len(self.model.owned_blocks)):
            if self.model.owned_blocks[i].team == 0:
                fill_color = pygame.Color(250, 246, 2)
            elif self.model.owned_blocks[i].team == 1:
                fill_color = pygame.Color(57, 154, 250)
            elif self.model.owned_blocks[i].team == 2:
                fill_color = pygame.Color(250, 153, 57)
            elif self.model.owned_blocks[i].team == 3:
                fill_color = pygame.Color(7, 224, 83)

            pygame.draw.rect(
                self.screen,
                fill_color,
                self.model.owned_blocks[i].rect,
                0
            )


        if not self.model.popup_state:
            pygame.display.flip()

    def drawPopup(self):
        popup_surface = pygame.Surface((int(g_popup_screen_rect[2]), int(g_popup_screen_rect[3])))
        popup_surface.fill(pygame.Color(149, 186, 245))

        #question = "Q: %s, what will you do?" % (self.model.get_current_player_name())

        # maximum number of option: 4
        assert len(self.model.popup_options) <= g_max_popup_option_number

        top = g_popup_screen_rect[3] * 0.1
        left = g_popup_screen_rect[2] * 0.1

        # Display question
        for i in range(len(self.model.popup_questions)):
            text_surface = self.font_question.render(self.model.popup_questions[i], 1, (0, 50, 100))
            text_rect = text_surface.get_rect()
            text_rect.top = top
            text_rect.left = left
            popup_surface.blit(text_surface, text_rect)

            top += g_popup_screen_rect[3] * 0.1

        top += g_popup_screen_rect[3] * 0.15
        left = g_popup_screen_rect[2] * 0.15

        # Display options
        for i in range(len(self.model.popup_options)):
            text_surface = self.font_option.render(self.model.popup_options[i], 1, (0, 50, 100))
            text_rect = text_surface.get_rect()
            text_rect.top = top
            text_rect.left = left

            """pygame.draw.rect(
                self.screen,
                pygame.Color(19, 110, 13),
                (g_popup_screen_rect[0] + left,
                 g_popup_screen_rect[1] + top,
                 g_popup_screen_rect[2] * 0.7,
                 pygame.font.Font.get_linesize(self.font_option) * 1.5
                 ),
                2
            )"""
            rect = (left,
                    top,
                    g_popup_screen_rect[2] * 0.7,
                    pygame.font.Font.get_linesize(self.font_option) * 1.5
            )
            self.model.popup_option_area[i] = rect
            pygame.draw.rect(
                popup_surface,
                pygame.Color(19, 110, 13),
                rect,
                2
            )

            top += pygame.font.Font.get_linesize(self.font_option) + g_popup_screen_rect[3] * 0.05

            popup_surface.blit(text_surface, text_rect)

        popup_rect = popup_surface.get_rect()
        popup_rect.centerx = g_popup_screen_rect[0] + g_popup_screen_rect[2] / 2
        popup_rect.centery = g_popup_screen_rect[1] + g_popup_screen_rect[3] / 2
        self.screen.blit(popup_surface, popup_rect)

        #pygame.display.update()
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

class MapBlockFeatureController:
    def __init__(self, model):
        self.model = model

    def buyMapBlock(self):
        self.model.current_land_block.team = self.model.popup_team
        self.model.possess_team = self.model.popup_team
        self.model.bought_block = self.model.current_land_block
        self.model.updateOwnedMapblocks()
        self.model.player_data[self.model.popup_team].money -= g_mapblock_price[self.model.current_land_block.num]

    def drawChanceCard(self):
        self.model.popup_state = True
        self.model.popup_options = ["Close"]

        chance_card_num = random.randint(0, 1)
        if chance_card_num == 0:
            self.model.popup_questions = [
                "Better luck next time"
            ]
        elif chance_card_num == 1:
            self.model.popup_questions = [
                "I'm sorry.",
                "You miss a turn."
            ]
            self.model.player_data[self.model.popup_player].remaining_miss_turn = 1

        self.model.was_chance = True

############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    # Initialize screen
    size = (g_screen_width, g_screen_height)
    screen = pygame.display.set_mode(size)

    font_map_block_info = pygame.font.SysFont('Tahoma', 14, False)
    font_temporary_dice = font_map_block_info

    # MVC objects
    model = OlinopolyModel()
    view = OlinopolyView(model, screen)
    controller_mouse = OlinopolyMouseController(model)
    controller_mouse_over = OlinopolyMouseOverController(model)
    controller_dice = OlinopolyDiceController(model)
    controller_dice_animation = DiceAnimationController(model)
    controller_mapblock_possess = MapBlockFeatureController(model)

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

        # Check missing turn
        if model.player_data[model.current_team_number].remaining_miss_turn > 0:
            model.player_data[model.current_team_number].remaining_miss_turn -= 1
            model.add_system_msg("%s is missing a turn." % (model.get_current_player_name()))
            model.changeToNextTeam()

        if not model.winner:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    break

                if model.popup_state:
                    if event.type == MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        logger.debug("Click when popup - x: %d / y: %d" % (x, y))

                        option_clicked = False
                        for i in range(len(model.popup_options)):
                            left = g_popup_screen_rect[0] +  model.popup_option_area[i][0]
                            right = g_popup_screen_rect[0] + model.popup_option_area[i][0] + model.popup_option_area[i][2]
                            top = g_popup_screen_rect[1] + model.popup_option_area[i][1]
                            bottom = g_popup_screen_rect[1] + model.popup_option_area[i][1] + model.popup_option_area[i][3]
                            if left < x < right:
                                if top < y < bottom:
                                    logger.debug("Clicked popup option: %d" % (i))
                                    model.popup_state = False
                                    option_clicked = True
                                    break
                        if option_clicked:
                            # Check clicked option from popup and do something
                            logger.debug("popup block info- num:%d, type:%d" % (model.current_land_block.num, model.current_land_block.type))

                            if (model.current_land_block.type == MAPBLOCK_TYPE_LOCATION) or (model.current_land_block.type == MAPBLOCK_TYPE_COURSE):
                                if i == 0:
                                    controller_mapblock_possess.buyMapBlock()
                                    model.add_system_msg("%s bought '%s'" % (
                                        model.get_player_name(model.popup_team),
                                        g_mapblock_name[model.current_land_block.num])
                                    )
                            elif model.current_land_block.type == MAPBLOCK_TYPE_EVENT:
                                if model.current_land_block.num == 15:  # Study Abroad - Exchange student
                                    if i == 0: # Belguim
                                        study_abroad_num = random.randint(1, 3)
                                    elif i == 1: # Korea
                                        study_abroad_num = random.randint(3, 6)
                                    elif i == 2: # France
                                        study_abroad_num = random.randint(2, 4)
                                    elif i == 3: # Singapore
                                        study_abroad_num = random.randint(1, 5)
                                    logger.debug("Study abroad num: %d" % (study_abroad_num))
                                    t = model.popup_team
                                    p = model.popup_player
                                    target = model.markers[t][p].block_pos + study_abroad_num
                                    logger.debug("Move marker %d, %d to %d" % (t, p, target))
                                    model.moveMarker(t, p, target, True)

                            elif model.current_land_block.type == MAPBLOCK_TYPE_CHANCE:
                                if i == 0:
                                    if model.was_chance:
                                        model.popup_state = False
                                        model.was_chance = False
                                    else:
                                        controller_mapblock_possess.drawChanceCard()

                else:
                    if event.type == USEREVENT + 1:
                        controller_mouse_over.check()

                    if event.type == USEREVENT + 2:
                        model.blinkSoftDsg()

                    if event.type == USEREVENT + 3:
                        controller_dice_animation.randomDice()

                    # Keyboard input --> Text box
                    if event.type == pygame.KEYDOWN:
                        r = model.text_box.add_char(event)
                        if r:
                            logger.debug("char_add result: %s", r)
                            model.chat_box.add_sentence("[%s] %s" % (model.get_current_player_name(), r))
                            model.text_box.str_list = []
                        model.text_box.update()

                    if event.type == MOUSEMOTION:
                        controller_mouse.handleMouseEvent(event)

                    if event.type == MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        if model.current_state == 1 and model.button_roll_dice.pressed((x, y)):
                            controller_dice.rollDice()
                            controller_dice_animation.randomdice_count = 0
                            controller_dice_animation.random_state = 0
                            logger.debug("role_dice_only: %s" % (model.role_dice_only))
                            if model.role_dice_only:
                                logger.debug("popup block info- num:%d, type:%d" % (model.current_land_block.num, model.current_land_block.type))
                                model.role_dice_only = False
                                if model.current_land_block.type == MAPBLOCK_TYPE_EVENT:
                                    if model.current_land_block.num == 9:
                                        logger.debug("it was roomdraw.")
                                        plus = model.dice_number * 5000
                                        model.player_data[model.current_team_number].money += plus
                                        model.add_system_msg("%s earned money, %d." %(model.get_current_player_name(), plus))
                                        model.changeToNextTeam()
                            else:
                                model.setState(2)
                                logger.debug("Set state 2")
                        elif model.current_state == 2 and controller_dice_animation.randomdice_count == 1:
                            result = False
                            for player in model.markers[model.my_team_number]:
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

                                    if model.current_land_block:    # if land block is map block (it it sen in moveMarker())
                                        logger.debug("current_land_block- num:%s team:%s" % (
                                            str(model.current_land_block.num), str(model.current_land_block.team)
                                        ))
                                        # Enable map block switch
                                        n = model.current_land_block
                                        if n in g_tips_position:
                                            model.player_data[team].is_tips = True
                                            logger.debug("is_tips is ON")
                                        if n in g_sibb_position:
                                            model.player_data[team].is_sibb = True
                                            logger.debug("is_sibb is ON")
                                        if n in g_career_fair_position:
                                            model.player_data[team].is_career_fair = True
                                            logger.debug("is_career_fair is ON")
                                        model.mapblockPopup(
                                            model.current_land_block,
                                            model.current_land_block.type,
                                            model.current_land_block.team,
                                            model.current_land_block.num,
                                            player
                                        )
                                        if n in g_study_abroad_position:
                                            model.moveMarker(team, player, model.current_land_block.num)

                                    break
                            if result:
                                model.setState(1)
                                if model.player_data[model.current_team_number].is_one_more:
                                    model.player_data[model.current_team_number].is_one_more = False
                                else:
                                    # Change to next team
                                    model.changeToNextTeam()

        view.draw()
        if model.popup_state:
            view.drawPopup()

        time.sleep(.001)
    # While end
    ####################
    pygame.quit()
