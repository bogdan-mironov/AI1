import os
import pygame
import time
import random
import math
pygame.font.init()

WIDTH,HEIGHT = 550,550
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("seizer")

#Enemies
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png")).convert_alpha()
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png")).convert_alpha()
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png")).convert_alpha()

#Player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png")).convert_alpha()

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png")).convert_alpha()
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png")).convert_alpha()
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png")).convert_alpha()
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png")).convert_alpha()

COLOR_MAP = {
            "red":(RED_SPACE_SHIP,RED_LASER),
            "green":(GREEN_SPACE_SHIP,GREEN_LASER),
            "blue":(BLUE_SPACE_SHIP,BLUE_LASER)
}
##
ENEMY_SPEED = 2
PLAYER_SPEED = 4
LASER_SPEED = 6

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

##
font = pygame.font.SysFont("courier new",15)

enemies = []
lasers = []

class Ship:
    def __init__(self,x,y,health =100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.attackCD = 10
    def draw(self,window,degree = 180):
        ship_img_rotated = pygame.transform.rotozoom(self.ship_img,degree,1)
        #SIR_rect= ship_img_rotated.get_rect(center = (self.ship_img.get_width()/2+self.x,self.ship_img.get_height()/2+self.y))
        window.blit(ship_img_rotated,(self.x,self.y))

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
    
class Player(Ship):
    def __init__(self,x,y,health = 100):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = pygame.transform.scale(YELLOW_LASER,(40,80))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.attackCD = 30
    def shoot(self):
        laser = Laser(self.x,self.y,self.laser_img)
        lasers.append(laser)

class Enemy(Ship):
    def __init__(self,x,y,color,health = 100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self):
        self.y += ENEMY_SPEED
class Laser:
    def __init__(self,x,y,laser_img):
        self.x = x + laser_img.get_width()/2
        self.y = y
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(laser_img)
    def draw(self,window):
        window.blit(self.laser_img,(self.x,self.y))
        self.move()
    def move(self):
        self.y -= 1 * LASER_SPEED

        for enemy in enemies:
            if self.collision(enemy):
                enemies.remove(enemy)
                print("ok")
                lasers.remove(self)
    def collision(self,obj2):
        obj2_rect = obj2.ship_img.get_rect(center = (obj2.ship_img.get_width()/2+obj2.x, obj2.ship_img.get_height()/2+obj2.y))
        obj1_rect = self.laser_img.get_rect(center = (self.x + self.laser_img.get_width()/2, self.laser_img.get_height()/2+self.y))
        offset_x = obj2_rect.x - obj1_rect.x
        offset_y = obj2_rect.y - obj1_rect.y
        return self.mask.overlap(obj2.mask,(offset_x,offset_y)) != None


player = Player(300,250)
def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    wave = 5

    BG_loop_point = 0
    def redraw_window():

        #background
        WIN.blit(BG,(0,BG_loop_point-HEIGHT))
        WIN.blit(BG,(0,BG_loop_point))


        cursor = pygame.mouse.get_pos()
        player_center = (player.ship_img.get_width()/2+player.x,player.ship_img.get_height()/2+player.y)

        # enemies toberedone
        for enemy in enemies:
            enemy.draw(WIN)

        for laser in lasers:
            laser.draw(WIN)

        player.draw(WIN,0)

        #interface
        health = font.render(f"{player.health}",1,(255,0,0))
        level = font.render("4",1,(255,0,0))

        WIN.blit(health,(10,HEIGHT-health.get_height()))
        WIN.blit(level,(WIDTH-level.get_width(),HEIGHT-level.get_height()))
        pygame.display.update()

    count = 0
    while run:
        clock.tick(FPS)

        if count <= 60:
            count += 1
        else:
            count = 0

        if len(enemies) == 0:
            for i in range(wave):
                enemy = Enemy(random.randrange(50, WIDTH-50),random.randrange(-500,-100),random.choice(["blue","green","red"]))
                enemies.append(enemy)
        for enemy in enemies:
            enemy.move()
            if (enemy.y + enemy.get_height() > HEIGHT):
                player.health -= 10
                enemies.remove(enemy)


        BG_loop_point+= 1
        if BG_loop_point == HEIGHT:
            BG_loop_point = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_SPEED > 10:
            player.x -= PLAYER_SPEED       
        if keys[pygame.K_d] and player.x - PLAYER_SPEED + player.get_width() < WIDTH - 10:
            player.x += PLAYER_SPEED
        if keys[pygame.K_w] and player.y - PLAYER_SPEED >  10:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_s] and player.y - PLAYER_SPEED  + player.get_height()< HEIGHT - 10:
            player.y += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            if count > player.attackCD:
                player.shoot()
                count = 0
            
        redraw_window()

        
        
main()