import enum
import sys

import pygame
import os
import colors

from entities.button import Button
from entities.level_controller import Level
from entities.level_screen import LevelScreen

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


def start_level(level_file):
    level = Level((SCREEN_WIDTH, SCREEN_HEIGHT), BG, level_file)

    run = True

    while run:
        pygame.display.update()
        level.draw(MAIN_SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level.is_pause_active():
                    state = pause_level()
                    if state == LevelState.RETRY:
                        level = Level((SCREEN_WIDTH, SCREEN_HEIGHT), BG, level_file)
                    elif state == LevelState.EXIT:
                        run = False


def select_level():
    level_screen = LevelScreen("configs/level_state.json")

    back_button = Button(150, 150, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load("images/BACK_BUTTON.png"))
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
                    start_level(level_screen.get_active())


def main_menu():
    title_font = pygame.font.SysFont("Algerian", 250)
    title = title_font.render('ARKANOID', False, colors.WHITE)

    run = True

    play_button = Button(550, 150, colors.DARK_BLUE, colors.AQUA, "PLAY", colors.WHITE)
    leaderboard_button = Button(550, 150, colors.DARK_BLUE, colors.AQUA, "LEADERBOARD", colors.WHITE)
    about_button = Button(150, 150, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load("images/ABOUT_BUTTON.png"))
    quit_button = Button(150, 150, colors.DARK_BLUE, colors.AQUA, "", colors.WHITE, pygame.image.load("images/QUIT_BUTTON.png"))

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
