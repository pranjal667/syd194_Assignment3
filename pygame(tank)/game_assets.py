import pygame

Initialize Pygame
pygame.init()

Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tank Game')

Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

Load assets
player_image = pygame.image.load(r'resources/tank_assets/tank.png').convert_alpha()
enemy_image = pygame.image.load(r'resources/tank_assets/enemyTank.png').convert_alpha()
terrain_image = pygame.image.load(r'resources/tank_assets/bg.png').convert_alpha()
terrain_image = pygame.transform.scale(terrain_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the background
shoot_sound = pygame.mixer.Sound(r'resources/tank_assets/gun.wav')
hit_sound = pygame.mixer.Sound(r'resources/tank_assets/explosion.wav')
explosion_sound = pygame.mixer.Sound(r'resources/tank_assets/explosion.wav')
pygame.mixer.music.load(r'resources/tank_assets/music.mp3')
pygame.mixer.music.play(-1)
enemy_bullet_image = pygame.image.load(r'resources/tank_assets/enemyBullet.png').convert_alpha()
bullet_image = pygame.image.load(r'resources/tank_assets/bullet.png').convert_alpha()

Game constants
BASE_PLAYER_SPEED = 5
BASE_PROJECTILE_SPEED = 10
BASE_ENEMY_SPEED = 2
ENEMY_SHOOT_PROBABILITY = 0.01
