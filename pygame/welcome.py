import sys
import pygame
from pygame.locals import *
from assets import SPRITES
from game import main_game

#Constants 
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_HEIGHT = SCREEN_HEIGHT * 0.8

def welcome_screen():
    """To show the welcome screen to the player before the game starts."""
    player_x = int(SCREEN_WIDTH / 5)
    player_y = int(SCREEN_HEIGHT - SPRITES['player'].get_height()) / 2
    message_x = int(SCREEN_WIDTH - SPRITES['message'].get_width()) / 2
    message_y = int(SCREEN_HEIGHT - SPRITES['message'].get_height()) / 2
    base_x = 0

    play_button = pygame.Rect(108, 222, 68, 65)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if play_button.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if play_button.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    main_game()

        SCREEN.blit(SPRITES['background'], (0, 0))
        SCREEN.blit(SPRITES['player'], (player_x, player_y))
        SCREEN.blit(SPRITES['message'], (message_x, message_y))
        SCREEN.blit(SPRITES['base'], (base_x, GROUND_HEIGHT))

        pygame.display.update()
        