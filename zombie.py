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

# Parametry postavy
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 8

# Hlavní smyčka
running = True
while running:
    pygame.time.delay(30)  # Zpomalení smyčky
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
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
    
    # Vykreslení
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
    pygame.display.update()
    
pygame.quit()
