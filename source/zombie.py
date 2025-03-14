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

# Načtení textur tlačítek
button_size = (100, 100)  # Čtvercová tlačítka 100x100 px
button_textures = {
    "play": pygame.image.load("Play.png"),
    "shop": pygame.image.load("Market.png"),
    "settings": pygame.image.load("Settings.png"),
    "exit": pygame.image.load("Quit.png")
}

 # Změna velikosti textur na čtverce
for key in button_textures:
    button_textures[key] = pygame.transform.scale(button_textures[key], button_size)

# Načtení obrázků zbraní
weapon_textures = {
    "Shotgun": pygame.image.load("shotgun.png"),
    "Assault Rifle": pygame.image.load("assault rifle.png"),
    "Minigun": pygame.image.load("minigun.png")
}

for key in weapon_textures:
    weapon_textures[key] = pygame.transform.scale(weapon_textures[key], (150, 100))
    
# Funkce pro vykreslení tlačítek
def draw_button(texture, x, y):
    screen.blit(texture, (x, y))
    
# Ceny zbraní
weapons = ["Shotgun", "Assault Rifle", "Minigun"]
prices = {"Shotgun": 500, "Assault Rifle": 1000, "Minigun": 2000}
player_coins = 3500
owned_weapons = []
equipped_weapon = None
    
def draw_shop():
    overlay_width, overlay_height = 700, 500  # Zvětšení overlay okna
    overlay = pygame.Surface((overlay_width, overlay_height))  # Vytvoříme poloprůhledný obdélník
    overlay.set_alpha(200)  # Nastavíme průhlednost (0-255)
    overlay.fill((50, 50, 50))  # Šedá barva
    screen.blit(overlay, (WIDTH // 2 - overlay_width // 2, HEIGHT // 2 - overlay_height // 2))  # Umístění overlaye
        
    # Vykreslení textů a mezer
    text_surface = font.render("SHOP", True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - 50, HEIGHT // 2 - overlay_height // 2 + 20))
        
    # Vykreslení zbraní a cen s většími mezerami
    for i, weapon in enumerate(weapons):
        y_offset = HEIGHT // 2 - overlay_height // 2 + 100 + i * 100
        screen.blit(weapon_textures[weapon], (WIDTH // 2 - 250, y_offset))
        text_surface = font.render(f"{weapon}: {prices[weapon]} coins", True, WHITE)
        screen.blit(text_surface, (WIDTH // 2 - 100, y_offset))
        
        button_text = "Buy" if weapon not in owned_weapons else "Equip"
        button_color = GREEN if weapon not in owned_weapons else BLUE
        pygame.draw.rect(screen, button_color, (WIDTH // 2 + 150, y_offset, 100, 40))
        button_surface = font.render(button_text, True, WHITE)
        screen.blit(button_surface, (WIDTH // 2 + 160, y_offset + 5))

    # Tlačítko pro zavření obchodu
    close_button = pygame.Surface((50, 50))
    close_button.fill(RED)
    screen.blit(close_button, (WIDTH // 2 + overlay_width // 2 - 60, HEIGHT // 2 - overlay_height // 2 + 10))
    pygame.display.update()
   
shop_open = False

# Parametry postavy
player = player_x, player_y = WIDTH // 2, HEIGHT // 2

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

# Textury hráče se zbraněmi
player_weapon_textures = {
    "Shotgun": {
        "right": [pygame.image.load(f"hrac_shotgun_vpravo{i}.png") for i in range(1, 4)],
        "left": [pygame.image.load(f"hrac_shotgun_vlevo{i}.png") for i in range(1, 4)],
        "up": [pygame.image.load(f"hrac_shotgun_vzad{i}.png") for i in range(1, 4)],
        "down": [pygame.image.load(f"hrac_shotgun{i}.png") for i in range(1, 4)]
    },
    "Assault Rifle": {
        "right": [pygame.image.load(f"hrac_rifle_vpravo{i}.png") for i in range(1, 4)],
        "left": [pygame.image.load(f"hrac_rifle_vlevo{i}.png") for i in range(1, 4)],
        "up": [pygame.image.load(f"hrac_rifle_vzad{i}.png") for i in range(1, 4)],
        "down": [pygame.image.load(f"hrac_rifle{i}.png") for i in range(1, 4)]
    },
    "Minigun": {
        "right": [pygame.image.load(f"hrac_minigun_vpravo{i}.png") for i in range(1, 4)],
        "left": [pygame.image.load(f"hrac_minigun_vlevo{i}.png") for i in range(1, 4)],
        "up": [pygame.image.load(f"hrac_minigun_vzad{i}.png") for i in range(1, 4)],
        "down": [pygame.image.load(f"hrac_minigun{i}.png") for i in range(1, 4)]
    }
}

# Změna velikosti textur hráče se zbraněmi
for weapon in player_weapon_textures:
    for direction in player_weapon_textures[weapon]:
        player_weapon_textures[weapon][direction] = [pygame.transform.scale(img, (player_width, player_height)) for img in player_weapon_textures[weapon][direction]]
    
menu_background = pygame.image.load("Backgroundfinal.png")  # Nahraď názvem souboru
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
# Hlavní menu
def main_menu():
    global current_player_textures
    global player_weapon_textures
    global shop_open
    global player_coins
    global equipped_weapon
    while True:
        screen.blit(menu_background, (0, 0))
        coins_text = font.render(f"Coins: {player_coins}", True, YELLOW)
        screen.blit(coins_text, (WIDTH - 300, 50))
         # Výpočet středu obrazovky
        x1 = WIDTH - 850  # První sloupec (víc vlevo)
        x2 = WIDTH - 650  # Druhý sloupec (víc vpravo)
        y1 = HEIGHT // 2 - 0  # První řada (nahoře)
        y2 = HEIGHT // 2 + 140   # Druhá řada (dole)

        # Vykreslení tlačítek
        draw_button(button_textures["play"], x1, y1)
        draw_button(button_textures["shop"], x2, y1)
        draw_button(button_textures["settings"], x1, y2)
        draw_button(button_textures["exit"], x2, y2)
        
        if shop_open:
            draw_shop()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if shop_open:
                    for i, weapon in enumerate(weapons):
                        y_offset = HEIGHT // 2 - 250 + 100 + i * 100
                        if WIDTH // 2 + 150 <= x <= WIDTH // 2 + 250 and y_offset <= y <= y_offset + 40:
                            if weapon not in owned_weapons:
                                if player_coins >= prices[weapon]:
                                    player_coins -= prices[weapon]
                                    owned_weapons.append(weapon)
                                    print(f"Koupeno: {weapon}")
                                else:
                                    print("Nedostatek mincí!")
                            else:
                                equipped_weapon = weapon
                                global current_player_textures
                                if weapon in player_weapon_textures:
                                    current_player_textures = player_weapon_textures[weapon]
                                else:
                                    current_player_textures = player_textures  
                                print(f"Vybaveno: {weapon}")
                else:                
                
                    if x1 <= x <= x1 + 100:
                        if y1 <= y <= y1 + 100:
                            print("Spuštění hry")
                            return
                        elif y2 <= y <= y2 + 100:
                            print("Nastavení")
            # Druhý sloupec (x2)
                    elif x2 <= x <= x2 + 100:
                        if y1 <= y <= y1 + 100:
                            print("Obchod")
                            shop_open = not shop_open
                            if shop_open and WIDTH // 2 + 290 <= x <= WIDTH // 2 + 340 and HEIGHT // 2 - 240 <= y <= HEIGHT // 2 - 190:
                                shop_open = False
                        elif y2 <= y <= y2 + 100:
                            pygame.quit()
                            exit()
                            # Zavření obchodu            
                if shop_open and WIDTH // 2 + 290 <= x <= WIDTH // 2 + 340 and HEIGHT // 2 - 240 <= y <= HEIGHT // 2 - 190:
                    shop_open = False

                        
                        
# Spustí hlavní menu
main_menu()


# Načtení textur mapy
background = pygame.image.load("airport.png")  
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 

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
    "right": [pygame.image.load(f"minibossvpravo{i}.png") for i in range(1, 4)],
    "left": [pygame.image.load(f"minibossvlevo{i}.png") for i in range(1, 4)],
    "up": [pygame.image.load(f"minibossvzad{i}.png") for i in range(1, 4)],
    "down": [pygame.image.load(f"miniboss{i}.png") for i in range(1, 4)]
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
current_player_textures = player_textures 
player_direction = "down"
player_frame = 0

# Přidání systému životů pro hráče
player_max_health = 5
player_health = player_max_health
player_hit_cooldown = 0 
player_invulnerable_time = 60  # 60 snímků = přibližně 2 sekundy při 30 FPS
player_hit_flash = False  # Pro vizuální efekt po zásahu

# Parametry nepřátel
enemy_speed = 3
enemies = []
wave = 1
spawned_zombies = 0
zombies_per_wave = 15
zombies_per_spawn = 3
spawn_timer = 2
spawn_interval = 60 

# Spawnování nepřátel
def spawn_enemies(count):
    global spawned_zombies
    safe_distance = 150  
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
                        # Přidání zdraví pro zombíky (3 hity)
                        enemies.append({
                            "x": enemy_x, 
                            "y": enemy_y, 
                            "alive": True, 
                            "frame": 0, 
                            "direction": "right",
                            "health": 1  # Zombie potřebuje 3 zásahy
                        })
                        spawned_zombies += 1
                        break
                

# Parametry střelby
bullets = []
bullet_speed = 15
bullet_width, bullet_height = 10, 10

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
            "direction": "right",
            "damage": 2  
        }
        return miniboss

# Funkce pro vykreslení health baru
def draw_health_bar():
    bar_width = 300
    bar_height = 30
    border_width = 2
    
    # Pozice health baru (v levém horním rohu, pod textem vlny)
    x, y = 50, 120
    
    # Vykreslení rámečku health baru
    pygame.draw.rect(screen, WHITE, (x - border_width, y - border_width, 
                                    bar_width + 2*border_width, bar_height + 2*border_width))
    
    # Vykreslení pozadí health baru
    pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height))
    
    # Výpočet aktuální šířky health baru
    current_bar_width = int(bar_width * (player_health / player_max_health))
    
    # Barva health baru v závislosti na zbývajícím zdraví
    bar_color = GREEN
    if player_health < player_max_health * 0.7:
        bar_color = YELLOW
    if player_health < player_max_health * 0.3:
        bar_color = RED
    
    # Vykreslení aktuálního zdraví
    pygame.draw.rect(screen, bar_color, (x, y, current_bar_width, bar_height))
    
    # Vykreslení textu se zdravím
    health_text = font.render(f"{int(player_health)}/{player_max_health}", True, WHITE)
    screen.blit(health_text, (x + bar_width + 20, y))

# Hlavní smyčka
if equipped_weapon in player_weapon_textures:
    current_player_textures = player_weapon_textures[equipped_weapon]
    print(f"Nastavuji textury pro {equipped_weapon}")
else:
    current_player_textures = player_textures
    print("Používám výchozí textury")
running = True
game_over = False
frame_counter = 0
miniboss = None
miniboss_spawned = False
while running:
    pygame.time.delay(30)  # Zpomalení smyčky
    frame_counter += 1
    moving = False
    
    # Aktualizace cooldownu po zásahu
    if player_hit_cooldown > 0:
        player_hit_cooldown -= 2
        # Blikání hráče během invulnerability
        player_hit_flash = (frame_counter % 6) < 3
    else:
        player_hit_flash = False
    
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

                # Kolize s minibossem dává poškození místo okamžitého konce hry
                miniboss_rect = pygame.Rect(miniboss["x"], miniboss["y"], miniboss_width, miniboss_height)
                player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
                
                if miniboss_rect.colliderect(player_rect) and player_hit_cooldown == 0:
                    player_health -= miniboss["damage"]
                    player_hit_cooldown = player_invulnerable_time
                    
                    if player_health <= 0:
                        game_over = True
            else:
                miniboss = None
                miniboss_spawned = False
                wave += 1
                

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

                # Kolize se zombíkem dává poškození místo okamžitého konce hry
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
                player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
                
                if enemy_rect.colliderect(player_rect) and player_hit_cooldown == 0:
                    player_health -= 1  # Zombík dává 1 poškození
                    player_hit_cooldown = player_invulnerable_time
                    
                    if player_health <= 0:
                        game_over = True
            

        for bullet in bullets[:]:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]

            hit = False
            for enemy in enemies:
                if enemy["alive"]:
                    if (enemy["x"] < bullet["x"] < enemy["x"] + enemy_width and
                        enemy["y"] < bullet["y"] < enemy["y"] + enemy_height):
                        # Snížení zdraví zombie místo okamžitého zabití
                        enemy["health"] -= 1
                        if enemy["health"] <= 0:
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
        
        screen.blit(background, (0, 0))
        
        # Podmínka pro vykreslení hráče s efektem blikání po zásahu
        if not player_hit_flash:
            screen.blit(current_player_textures[player_direction][player_frame], (player_x, player_y))
        else:
            # Vykreslení hráče s červeným nádechem při zásahu
            player_img = current_player_textures[player_direction][player_frame].copy()
            red_overlay = pygame.Surface(player_img.get_size()).convert_alpha()
            red_overlay.fill((255, 0, 0, 128))  # Červená s průhledností
            player_img.blit(red_overlay, (0, 0))
            screen.blit(player_img, (player_x, player_y))
            
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
                
                # Vykreslení zdraví zombíka
                zombie_health_width = 50
                zombie_health_height = 5
                pygame.draw.rect(screen, RED, (enemy["x"] + enemy_width//2 - zombie_health_width//2, 
                                              enemy["y"] - 10, 
                                              zombie_health_width, zombie_health_height))
                
                current_health_width = int(zombie_health_width * (enemy["health"] / 2))
                pygame.draw.rect(screen, GREEN, (enemy["x"] + enemy_width//2 - zombie_health_width//2, 
                                                enemy["y"] - 10, 
                                                current_health_width, zombie_health_height))
            else:
                screen.blit(enemy_texture_dead, (enemy["x"], enemy["y"]))

        if miniboss and miniboss["alive"]:
            miniboss_texture = miniboss_textures[miniboss["direction"]][miniboss["frame"]]
            screen.blit(miniboss_texture, (miniboss["x"], miniboss["y"]))
            
            # Vykreslení zdraví minibosse
            boss_health_width = 150
            boss_health_height = 10
            pygame.draw.rect(screen, RED, (miniboss["x"] + miniboss_width//2 - boss_health_width//2, 
                                          miniboss["y"] - 20, 
                                          boss_health_width, boss_health_height))
            
            current_health_width = int(boss_health_width * (miniboss["health"] / miniboss_health))
            pygame.draw.rect(screen, GREEN, (miniboss["x"] + miniboss_width//2 - boss_health_width//2, 
                                            miniboss["y"] - 20, 
                                            current_health_width, boss_health_height))

        for bullet in bullets:
            pygame.draw.rect(screen, BLACK, (bullet["x"], bullet["y"], bullet_width, bullet_height))
            
        # Vykreslení uživatelského rozhraní
        wave_text = font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(wave_text, (50, 50))

        # Vykreslení health baru hráče
        draw_health_bar()

        # Vykreslení počtu mincí
        coins_text = font.render(f"Coins: {player_coins}", True, YELLOW)
        screen.blit(coins_text, (WIDTH - 300, 50))
        
        # Game over obrazovka
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
            
        game_over_text = font.render("GAME OVER", True, RED)
        score_text = font.render(f"Wave Reached: {wave}", True, WHITE)
        restart_text = font.render("Press R to Restart or ESC to Quit", True, WHITE)
            
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        elif keys[pygame.K_r]:
            running = False
            main_menu()  
            
            
            # Aktualizace obrazovky
    pygame.display.update()
    
pygame.quit()	

