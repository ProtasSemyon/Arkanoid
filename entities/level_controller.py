import json
import sys

import pygame

import colors
from entities.button import Button
from utilities import *


class Bonus:
    def __init__(self, pos):
        self.img = None
        self.active = False
        self.drop_speed = 0
        self.pos = pos
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def draw(self, screen):
        screen.blit(self.img, (self.pos_x, self.pos_y))

    def update(self):
        self.pos_y += self.drop_speed

    def activate(self):
        self.active = True


class IncreaseBoard(Bonus):
    def __init__(self, pos):
        super().__init__(pos)
        self.img = pygame.transform.scale(pygame.image.load('images/increaseboard.png'), (100, 100))
        self.drop_speed = 3


class Tile(pygame.Rect):
    def __init__(self, x_pos, y_pos, hp):
        super().__init__(x_pos, y_pos, 150, 50)
        self.bonus = None
        self.hp = hp
        self.active = True

    def draw(self, screen):
        pygame.draw.rect(screen, ((50 + self.hp * 60) * (self.hp % 3) % 256, (50 + self.hp * 60) * (self.hp % 3 + 1)
                                  % 256, (50 + self.hp * 60) * (self.hp % 3 + 2) % 256), self)

    def hit(self):
        self.hp -= 1
        if self.hp == 0:
            self.active = False
            self.drop_bonus()

    # TODO: bonus after die
    def add_bonus(self, bonus: Bonus):
        self.bonus = bonus

    def drop_bonus(self):
        if self.bonus is not None:
            self.bonus.activate()


class Ball:
    def __init__(self, x_pos, y_pos, dx, dy, screen_width, screen_height, top_padding):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_padding = top_padding
        # ball parameters
        self.radius = 15
        self.speed = 5
        self.dx, self.dy = dx, dy
        rect_side = self.radius * 2 ** 0.5
        self.rect = pygame.Rect(0, 0, rect_side, rect_side)
        self.rect.center = (x_pos, y_pos)
        self.active = True

    def change_radius(self, dr):
        self.radius += dr
        rect_side = self.radius * 2 ** 0.5
        self.rect = pygame.Rect(self.rect.left, self.rect.top, rect_side, rect_side)

    def change_speed(self, ds):
        self.speed += ds

    def collide(self, rect):
        return self.rect.colliderect(rect)

    def reflect_x(self):
        self.dx = -self.dx

    def reflect_y(self):
        self.dy = -self.dy

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, colors.WHITE, self.rect.center, self.radius)

    def update(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

        if self.rect.centerx < self.radius:
            self.dx = -self.dx
            self.rect.centerx = self.radius

        if self.rect.centerx > self.screen_width - self.radius:
            self.dx = -self.dx
            self.rect.centerx = self.screen_width - self.radius

        if self.rect.centery < self.radius + self.top_padding:
            self.dy = -self.dy
            self.rect.centery = self.radius + self.top_padding

        if self.rect.centery > self.screen_height:
            print("bonk")
            self.active = False

    def detect_collision(self, rect):
        if not self.collide(rect):
            return False
        if self.dx > 0:
            delta_x = self.rect.right - rect.left
        else:
            delta_x = rect.right - self.rect.left
        if self.dy > 0:
            delta_y = self.rect.bottom - rect.top
        else:
            delta_y = rect.bottom - self.rect.top

        if abs(delta_x - delta_y) < 10:
            self.dx, self.dy = -self.dx, -self.dy
        elif delta_x > delta_y:
            self.dy = -self.dy
        elif delta_y > delta_y:
            self.dx = -self.dx
        return True


class Player:
    def __init__(self, color, board_speed, screen_width, screen_height, top_padding, tiles):
        # screen settings
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_padding = top_padding

        # board settings
        self.board = pygame.Rect(500, 900, 250, 50)
        self.color = color
        self.board_speed = board_speed

        # balls
        self.balls = []
        self.balls.append(Ball(self.board.centerx, self.board.top - 20, 1,
                               -1, screen_width, screen_height, top_padding))
        self.tiles = tiles
        self.score = 0
        self.active = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.board)
        for ball in self.balls:
            if ball.active:
                ball.draw(screen)

    def update(self):
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_a]:
            self.__left()
        if key_press[pygame.K_d]:
            self.__right()

        for ball in self.balls:
            if not ball.active:
                self.balls.remove(ball)

        for ball in self.balls:
            if ball.active:
                ball.update()

        for ball in self.balls:
            ball.detect_collision(self.board)
            for tile in self.tiles:
                if ball.detect_collision(tile):
                    tile.hit()
                    self.score += 10

        if len(self.balls) == 0:
            self.active = False

    def __left(self):
        if self.board.left - self.board_speed > 0:
            self.board.left -= self.board_speed

    def __right(self):
        if self.board.right + self.board_speed < 1250:
            self.board.right += self.board_speed

    def increase_board(self, ds):
        self.board.w += ds


class Level(pygame.Surface):
    cols = 6

    def __init__(self, size, bg_img, level_file, win_func, lose_func):
        super().__init__(size)
        try:
            file = open(level_file, 'r')
        except IOError:
            print("Error")
            sys.exit()
        else:
            with file as json_file:
                level_data = json.load(json_file)
                self.bonus_list = []
                self.tiles = self.__get_tile(level_data['tiles'])
                self.number = level_data['num']
        self.bg_img = bg_img
        self.top_bar = pygame.Surface((size[0], 100))
        self.pause_button = Button(100, 100, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE,
                                   pygame.image.load('images/PAUSE.png'))
        self.win_func = win_func
        self.lose_func = lose_func
        self.finish = False
        self.player = Player(colors.ORANGE, 10, *size, 100, self.tiles)

    def draw(self, screen):
        self.blit(pygame.transform.scale(self.bg_img, self.get_size()), (0, 0))
        self.update()
        screen.blit(self, (0, 0))

    def update(self):
        self.__update_top_bar()
        self.__update_level()
        if self.finish:
            self.win_func(self.player.score)

    def getScore(self):
        return self.player.score

    def __update_top_bar(self):
        font = pygame.font.SysFont('Algerian', 60)
        score_text = font.render('Score: ' + str(self.player.score), False, colors.WHITE)
        level_text = font.render('Level ' + str(self.number), False, colors.WHITE)
        self.top_bar.fill(colors.DARK_BLUE)
        self.top_bar.blit(score_text, left(self.top_bar.get_size(), score_text.get_size()))
        self.top_bar.blit(level_text, center(self.top_bar.get_size(), score_text.get_size()))
        self.pause_button.draw(self.top_bar, *right(self.top_bar.get_size(), self.pause_button.get_size()))
        self.blit(self.top_bar, (0, 0))

    def __update_level(self):
        if len(self.tiles) == 0:
            self.finish = True
        for tile in self.tiles:
            if tile.active:
                tile.draw(self)
            else:
                self.tiles.remove(tile)

        if self.player.active:
            self.player.update()
            self.player.draw(self)
        else:
            self.lose_func()

        for bonus in self.bonus_list:
            if bonus.active:
                bonus.update()
                bonus.draw(self)

    def is_pause_active(self):
        return self.pause_button.is_active()

    def __get_tile(self, tile_data):
        tile_list = []
        for tile in tile_data:
            tile_list.append(Tile(50 + tile['pos'] % self.cols * 200, 150 + tile['pos'] // self.cols * 100,
                                  tile['hp']))
            tile_bonus = self.__create_bonus(tile['bonus'], tile_list[-1].center)
            tile_list[-1].add_bonus(tile_bonus)
            self.bonus_list.append(tile_bonus)
        return tile_list

    @staticmethod
    def __create_bonus(bonus_name: str, pos) -> Bonus:
        new_bonus = None
        if bonus_name == 'increaseboard':
            new_bonus = IncreaseBoard(pos)
        return new_bonus
