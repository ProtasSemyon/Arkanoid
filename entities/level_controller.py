import pygame
import json
import sys

import colors
from entities.button import Button
from utilities import *


class Tile:
    pass


class Level(pygame.Surface):
    def __init__(self, size, bg_img, level_file):
        super().__init__(size)
        # try:
        #     file = open(level_file, 'r')
        # except IOError:
        #     print("Error")
        #     sys.exit()
        # else:
        #     with file as json_file:
        #         self.level_data = json.load(json_file)
        self.bg_img = bg_img
        self.score = 0
        self.top_bar = pygame.Surface((size[0], 100))
        self.pause_button = Button(100, 100, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load('images/PAUSE.png'))

    def draw(self, screen):
        self.blit(pygame.transform.scale(self.bg_img, self.get_size()), (0, 0))
        self.update()
        screen.blit(self, (0, 0))

    def update(self):
        self.__update_top_bar()

    def getScore(self):
        return self.score

    def __update_top_bar(self):
        font = pygame.font.SysFont('Algerian', 75)
        score_text = font.render('Score: ' + str(self.score), False, colors.WHITE)
        self.top_bar.fill(colors.DARK_BLUE)
        self.top_bar.blit(score_text, left(self.top_bar.get_size(), score_text.get_size()))
        self.pause_button.draw(self.top_bar, *right(self.top_bar.get_size(), self.pause_button.get_size()))
        self.blit(self.top_bar, (0, 0))

    def __update_level(self):
        pass

    def is_pause_active(self):
        return self.pause_button.is_active()