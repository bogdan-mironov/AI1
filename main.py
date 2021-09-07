import os
import pygame
import time
import random
import math
pygame.font.init()

WIDTH,HEIGHT = 550,550
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shit seizer")

#Enemies
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#Player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))


class Ship:
    def __init__(self,x,y,health =100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.attackCD = 0
    def draw(self,window,angle = None):
        ship_img_rotated = pygame.transform.rotozoom(self.ship_img,angle,1)
        SIR_rect= ship_img_rotated.get_rect(center = (self.ship_img.get_width()/2+self.x,self.ship_img.get_height()/2+self.y))
        window.blit(ship_img_rotated,SIR_rect)
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
    



class Player(Ship):
    def __init__(self,x,y,health = 100):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP ={
                "red":(RED_SPACE_SHIP,RED_LASER),
                "green":(GREEN_SPACE_SHIP,GREEN_LASER),
                "blue":(BLUE_SPACE_SHIP,BLUE_LASER)
        }
    def __init__  (self,x,y, color, health = 100):
        super().__init__(x,y,health)
        self,ship_img,self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,enemy_velocity):
        self.y += enemy_velocity

def main():
    run = True
    FPS = 60

    player_velocity = 3
    player = Player(300,250)
    
    clock = pygame.time.Clock()

    BG_loop_point = 0

    enemies = []
    wave_length = 5
    enemy_velocity = 1
    main_font = pygame.font.SysFont("comicsans",50)
    def redraw_window():


        WIN.blit(BG,(0,BG_loop_point-HEIGHT))
        WIN.blit(BG,(0,BG_loop_point))


        cursor = pygame.mouse.get_pos()
        player_center = (player.ship_img.get_width()/2+player.x,player.ship_img.get_height()/2+player.y)

        angle = math.atan2(player_center[1]-cursor[1],cursor[0]-player_center[0])
        degree = math.degrees(angle) - 90

        window_info = main_font.render(f"{(player_center[0],player_center[1])},{pygame.mouse.get_pos()},{degree}",1,(255,0,0))
        WIN.blit(window_info,(10,10))

        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN,degree)
        pygame.display.update()

    
    while run:
        clock.tick(FPS)
        redraw_window()
        BG_loop_point+= 1
        if BG_loop_point == 550:
            BG_loop_point = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 10:
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x - player_velocity + player.get_width() < WIDTH - 10:
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity >  10:
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y - player_velocity  + player.get_height()< HEIGHT - 10:
            player.y += player_velocity
        
main()
        
