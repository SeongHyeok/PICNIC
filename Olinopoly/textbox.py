# -*- coding: utf-8 -*-
"""
Created on Sun May  4 22:46:02 2014

@author: sim
"""

import pygame

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatBox():
    def __init__(self, rect, width = 1):
        self.rect = rect
        self.width = width

        self.font_size = 16
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.max_lines = 11
        self.str_list = []
        self.color = (0, 0, 0)

    def add_sentence(self, s):
        if len(self.str_list) == self.max_lines:
            self.str_list = self.str_list[1:]
        self.str_list.append(s)
        logger.debug("str_list: %s" %(self.str_list))

class TextBox():
    def __init__(self, rect, width = 1):
        self.rect = rect
        self.width = width

        self.font_size = 18
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.str_list = []
        self.color = (0, 0, 0)
        self.string = ''.join(self.str_list)
        self.label = None

    def add_char(self, event):
        '''modify string list based on event.key'''
        if event.key == pygame.K_BACKSPACE:
            if self.str_list:
                self.str_list.pop()
        elif event.key == pygame.K_RETURN:
            return ''.join(self.str_list)
        elif event.key in [pygame.K_TAB, pygame.K_KP_ENTER]: # unwanted keys
            return False
        elif event.key == pygame.K_DELETE:
            self.str_list = []
            return False
        else:
            char = event.unicode
            if char: # stop emtpy space for shift key adding to list
                self.str_list.append(char)

    def update(self):
        s = ''.join(self.str_list)
        if len(s) > 0:
            for n, l in enumerate(s):
                if self.font.size(s[n:])[0] < self.rect[2]:
                    self.label = self.font.render(s[n:], 1, self.color)
                    break
        else:
            self.label = self.font.render(s, 1, self.color)

        self.string = ''.join(self.str_list)