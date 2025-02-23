import pygame 
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (232, 215, 10)
BLUE = (10, 111, 232)

# Font
font = pygame.font.Font(None, 74)

# Funkce pro vykreslení tlačítek
def draw_button(text, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

# Hlavní menu
def main_menu():
    while True:
        screen.fill(BLACK)
        draw_button("Hr\u00e1t", GREEN, WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 80) 
        draw_button("Ukon\u010dit", RED, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100:
                    if HEIGHT // 2 - 100 <= y <= HEIGHT // 2 - 20:
                        return  # Spustí hru
                    if HEIGHT // 2 + 50 <= y <= HEIGHT // 2 + 130:
                        pygame.quit()
                        exit()

# Spustí hlavní menu
main_menu()

# Načtení textur hráče (animace pro všechny směry)
player_textures = {
    "right": [pygame.image.load(f"hracvpravo{i}.png") for i in range(1, 4)],
    "left": [pygame.image.load(f"hracvlevo{i}.png") for i in range(1, 4)],
    "up": [pygame.image.load(f"hracvzad{i}.png") for i in range(1, 4)],
    "down": [pygame.image.load(f"hrac{i}.png") for i in range(1, 4)]
}

# Změna velikosti textur hráče
player_width, player_height = 100, 150
for direction in player_textures:
    player_textures[direction] = [pygame.transform.scale(img, (player_width, player_height)) for img in player_textures[direction]]

# Načtení textur nepřátel
enemy_width, enemy_height = 100, 150

enemy_texture_dead = pygame.image.load("enemy2.png")
enemy_texture_dead = pygame.transform.scale(enemy_texture_dead, (enemy_width, enemy_height))

enemy_textures = {
    "right": [pygame.image.load(f"zombievpravo{i}.png") for i in range(1, 4)],
    "left": [pygame.image.load(f"zombievlevo{i}.png") for i in range(1, 4)],
    "up": [pygame.image.load(f"zombievzad{i}.png") for i in range(1, 4)],
    "down": [pygame.image.load(f"zombie{i}.png") for i in range(1, 4)]
}

# Změna velikosti textur nepřátel
for direction in enemy_textures:
    enemy_textures[direction] = [pygame.transform.scale(img, (enemy_width, enemy_height)) for img in enemy_textures[direction]]

# Parametry postavy
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 10
player_direction = "down"
player_frame = 0

# Parametry nepřátel
enemy_speed = 3
enemies = []
wave = 1
spawned_zombies = 0
zombies_per_wave = 15
zombies_per_spawn = 3
spawn_timer = 2
spawn_interval = 60 # Počet snímků mezi spawnem další skupiny
def spawn_enemies(count):
    global spawned_zombies
    safe_distance = 100  # Minimální vzdálenost od hráče
    for _ in range(count):
        if spawned_zombies < zombies_per_wave:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy_y = random.randint(0, HEIGHT - enemy_height)
            enemies.append({"x": enemy_x, "y": enemy_y, "alive": True, "frame": 0, "direction": "right"})
            spawned_zombies += 1
                # Kontrola vzdálenosti od hráče
        if abs(enemy_x - player_x) > safe_distance and abs(enemy_y - player_y) > safe_distance:
                    break  # Pokud je dostatečně daleko, ukončíme cyklus

# Parametry střelby
bullets = []
bullet_speed = 7
bullet_width, bullet_height = 10, 20

# Hlavní smyčka
running = True
game_over = False
frame_counter = 0
while running:
    pygame.time.delay(30)  # Zpomalení smyčky
    frame_counter += 1
    moving = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_dx = 0
                bullet_dy = 0
                if player_direction == "up":
                    bullet_dy = -bullet_speed
                elif player_direction == "down":
                    bullet_dy = bullet_speed
                elif player_direction == "left":
                    bullet_dx = -bullet_speed
                elif player_direction == "right":
                    bullet_dx = bullet_speed
                bullets.append({"x": player_x + player_width // 2 - bullet_width // 2, "y": player_y + player_height // 2 - bullet_height // 2, "dx": bullet_dx, "dy": bullet_dy})
    
    if not game_over:
         # Spawnování nepřátel ve vlnách
        if spawned_zombies < zombies_per_wave:
            if frame_counter - spawn_timer >= spawn_interval:
                spawn_enemies(zombies_per_spawn)
                spawn_timer = frame_counter
        else:
            # Pokud jsou všichni zombíci mrtví, posun na další vlnu
            if all(not enemy["alive"] for enemy in enemies):
                wave += 1
                spawned_zombies = 0
                zombies_per_wave += 15
                enemies.clear()
        
        # Pohyb postavy
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_direction = "up"
            moving = True
        if keys[pygame.K_DOWN]:
            player_direction = "down"
            moving = True
        if keys[pygame.K_LEFT]:
            player_direction = "left"
            moving = True
        if keys[pygame.K_RIGHT]:
            player_direction = "right"
            moving = True
        if keys[pygame.K_w]:
            player_y -= player_speed
            player_direction = "up"
            moving = True
        if keys[pygame.K_s]:
            player_y += player_speed
            player_direction = "down"
            moving = True
        if keys[pygame.K_a]:
            player_x -= player_speed
            player_direction = "left"
            moving = True
        if keys[pygame.K_d]:
            player_x += player_speed
            player_direction = "right"
            moving = True
        
        # Animace hráče
        if moving:
            player_frame = (frame_counter // 10) % 3
        else:
            player_frame = 0
        
        
        # Omezení pohybu na obrazovku
        player_x = max(0, min(WIDTH - player_width, player_x))
        player_y = max(0, min(HEIGHT - player_height, player_y))
        
        # Pohyb nepřátel směrem k hráči
        for enemy in enemies:
            if enemy["alive"]:
                if enemy["x"] < player_x:
                    enemy["x"] += enemy_speed
                    enemy["direction"] = "right"
                elif enemy["x"] > player_x:
                    enemy["x"] -= enemy_speed
                    enemy["direction"] = "left"
                if 	enemy["y"] < player_y:
                    enemy["y"] += enemy_speed
                    enemy["direction"] = "down"
                elif enemy["y"] > player_y:
                    enemy["y"] -= enemy_speed
                    enemy["direction"] = "up"
                
                # Animace chůze nepřátel
                enemy["frame"] = (frame_counter // 10) % 3
                
                # Kolize s hráčem
                if abs(enemy["x"] - player_x) < enemy_width and abs(enemy["y"] - player_y) < enemy_height:
                    game_over = True
        
        # Pohyb střel
        for bullet in bullets:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]
            
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
        bullets = [bullet for bullet in bullets if 0 < bullet["x"] < WIDTH and 0 < bullet["y"] < HEIGHT]
        
        # Vykreslení
        screen.fill(BLACK)
        screen.blit(player_textures[player_direction][player_frame], (player_x, player_y))
        for enemy in enemies:
            if enemy["alive"]:
                # kód pro vykreslení živého nepřítele
                # např. výběr textury podle směru
                if enemy["direction"] == "right":
                    texture = enemy_textures["right"][enemy["frame"]]
                elif enemy["direction"] == "left":
                        texture = enemy_textures["left"][enemy["frame"]]
                elif enemy["direction"] == "up":
                    texture = enemy_textures["up"][enemy["frame"]]
                else:  # "down"
                    texture = enemy_textures["down"][enemy["frame"]]
                screen.blit(texture, (enemy["x"], enemy["y"]))
            else:
                screen.blit(enemy_texture_dead, (enemy["x"], enemy["y"]))
        
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], bullet_width, bullet_height))
        
        text = font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(text, (50, 50))
    else:
        font = pygame.font.Font(None, 74)
        text = font.render("Prohrál jsi", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        
        
    pygame.display.update()
    
pygame.quit()

