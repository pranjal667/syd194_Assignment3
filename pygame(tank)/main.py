import pygame
import sys
import random
from game_assets import *
from player import Player
from enemy import Enemy

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text(screen, "Tank Battle Game", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Press ENTER to Play", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, "Press ESC to Exit", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over(score):
    while True:
        screen.fill(BLACK)
        draw_text(screen, f"Game Over! Total Score: {score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Press R to Retry", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, "Press ESC to Exit", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global PLAYER_SPEED, PROJECTILE_SPEED, ENEMY_SPEED
    PLAYER_SPEED = BASE_PLAYER_SPEED
    PROJECTILE_SPEED = BASE_PROJECTILE_SPEED
    ENEMY_SPEED = BASE_ENEMY_SPEED

    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()

    player = Player(PLAYER_SPEED)
    all_sprites.add(player)

    score = 0
    enemy_spawn_timer = 0
    level = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    projectile = player.shoot()
                    all_sprites.add(projectile)
                    projectiles.add(projectile)

        all_sprites.update()

        if score // 50 > level - 1:
            level += 1
            PLAYER_SPEED += 1
            PROJECTILE_SPEED += 1
            ENEMY_SPEED += 1
            player.speed = PLAYER_SPEED

        enemy_spawn_timer += 1
        if enemy_spawn_timer > 60:
            enemy_spawn_timer = 0
            enemy = Enemy(SCREEN_WIDTH, random.randint(100, SCREEN_HEIGHT - 50), ENEMY_SPEED)
            all_sprites.add(enemy)
            enemies.add(enemy)

        for enemy in enemies:
            enemy_projectile = enemy.update()
            if enemy_projectile:
                all_sprites.add(enemy_projectile)
                enemy_projectiles.add(enemy_projectile)

        for projectile in projectiles:
            hits = pygame.sprite.spritecollide(projectile, enemies, False)
            for hit in hits:
                hit.health -= 10
                if hit.health <= 0:
                    explosion_sound.play()
                    hit.kill()
                    score += 10
                projectile.kill()

        for projectile in enemy_projectiles:
            if pygame.sprite.collide_rect(projectile, player):
                hit_sound.play()
                player.health -= 10
                if player.health <= 0:
                    explosion_sound.play()
                    player.lives -= 1
                    player.health = 100
                    if player.lives <= 0:
                        running = False
                projectile.kill()

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                explosion_sound.play()
                enemy.kill()
                player.lives -= 1
                player.health = 100
                if player.lives <= 0:
                    running = False
                else:
                    player.rect.center = (100, SCREEN_HEIGHT // 2)
                    enemy_spawn_timer = 0
                    for e in enemies:
                        e.kill()

        screen.blit(terrain_image, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH // 2, 10)
        draw_text(screen, f"Lives: {player.lives}", 24, 60, 10)
        draw_text(screen, f"Health: {player.health}", 24, 60, 40)
        pygame.display.flip()

        if not running:
            game_over(score)
            return main()

        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    pygame.init()
    main_menu()
    main()
