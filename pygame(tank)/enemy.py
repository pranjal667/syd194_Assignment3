import pygame
import random
from game_assets import *
from player import Projectile  # Importing player Projectile class

class Enemy(pygame.sprite.Sprite):
    def init(self, x, y, speed):
        super().init()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.health = 50

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

        # Random chance for the enemy to shoot
        if random.random() < ENEMY_SHOOT_PROBABILITY:
            return EnemyProjectile(self.rect.left, self.rect.centery)
        return None

class EnemyProjectile(pygame.sprite.Sprite):
    def init(self, x, y):
        super().init()
        self.image = enemy_bullet_image  # Use the enemy bullet image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -BASE_PROJECTILE_SPEED  # Move left

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()