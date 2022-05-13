import pygame
import os
import time
import random
pygame.font.init()

x = 1920
y = 320

killed = 0

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

WIDTH, HEIGHT = 1000, 1200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Player Ship
PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("SpaceshipImages","player_ship.png"))
PLAYER_SIZE = (50, 50)

# Enemy Ships
XXSMALL_GRAY_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","xxs_gray.png")), (40, 40))
XXSMALL_BLACK_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","xxs_black.png")), (40, 40))

XSMALL_GRAY_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","xs_gray.png")), (45, 45))
XSMALL_BLACK_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","xs_black.png")), (45, 45))

SMALL_GRAY_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","small_gray.png")), (50, 50))
SMALL_BLACK_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","small_black.png")), (50, 50))

MEDIUM_GRAY_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","m_gray.png")), (80, 70))
MEDIUM_BLACK_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","m_black.png")), (80, 70))

LARGE_GRAY_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","l_gray.png")), (100, 90))
LARGE_BLACK_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("SpaceshipImages","l_black.png")), (100, 90))

# Lasers
RED_LASER_BULLETS = pygame.image.load(os.path.join("Lasers","red_laser.png"))
BLUE_LASER_BULLETS = pygame.image.load(os.path.join("Lasers","blue_laser.png"))
RED_LASER_MISSLE = pygame.image.load(os.path.join("Lasers","red.missle.png"))
BLUE_LASER_MISSLE = pygame.image.load(os.path.join("Lasers","blue_missle.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Background","space.png")), (WIDTH, HEIGHT))



class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 1

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                print(obj.health)
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()





class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(PLAYER_SPACE_SHIP, PLAYER_SIZE)
        self.laser_img = BLUE_LASER_BULLETS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


    def move_lasers(self, vel, enemies):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for enemy in enemies:
                    if laser.collision(enemy):
                        enemy.max_health -= 10
                        self.lasers.remove(laser)
                        if enemy.max_health <= 0:
                            enemies.remove(enemy)
                            global killed
                            killed += 1




    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+26, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
            super().draw(window)
            self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "xxs_gray": (XXSMALL_GRAY_SPACE_SHIP, RED_LASER_BULLETS),
                "xs_gray": (XSMALL_GRAY_SPACE_SHIP, RED_LASER_BULLETS),
                "s_gray": (SMALL_GRAY_SPACE_SHIP, RED_LASER_BULLETS),
                "m_gray": (MEDIUM_GRAY_SPACE_SHIP, RED_LASER_MISSLE),
                "l_gray": (LARGE_GRAY_SPACE_SHIP, RED_LASER_MISSLE),
                "xxs_black": (XXSMALL_BLACK_SPACE_SHIP, RED_LASER_BULLETS),
                "xs_black": (XSMALL_BLACK_SPACE_SHIP, RED_LASER_BULLETS),
                "s_black": (SMALL_BLACK_SPACE_SHIP, RED_LASER_BULLETS),
                "m_black": (MEDIUM_BLACK_SPACE_SHIP, RED_LASER_MISSLE),
                "l_black": (LARGE_BLACK_SPACE_SHIP, RED_LASER_MISSLE)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move(self, vel):
        self.y += vel


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+18, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.max_health/self.health), 10))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    crashed = 0

    main_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 50)

    enemies = []
    wave_length = 0
    enemy_vel = 2

    player_vel = 7.5
    laser_vel = 7.5

    player = Player(450, 900)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        crash_label = main_font.render(f"Crashed: {crashed}", 1, (255,255,255))
        killed_label = main_font.render(f"Killed: {killed}", 1, (255,255,255))

        # added a kill counter to keep track of how many total enemies there are per wave.
        WIN.blit(killed_label, (10, 90))
        WIN.blit(crash_label, (10, 50))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))


        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)


        if lost:
            lost_label = lost_font.render("You lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue


        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):

                # enemies weren't increasing in the correct rate due to the wave_length variable being set to five.
                if level <= 4:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["xxs_gray", "xs_gray", "s_gray"]))
                    enemies.append(enemy)

                elif level <= 5:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["xs_gray", "s_gray", "m_gray"]))
                    enemies.append(enemy)
                elif level <= 10:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["s_gray", "m_gray"]))
                    enemies.append(enemy)
                elif level <= 19:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["s_gray", "m_gray", "l_gray"]))
                    enemies.append(enemy)
                elif level <= 20:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["xxs_black", "xs_black", "s_black"]))
                    enemies.append(enemy)
                elif level <= 24:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["xxs_black", "xs_black", "s_black"]))
                    enemies.append(enemy)
                elif level <= 25:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["s_black", "m_black"]))
                    enemies.append(enemy)
                elif level <= 29:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["s_black", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level <= 30:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["xs_gray", "s_gray", "m_gray", "l_gray", "xs_black", "s_black", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level <= 49:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["xs_gray", "s_gray", "m_gray", "l_gray", "xs_black", "s_black", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level <= 50:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["s_gray", "m_gray", "l_gray", "s_black", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level <= 74:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["s_gray", "m_gray", "l_gray", "s_black", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level <= 75:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["m_gray", "l_gray", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level <= 99:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["m_gray", "l_gray", "m_black", "l_black"]))
                    enemies.append(enemy)
                elif level >= 100:
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["l_gray", "l_black"]))
                    enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()



        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)



            if random.randrange(0, 4*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                crashed = 0
                enemies.remove(enemy)
                crashed += 1

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to be begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()