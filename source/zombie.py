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
player_width, player_height = 80, 120
for direction in player_textures:
    player_textures[direction] = [pygame.transform.scale(img, (player_width, player_height)) for img in player_textures[direction]]

# Načtení textur nepřátel
enemy_width, enemy_height = 80, 120
enemy_texture_dead = pygame.image.load("zombiedead.png")
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

# Načtení textur minibosse
miniboss_textures = {
    "right": [pygame.image.load(f"zombievpravo{i}.png") for i in range(1, 4)],
    "left": [pygame.image.load(f"zombievlevo{i}.png") for i in range(1, 4)],
    "up": [pygame.image.load(f"zombievzad{i}.png") for i in range(1, 4)],
    "down": [pygame.image.load(f"zombie{i}.png") for i in range(1, 4)]
}

# Načtení textur překážek
obstacle_texture = pygame.image.load("Bedna.png")
obstacle_size = (100, 100)
obstacle_texture = pygame.transform.scale(obstacle_texture, obstacle_size)

# Seznam překážek
obstacles = [
    pygame.Rect(400, 300, *obstacle_size),
    pygame.Rect(800, 600, *obstacle_size),
    pygame.Rect(1200, 400, *obstacle_size)
]

# Parametry minibosse
miniboss_width, miniboss_height = 200, 250
miniboss_speed = 2
miniboss_health = 20

# Změna velikosti textur minibosse
for direction in miniboss_textures:
    miniboss_textures[direction] = [pygame.transform.scale(img, (miniboss_width, miniboss_height)) for img in miniboss_textures[direction]]

# Parametry postavy
player = player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 8
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
    safe_distance = 150  # Větší minimální vzdálenost od hráče
    for _ in range(count):
        if spawned_zombies < zombies_per_wave:
            while True:
                enemy_x = random.randint(0, WIDTH - enemy_width)
                enemy_y = random.randint(0, HEIGHT - enemy_height)
                # Kontrola, zda je zombík dostatečně daleko od hráče
                if abs(enemy_x - player_x) > safe_distance and abs(enemy_y - player_y) > safe_distance:
                    # Kontrola, zda místo není obsazeno překážkou
                    zombie_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
                    collision_with_obstacle = False
                    for obstacle in obstacles:
                        if zombie_rect.colliderect(obstacle):
                            collision_with_obstacle = True
                            break
                    if not collision_with_obstacle:
                        enemies.append({"x": enemy_x, "y": enemy_y, "alive": True, "frame": 0, "direction": "right"})
                        spawned_zombies += 1
                        break
                

# Parametry střelby
bullets = []
bullet_speed = 7
bullet_width, bullet_height = 10, 20

# Funkce pro kontrolu kolize hráče s překážkami
def check_collision(x, y, dx, dy):
    new_rect = pygame.Rect(x + dx, y + dy, player_width, player_height)
    for obstacle in obstacles:
        if new_rect.colliderect(obstacle):
            return False  # Kolize, pohyb není možný
    return True

# Funkce pro kontrolu kolize zombie s	 překážkami
def check_collision_enemy(x, y, dx, dy):
    new_rect = pygame.Rect(x + dx, y + dy, enemy_width, enemy_height)
    for obstacle in obstacles:
        if new_rect.colliderect(obstacle):
            return False  # Kolize, pohyb není možný
    return True

# Funkce pro kontrolu kolize minibosse s překážkami
def check_collision_miniboss(x, y, dx, dy):
    new_rect = pygame.Rect(x + dx, y + dy, miniboss_width, miniboss_height)
    for obstacle in obstacles:
        if new_rect.colliderect(obstacle):
            return False  # Kolize, pohyb není možný
    return True


# Funkce pro spawn minibosse
def spawn_miniboss():
    miniboss_x = random.randint(0, WIDTH - miniboss_width)
    miniboss_y = random.randint(0, HEIGHT - miniboss_height)
    miniboss_rect = pygame.Rect(miniboss_x, miniboss_y, miniboss_width, miniboss_height)
      # Zkontrolujeme, zda miniboss není spawnován v překážkách
    collision_with_obstacle = False
    for obstacle in obstacles:
        if miniboss_rect.colliderect(obstacle):
            collision_with_obstacle = True
            break
             # Zkontrolujeme, zda miniboss není spawnován příliš blízko hráče
    collision_with_player = False
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if miniboss_rect.colliderect(player_rect):
        collision_with_player = True
        
    if not collision_with_obstacle and not collision_with_player:
        miniboss = {
            "x": miniboss_x,
            "y": miniboss_y,
            "alive": True,
            "health": miniboss_health,
            "frame": 0,
            "direction": "right"
        }
        return miniboss

# Hlavní smyčka
running = True
game_over = False
frame_counter = 0
miniboss = None
miniboss_spawned = False
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
        # Spawn zombie pokud miniboss ještě není spawnut
        if not miniboss_spawned:
            if spawned_zombies < zombies_per_wave:
                if frame_counter - spawn_timer >= spawn_interval:
                    spawn_enemies(zombies_per_spawn)
                    spawn_timer = frame_counter
            else:
                # Pokud jsou všechny zombie mrtvé, spawnni miniboss
                if all(not enemy["alive"] for enemy in enemies):
                    
                    miniboss = spawn_miniboss()
                    miniboss_spawned = True
                    enemies.clear()
                    spawned_zombies = 0
        else:
            # Zpracování minibosse, pokud existuje
            if miniboss and miniboss["alive"]:
                if miniboss["x"] < player_x and check_collision_miniboss(miniboss["x"], miniboss["y"], miniboss_speed, 0):
                    miniboss["x"] += miniboss_speed
                    miniboss["direction"] = "right"
                elif miniboss["x"] > player_x and check_collision_miniboss(miniboss["x"], miniboss["y"], -miniboss_speed, 0):
                    miniboss["x"] -= miniboss_speed
                    miniboss["direction"] = "left"
                if miniboss["y"] < player_y and check_collision_miniboss(miniboss["x"], miniboss["y"], 0, miniboss_speed):
                    miniboss["y"] += miniboss_speed
                    miniboss["direction"] = "down"
                elif miniboss["y"] > player_y and check_collision_miniboss(miniboss["x"], miniboss["y"], 0, -miniboss_speed):
                    miniboss["y"] -= miniboss_speed
                    miniboss["direction"] = "up"
                miniboss["frame"] = (frame_counter // 10) % 3

                if (miniboss["x"] < player_x + player_width and
                    miniboss["x"] + miniboss_width > player_x and
                    miniboss["y"] < player_y + player_height and
                    miniboss["y"] + miniboss_height > player_y):
                    game_over = True
            else:
                miniboss = None
                miniboss_spawned = False
                wave += 1
                zombies_per_wave += 15

        # Pohyb hráče, zombie, střel atd.
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
        if keys[pygame.K_w] and check_collision(player_x, player_y, 0, -player_speed):
            player_y -= player_speed
            player_direction = "up"
            moving = True
        if keys[pygame.K_s] and check_collision(player_x, player_y, 0, player_speed):
            player_y += player_speed
            player_direction = "down"
            moving = True
        if keys[pygame.K_a] and check_collision(player_x, player_y, -player_speed, 0):
            player_x -= player_speed
            player_direction = "left"
            moving = True
        if keys[pygame.K_d] and check_collision(player_x, player_y, player_speed, 0):
            player_x += player_speed
            player_direction = "right"
            moving = True

        if moving:
            player_frame = (frame_counter // 10) % 3
        else:
            player_frame = 0

        player_x = max(0, min(WIDTH - player_width, player_x))
        player_y = max(0, min(HEIGHT - player_height, player_y))

        for enemy in enemies:
            if enemy["alive"]:
                if enemy["x"] < player_x and check_collision_enemy(enemy["x"], enemy["y"], enemy_speed, 0):
                    enemy["x"] += enemy_speed
                    enemy["direction"] = "right"
                elif enemy["x"] > player_x and check_collision_enemy(enemy["x"], enemy["y"], -enemy_speed, 0):
                    enemy["x"] -= enemy_speed
                    enemy["direction"] = "left"
                if enemy["y"] < player_y and check_collision_enemy(enemy["x"], enemy["y"], 0, enemy_speed):
                    enemy["y"] += enemy_speed
                    enemy["direction"] = "down"
                elif enemy["y"] > player_y and check_collision_enemy(enemy["x"], enemy["y"], 0, -enemy_speed):
                    enemy["y"] -= enemy_speed
                    enemy["direction"] = "up"
                enemy["frame"] = (frame_counter // 10) % 3

                if (enemy["x"] < player_x + player_width and
                    enemy["x"] + enemy_width > player_x and
                    enemy["y"] < player_y + player_height and
                    enemy["y"] + enemy_height > player_y):
                    game_over = True
            

        for bullet in bullets[:]:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]

            hit = False
            for enemy in enemies:
                if enemy["alive"]:
                    if (enemy["x"] < bullet["x"] < enemy["x"] + enemy_width and
                        enemy["y"] < bullet["y"] < enemy["y"] + enemy_height):
                        enemy["alive"] = False
                        hit = True
                        break
            if miniboss and miniboss["alive"]:
                if (miniboss["x"] < bullet["x"] < miniboss["x"] + miniboss_width and
                    miniboss["y"] < bullet["y"] < miniboss["y"] + miniboss_height):
                    miniboss["health"] -= 1
                    hit = True
                    if miniboss["health"] <= 0:
                        miniboss["alive"] = False
            if hit and bullet in bullets:
                bullets.remove(bullet)

        bullets = [bullet for bullet in bullets if 0 < bullet["x"] < WIDTH and 0 < bullet["y"] < HEIGHT]

        screen.fill(BLACK)
        screen.blit(player_textures[player_direction][player_frame], (player_x, player_y))
        # Vykreslení překážek
        for obstacle in obstacles:
            screen.blit(obstacle_texture, (obstacle.x, obstacle.y))

        for enemy in enemies:
            if enemy["alive"]:
                if enemy["direction"] == "right":
                    texture = enemy_textures["right"][enemy["frame"]]
                elif enemy["direction"] == "left":
                    texture = enemy_textures["left"][enemy["frame"]]
                elif enemy["direction"] == "up":
                    texture = enemy_textures["up"][enemy["frame"]]
                else:
                    texture = enemy_textures["down"][enemy["frame"]]
                screen.blit(texture, (enemy["x"], enemy["y"]))
            else:
                screen.blit(enemy_texture_dead, (enemy["x"], enemy["y"]))

        if miniboss and miniboss["alive"]:
            miniboss_texture = miniboss_textures[miniboss["direction"]][miniboss["frame"]]
            screen.blit(miniboss_texture, (miniboss["x"], miniboss["y"]))

        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], bullet_width, bullet_height))
            
        text = font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(text, (50, 50))
    else:
        font_big = pygame.font.Font(None, 74)
        text = font_big.render("Prohrál jsi", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        
        
    pygame.display.update()
    
pygame.quit()	


