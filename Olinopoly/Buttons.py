# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

pygame.init()

# [TODO] Improve button

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1,3):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print "Some button was pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


 #msg = "Dice number: %d" % (self.model.dice_number)
  #              w, h = font_temporary_dice.size(msg)
   #             title = font_temporary_dice.render(msg, True, (0, 0, 0))
    #            self.screen.blit(
     #               title,
      #              (g_button_rect[0],
       #              g_button_rect[1] - g_button_rect[3] - 10 + g_button_rect[3]/2
        #             )
         #       )
            #pygame.draw.rect(
             #   self.screen,
              #  pygame.Color(0, 0, 0),
               # (g_button_rect[0],
                # g_button_rect[1] - g_button_rect[3] - 10,
                # g_button_rect[2] + w,
                # g_button_rect[3]/5 + h
                 #),
               # 1
            #)
