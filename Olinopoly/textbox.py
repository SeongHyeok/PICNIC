# -*- coding: utf-8 -*-
"""
Created on Sun May  4 22:46:02 2014

@author: sim
"""

import pygame

class ChatBox():
    def __init__(self, rect, width = 1):
        self.rect = rect
        self.width = width

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

    def char_add(self, event):
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
        print s
        if len(s) > 0:
            for n, l in enumerate(s):
                if self.font.size(s[n:])[0] < self.rect[2]:
                    self.label = self.font.render(s[n:], 1, self.color)
                    break
        else:
            self.label = self.font.render(s, 1, self.color)

        self.string = ''.join(self.str_list)

class TextBox2:
    def __init__(self, rect, width=1):
        self.selected = False
        self.font_size = 15
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.str_list = []
        self.width = width
        self.color = (255,255,255)
        self.rect = rect
        self.string = ''.join(self.str_list)

    def char_add(self, event):
        '''modify string list based on event.key'''
        if event.key == pygame.K_BACKSPACE:
            if self.str_list:
                self.str_list.pop()
        elif event.key == pygame.K_RETURN:
            return ''.join(self.str_list)
        elif event.key in [pygame.K_TAB, pygame.K_KP_ENTER]:#unwanted keys
            return False
        elif event.key == pygame.K_DELETE:
            self.str_list = []
            return False
        else:
            char = event.unicode
            if char: #stop emtpy space for shift key adding to list
                self.str_list.append(char)

    def update(self, scr):

        if self.selected:
            width = 2
        else:
            width = self.width

        s = ''.join(self.str_list)
        if len(s) > 0:
            for n, l in enumerate(s):
                if self.font.size(s[n:])[0] < self.rect.width:
                    label = self.font.render(s[n:], 1, self.color)
                    break
        else:
            label = self.font.render(s, 1, self.color)

        self.string = ''.join(self.str_list)
        pygame.draw.rect(scr, self.color, self.rect, width)
        scr.blit(label, self.rect)

class Button:
    def __init__(self, text, rect):
        self.text = text
        self.is_hover = False
        self.default_color = (100,100,100)
        self.hover_color = (255,255,255)
        self.font_color = (0,0,0)
        self.rect = rect

    def label(self):
        '''button label font'''
        font = pygame.font.Font(None, 20)
        return font.render(self.text, 1, self.font_color)

    def color(self):
        '''change color when hovering'''
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color

    def update(self, screen):
        pygame.draw.rect(screen, self.color(), self.rect)
        screen.blit(self.label(), self.rect)

        #change color if mouse over button
        self.check_hover(pygame.mouse.get_pos())

    def check_hover(self, mouse):
        '''adjust is_hover value based on mouse over button - to change hover color'''
        if self.rect.collidepoint(mouse):
            self.is_hover = True
        else:
            self.is_hover = False

class Control:
    def __init__(self):
        pygame.init()
        self.screensize = (800,600)
        self.screen = pygame.display.set_mode(self.screensize)
        self.clock = pygame.time.Clock()
        self.gamestate = True
        self.input_entered = None

        self.textboxes = [
            TextBox(pygame.Rect(100,300, 300,25), 1),
            #TextBox(pygame.Rect(100,500, 300,25), 1)
        ]
        self.btn = Button('Submit', pygame.Rect(100,350, 100, 25))

    def update(self):
        self.screen.fill((0,0,0))
        for box in self.textboxes:
            box.update(self.screen)
        self.btn.update(self.screen)
        pygame.display.flip()
        #self.input_enetered = None


    def mainloop(self):
        while self.gamestate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = False
                elif event.type == pygame.KEYDOWN:
                    for box in self.textboxes:
                        if box.selected:
                            self.input_entered = box.char_add(event)
                            if self.input_entered:
                                print(self.input_entered)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for box in self.textboxes:
                            if box.rect.collidepoint(pygame.mouse.get_pos()):
                                box.selected = True
                            else:
                                box.selected = False
                            if self.btn.rect.collidepoint(pygame.mouse.get_pos()):
                                if box.string:
                                    print(box.string)
            self.update()
