import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Barvy
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Načtení textur
player_texture = pygame.image.load("player1.png")
enemy_texture_alive_right_1 = pygame.image.load("1vpravo.png")
enemy_texture_alive_right_2 = pygame.image.load("2vpravo.png")
enemy_texture_alive_left_1 = pygame.image.load("1vlevo.png")
enemy_texture_alive_left_2 = pygame.image.load("2vlevo.png")
enemy_texture_dead = pygame.image.load("enemy2.png")

# Parametry postavy
player_width = 50
player_height = 70
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Parametry nepřátel
enemy_width = 100
enemy_height = 150
enemy_speed = 3
enemies = []
for _ in range(5):
    enemy_x = random.randint(0, WIDTH - enemy_width)
    enemy_y = random.randint(0, HEIGHT - enemy_height)
    enemies.append({"x": enemy_x, "y": enemy_y, "alive": True, "frame": 0, "direction": "right"})

# Parametry střelby
bullets = []
bullet_speed = 7
bullet_width = 10
bullet_height = 20

# Změna velikosti textur
player_texture = pygame.transform.scale(player_texture, (player_width, player_height))
enemy_texture_alive_right_1 = pygame.transform.scale(enemy_texture_alive_right_1, (enemy_width, enemy_height))
enemy_texture_alive_right_2 = pygame.transform.scale(enemy_texture_alive_right_2, (enemy_width, enemy_height))
enemy_texture_alive_left_1 = pygame.transform.scale(enemy_texture_alive_left_1, (enemy_width, enemy_height))
enemy_texture_alive_left_2 = pygame.transform.scale(enemy_texture_alive_left_2, (enemy_width, enemy_height))
enemy_texture_dead = pygame.transform.scale(enemy_texture_dead, (enemy_width, enemy_height))

# Hlavní smyčka
running = True
game_over = False
frame_counter = 0
while running:
    pygame.time.delay(30)  # Zpomalení smyčky
    frame_counter += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append({"x": player_x + player_width // 2 - bullet_width // 2, "y": player_y})
    
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
        player_x = max(0, min(WIDTH - player_width, player_x))
        player_y = max(0, min(HEIGHT - player_height, player_y))
        
        # Pohyb nepřátel směrem k hráči
        for enemy in enemies:
            if enemy["alive"]:
                previous_x = enemy["x"]
                if enemy["x"] < player_x:
                    enemy["x"] += enemy_speed
                    enemy["direction"] = "right"
                elif enemy["x"] > player_x:
                    enemy["x"] -= enemy_speed
                    enemy["direction"] = "left"
                if enemy["y"] < player_y:
                    enemy["y"] += enemy_speed
                elif enemy["y"] > player_y:
                    enemy["y"] -= enemy_speed
                
                # Animace chůze nepřátel
                enemy["frame"] = (frame_counter // 10) % 2
                
                # Kolize s hráčem
                if abs(enemy["x"] - player_x) < enemy_width and abs(enemy["y"] - player_y) < enemy_height:
                    game_over = True
        
        # Pohyb střel
        for bullet in bullets:
            bullet["y"] -= bullet_speed
        
        # Kontrola kolize střel s nepřáteli
        for enemy in enemies:
            if enemy["alive"]:
                for bullet in bullets:
                    if (enemy["x"] < bullet["x"] < enemy["x"] + enemy_width and
                        enemy["y"] < bullet["y"] < enemy["y"] + enemy_height):
                        enemy["alive"] = False
                        bullets.remove(bullet)
                        break
        
        # Odstranění střel mimo obrazovku
        bullets = [bullet for bullet in bullets if bullet["y"] > 0]
        
        # Vykreslení
        screen.fill(BLACK)
        screen.blit(player_texture, (player_x, player_y))
        for enemy in enemies:
            if enemy["alive"]:
                if enemy["direction"] == "right":
                    texture = enemy_texture_alive_right_1 if enemy["frame"] == 0 else enemy_texture_alive_right_2
                else:
                    texture = enemy_texture_alive_left_1 if enemy["frame"] == 0 else enemy_texture_alive_left_2
                screen.blit(texture, (enemy["x"], enemy["y"]))
            else:
                screen.blit(enemy_texture_dead, (enemy["x"], enemy["y"]))
        
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], bullet_width, bullet_height))
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Prohrál jsi", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    
    pygame.display.update()
    
pygame.quit()
