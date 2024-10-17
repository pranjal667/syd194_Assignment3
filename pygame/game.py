import random
import sys
import pygame
from pygame.locals import *
from assets import SPRITES, SOUNDS

# Constants
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_HEIGHT = SCREEN_HEIGHT * 0.8
FPSCLOCK = pygame.time.Clock()

def main_game():
    """The main game function where gameplay happens."""
    score = 0
    player_x = int(SCREEN_WIDTH / 5)
    player_y = int(SCREEN_HEIGHT / 2)
    base_x = 0

    pipe1 = generate_random_pipe()
    pipe2 = generate_random_pipe()

    upper_pipes = [
        {'x': SCREEN_WIDTH + 200, 'y': pipe1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': pipe2[0]['y']}
    ]
    lower_pipes = [
        {'x': SCREEN_WIDTH + 200, 'y': pipe1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': pipe2[1]['y']}
    ]

    pipe_velocity_x = -4
    player_velocity_y = -9
    max_velocity_y = 10
    player_acc_y = 1
    player_flap_acc = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_velocity_y = player_flap_acc
                    player_flapped = True
                    SOUNDS['wing'].play()

        if detect_collision(player_x, player_y, upper_pipes, lower_pipes):
            return

        player_mid_pos = player_x + SPRITES['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + SPRITES['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score}")
                SOUNDS['point'].play()

        if player_velocity_y < max_velocity_y and not player_flapped:
            player_velocity_y += player_acc_y

        if player_flapped:
            player_flapped = False

        player_height = SPRITES['player'].get_height()
        player_y = player_y + min(player_velocity_y, GROUND_HEIGHT - player_y - player_height)

        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_velocity_x
            lower_pipe['x'] += pipe_velocity_x

        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = generate_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        if upper_pipes[0]['x'] < -SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        SCREEN.blit(SPRITES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(SPRITES['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            SCREEN.blit(SPRITES['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
        
        SCREEN.blit(SPRITES['base'], (base_x, GROUND_HEIGHT))
        SCREEN.blit(SPRITES['player'], (player_x, player_y))

        digits = [int(x) for x in str(score)]
        width = sum(SPRITES['numbers'][digit].get_width() for digit in digits)
        x_offset = (SCREEN_WIDTH - width) / 2
        for digit in digits:
            SCREEN.blit(SPRITES['numbers'][digit], (x_offset, SCREEN_HEIGHT * 0.12))
            x_offset += SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generate_random_pipe():
    """Generate positions of two pipes (one upper and one lower)."""
    pipe_height = SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREEN_WIDTH + 10
    y1 = pipe_height - y2 + offset
    return [
        {'x': pipe_x, 'y': -y1},  # Upper pipe
        {'x': pipe_x, 'y': y2}    # Lower pipe
    ]

def detect_collision(player_x, player_y, upper_pipes, lower_pipes):
    """Check if the player has collided with pipes or the ground."""
    if player_y > GROUND_HEIGHT - 25 or player_y < 0:
        SOUNDS['hit'].play()
        return True

    for upper_pipe in upper_pipes:
        pipe_height = SPRITES['pipe'][0].get_height()
        if player_y < pipe_height + upper_pipe['y'] and abs(player_x - upper_pipe['x']) < SPRITES['pipe'][0].get_width() - 20:
            SOUNDS['hit'].play()
            return True

    for lower_pipe in lower_pipes:
        if player_y + SPRITES['player'].get_height() > lower_pipe['y'] and abs(player_x - lower_pipe['x']) < SPRITES['pipe'][0].get_width() - 20:
            SOUNDS['hit'].play()
            return True

    return False
