import pygame
import random
import math

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1600, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Barvy
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Parametry postavy
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Parametry nepřátel
enemy_size = 50
enemy_speed = 3
enemies = []
for _ in range(5):
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = random.randint(0, HEIGHT - enemy_size)
    enemies.append([enemy_x, enemy_y])

# Hlavní smyčka
running = True
game_over = False
while running:
    pygame.time.delay(30)  # Zpomalení smyčky
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        # Pohyb postavy
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
        
        # Omezení pohybu na obrazovku
        player_x = max(0, min(WIDTH - player_size, player_x))
        player_y = max(0, min(HEIGHT - player_size, player_y))
        
        # Pohyb nepřátel směrem k hráči
        for enemy in enemies:
            if enemy[0] < player_x:
                enemy[0] += enemy_speed
            elif enemy[0] > player_x:
                enemy[0] -= enemy_speed
            if enemy[1] < player_y:
                enemy[1] += enemy_speed
            elif enemy[1] > player_y:
                enemy[1] -= enemy_speed
            
            # Kolize s hráčem
            if abs(enemy[0] - player_x) < player_size and abs(enemy[1] - player_y) < player_size:
                game_over = True
        
        # Vykreslení
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Prohrál jsi", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    
    pygame.display.update()
    
pygame.quit()
