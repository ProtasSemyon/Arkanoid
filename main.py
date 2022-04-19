import pygame
import os
import colors
from button import Button

pygame.font.init()
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1250, 1000
FPS = 60
clock = pygame.time.Clock()

MAIN_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")

BG = pygame.transform.scale(pygame.image.load(os.path.join("images", "background.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))


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
