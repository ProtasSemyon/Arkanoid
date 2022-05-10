import json
import sys

import pygame

import colors
from entities.button import Button


class LevelScreen:
    cols = 4
    tile_size = (200, 200)

    def __init__(self, levels_file):
        try:
            file = open(levels_file, 'r')
        except IOError:
            print("Error")
            sys.exit()
        else:
            with file as json_file:
                self.levels_data = json.load(json_file)
        self.load_file = levels_file
        self.locked_img = pygame.image.load("images/lock.png")
        self.tiles = []
        self.active_tile_num = None
        self.__update()

    def draw(self, screen):
        for i in range(len(self.tiles)):
            self.tiles[i].draw(screen, i % self.cols * (self.tile_size[0] + 50) + 100,
                               i // self.cols * (self.tile_size[1] + 50) + 50)

    def is_active(self):
        for i in range(len(self.tiles)):
            if self.tiles[i].is_active() and self.levels_data[i]['condition'] == 'unlock':
                self.active_tile_num = i
                return True
        return False

    def get_active(self):
        return self.levels_data[self.active_tile_num]['level_config']

    def unlock(self, level_num):
        if len(self.levels_data) > level_num > 0:
            self.levels_data[level_num - 1]['condition'] = 'unlock'
            self.__update()
            with open(self.load_file, 'w') as load_file:
                json.dump(self.levels_data, load_file, indent=3)

    def __update(self):
        self.tiles = []
        for record in self.levels_data:
            if record['condition'] == 'unlock':
                self.tiles.append(
                    Button(self.tile_size[0], self.tile_size[1], colors.DARK_BLUE, colors.AQUA, str(record['number']),
                           colors.WHITE))
            else:
                self.tiles.append(
                    Button(self.tile_size[0], self.tile_size[1], colors.DARK_BLUE, colors.AQUA, "", colors.WHITE,
                           self.locked_img))

