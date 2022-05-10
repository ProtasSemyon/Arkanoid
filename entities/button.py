import pygame
from utilities import *


class Button:
    def __init__(self, width, height, inactive_color, active_color, text, text_color, image=None):
        self.width, self.height = width, height
        self.inactive_color, self.active_color = inactive_color, active_color
        font = pygame.font.SysFont("Arial", 75)
        self.text = font.render(text, False, text_color)
        self.image = image
        self.pos = (0, 0)

    def draw(self, screen, x_pos, y_pos):
        self.pos = (x_pos, y_pos)
        mouse_pos = pygame.mouse.get_pos()
        if point_in_box(self.pos, (self.width, self.height), mouse_pos):
            pygame.draw.rect(screen, self.active_color, (x_pos, y_pos, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x_pos, y_pos, self.width, self.height))
        center_pos = center((self.width, self.height), self.text.get_size())
        screen.blit(self.text, (center_pos[0] + x_pos, center_pos[1] + y_pos))
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            screen.blit(self.image, self.pos)

    def is_active(self):
        mouse_pos = pygame.mouse.get_pos()
        return point_in_box(self.pos, (self.width, self.height), mouse_pos)

    def get_size(self):
        return self.width, self.height




