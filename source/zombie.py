import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zelená postavička")

# Barvy
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Načtení textur
player_texture = pygame.image.load("player1.png")
enemy_texture_alive = pygame.image.load("enemy1.png")
enemy_texture_dead = pygame.image.load("enemy2.png")

# Změna velikosti textur
player_texture = pygame.transform.scale(player_texture, (50, 50))
enemy_texture_alive = pygame.transform.scale(enemy_texture_alive, (50, 50))
enemy_texture_dead = pygame.transform.scale(enemy_texture_dead, (50, 50))

# Parametry postavy
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Parametry nepřátel
enemy_size= 50
enemy_speed = 3
enemies = []
for _ in range(5):
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = random.randint(0, HEIGHT - enemy_size)
    enemies.append({"x": enemy_x, "y": enemy_y, "alive": True})

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
            if enemy["alive"]:
                if enemy["x"] < player_x:
                    enemy["x"] += enemy_speed
                elif enemy["x"] > player_x:
                    enemy["x"] -= enemy_speed
                if enemy["y"] < player_y:
                    enemy["y"] += enemy_speed
                elif enemy["y"] > player_y:
                    enemy["y"] -= enemy_speed
                
                # Kolize s hráčem
                if abs(enemy["x"] - player_x) < player_size and abs(enemy["y"] - player_y) < player_size:
                    game_over = True
        
        # Vykreslení
        screen.fill(WHITE)
        screen.blit(player_texture, (player_x, player_y))
        for enemy in enemies:
            if enemy["alive"]:
                screen.blit(enemy_texture_alive, (enemy["x"], enemy["y"]))
            else:
                screen.blit(enemy_texture_dead, (enemy["x"], enemy["y"]))
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Prohrál jsi", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    
    pygame.display.update()
    
pygame.quit()
