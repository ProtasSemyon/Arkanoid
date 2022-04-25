import enum
import sys

import pygame
import os
import colors

from entities.button import Button
from entities.level_controller import Level
from entities.level_screen import LevelScreen
from utilities import center

pygame.font.init()
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1250, 1000
FPS = 60
clock = pygame.time.Clock()

MAIN_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")

BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "background.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))


class LevelState(enum.Enum):
    PLAY = 0
    RETRY = 1
    EXIT = 2


def pause_level():
    transparent_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    transparent_surf.fill(colors.WHITE)
    transparent_surf.set_alpha(3)

    menu_surf = pygame.Surface((350, 500))
    menu_surf.fill(colors.DARK_BLUE2)

    play_button = Button(250, 100, colors.DARK_BLUE, colors.AQUA, "Play", colors.WHITE)
    retry_button = Button(250, 100, colors.DARK_BLUE, colors.AQUA, "Retry", colors.WHITE)
    exit_button = Button(250, 100, colors.DARK_BLUE, colors.AQUA, "Exit", colors.WHITE)

    run = True

    while run:
        pygame.display.update()
        MAIN_SCREEN.blit(transparent_surf, (0, 0))
        MAIN_SCREEN.blit(menu_surf, (450, 300))

        play_button.draw(MAIN_SCREEN, 500, 350)
        retry_button.draw(MAIN_SCREEN, 500, 500)
        exit_button.draw(MAIN_SCREEN, 500, 650)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_active():
                    return LevelState.PLAY
                if retry_button.is_active():
                    return LevelState.RETRY
                if exit_button.is_active():
                    return LevelState.EXIT
    clock.tick(FPS)


class GameController:
    def __init__(self, unlock_func):
        self.run = True
        self.font = pygame.font.SysFont('Algerian', 75)
        self.clock = clock
        self.unlock = unlock_func

    def win_level(self, level_score, current_level):
        self.run = False
        self.unlock(current_level + 1)

        transparent_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        transparent_surf.fill(colors.DARK_BLUE)
        transparent_surf.set_alpha(3)

        win_text_1 = self.font.render('You win!', False, colors.GREEN)
        win_text_2 = self.font.render('Youre score is ' + str(level_score), False, colors.GREEN)

        run = True

        while run:
            pygame.display.update()
            MAIN_SCREEN.blit(transparent_surf, (0, 0))
            text_center_1 = center((SCREEN_WIDTH, SCREEN_HEIGHT), win_text_1.get_size())
            text_center_2 = center((SCREEN_WIDTH, SCREEN_HEIGHT), win_text_2.get_size())

            MAIN_SCREEN.blit(win_text_1, (text_center_1[0], text_center_1[1] - win_text_1.get_size()[1]))
            MAIN_SCREEN.blit(win_text_2, (text_center_2[0], text_center_2[1] + win_text_2.get_size()[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_SPACE]:
                run = False

    def lose_level(self):
        self.run = False

        transparent_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        transparent_surf.fill(colors.DARK_BLUE)
        transparent_surf.set_alpha(3)

        lose_text = self.font.render("You lose!" + str(), False, colors.RED)

        run = True

        while run:
            pygame.display.update()
            MAIN_SCREEN.blit(transparent_surf, (0, 0))
            MAIN_SCREEN.blit(lose_text, center((SCREEN_WIDTH, SCREEN_HEIGHT), lose_text.get_size()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_SPACE]:
                run = False

    def start_level(self, level_file):
        level = Level((SCREEN_WIDTH, SCREEN_HEIGHT), BG, level_file, self.win_level, self.lose_level)

        while self.run:
            pygame.display.update()
            level.draw(MAIN_SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if level.is_pause_active():
                        state = pause_level()
                        if state == LevelState.RETRY:
                            level = Level((SCREEN_WIDTH, SCREEN_HEIGHT), BG, level_file, self.win_level, self.lose_level)
                        elif state == LevelState.EXIT:
                            self.run = False
        self.run = True
        clock.tick(FPS)


def select_level():
    level_screen = LevelScreen("configs/level_state.json")
    game_controller = GameController(level_screen.unlock)
    back_button = Button(150, 150, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load(
        "images/back_button.png"))
    run = True

    while run:
        pygame.display.update()
        MAIN_SCREEN.blit(BG, (0, 0))
        level_screen.draw(MAIN_SCREEN)
        back_button.draw(MAIN_SCREEN, 100, 800)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_active():
                    run = False
                elif level_screen.is_active():
                    game_controller.start_level(level_screen.get_active())

        clock.tick(FPS)


def main_menu():
    title_font = pygame.font.SysFont("Algerian", 250)
    title = title_font.render('ARKANOID', False, colors.WHITE)

    run = True

    play_button = Button(550, 150, colors.DARK_BLUE, colors.AQUA, "PLAY", colors.WHITE)
    leaderboard_button = Button(550, 150, colors.DARK_BLUE, colors.AQUA, "LEADERBOARD", colors.WHITE)
    about_button = Button(150, 150, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load(
        "images/about_button.png"))
    quit_button = Button(150, 150, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load(
        "images/quit_button.png"))

    while run:
        MAIN_SCREEN.blit(BG, (0, 0))
        MAIN_SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_size()[0] // 2, 150))

        play_button.draw(MAIN_SCREEN, 350, 550)
        leaderboard_button.draw(MAIN_SCREEN, 350, 800)
        about_button.draw(MAIN_SCREEN, 50, 800)
        quit_button.draw(MAIN_SCREEN, 1050, 800)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_active():
                    select_level()
                if leaderboard_button.is_active():
                    pass
                if about_button.is_active():
                    pass
                if quit_button.is_active():
                    quit_game()
        clock.tick(FPS)
    pygame.quit()


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()
