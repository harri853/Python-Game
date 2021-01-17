# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 12:04:12 2020

@author: Alex
"""
# Import libraries and modules
import pygame, sys, os
import random

# Import individual contribuutions
import utils.alex as FuncAlex
import utils.harri as FuncHarri
import utils.hongyuan as FuncHongyuan
import utils.peggy as FuncPeggy

# Classes and Functions

# Shutdown application
def Shutdown():
    pygame.quit()
    sys.exit()
    os._exit()
    
def CenterWindow():
    FuncAlex.CenterWindow()

# Draw menu buttons - centered on screen (stackable)
def DrawMenuButton(window, width, height, button_number, image):
    return FuncAlex.DrawMenuButton(window, width, height, button_number, image)

# Draw static background - useful for menu screens etc
def DrawStaticBackground(window, width, height, image):
    FuncAlex.DrawStaticBackground(window, width, height, image)
    
# Draw Level Screen    
def DrawLevelScreen(window, width, height, image, level):
    FuncAlex.DrawLevelScreen(window, width, height, image, level)

    
# Draw infinite scroll
def DrawScrollBackground(window, width, speed, image, fps, x):
    return FuncAlex.DrawScrollBackground(window, width, speed, image, fps, x)


#%% Harri's code

""" GLOBAL VAR HARDCODED - REPLACE """
screen_width = 1600
screen_height = 900
#code is mainly reused here
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        # Player image loaded in 
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect(center=(screen_width/2,screen_height/2))
        self.life = 1

    def update(self, image):
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect.center = pygame.mouse.get_pos()
     
    # Return bullets and has the position of wherever the mouse is
    def create_rightbullet(self, image):
        return RightBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], image) 

    def create_leftbullet(self, image):
        return LeftBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], image) 

    def create_downbullet(self, image):
        return DownBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], image) 

    def create_upbullet(self, image):
        return UpBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], image)

    def create_bullet(self, image):
        return Bullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], image) 


# Bullet class 
class Bullet(pygame.sprite.Sprite):
   def __init__(self,pos_x, pos_y, image):
       super().__init__()
       # Bullet image loaded in 
       bullet_img = image.convert_alpha()
       self.image = pygame.Surface((50, 10))
       self.image = bullet_img
       self.rect = self.image.get_rect(center = (pos_x,pos_y))
       

   def update(self):
       self.rect.x += 10
       #If bullet goes too far to the right, bullet will destroy itself to save memory and improve performance
       if self.rect.x >= screen_width + 200: 
           self.kill() 

# Mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self, images, level):
        # Animation loops for mobs
        self.mob_frame_loop = 0
        self.mob_frame = 0
        self.images = images
        self.level = level
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(images[self.mob_frame], (100, 100))
        self.rect = self.image.get_rect()
        
        # Spanwns them on x axis outside of screen to the right and in a random place to the right of the screen
        # Randomise their speed along with level
        self.rect.y = random.randrange(screen_height - self.rect.height)
        self.rect.x = random.randrange(screen_width + 100, screen_width+500)
        self.speedx = random.randrange(5, 10) * self.level
        self.speedy = random.randrange(-2, 2)

    def update(self):
        #mobs go in left direction
        self.rect.x -= self.speedx 
        self.rect.y -= self.speedy #speed of y
        self.mob_frame_loop += 1
        self.mob_frame = (self.mob_frame_loop // 5) % 2
        self.image = pygame.transform.scale(self.images[self.mob_frame], (100, 100))
        
        # Mobs would take too long to travel to -100 so they respawn when they get to y < - 25 and y > sh + 25
        if self.rect.x <= -100 or self.rect.y < -25 or self.rect.y > screen_height + 25: 
            self.rect.y = random.randrange(screen_height - self.rect.height)  
            self.rect.x = random.randrange(screen_width + 100, screen_width + 500)  
            self.speedx = random.randrange(5, 10) * self.level


class Boss(pygame.sprite.Sprite): #spawn boss
    def __init__(self, HEIGHT, WIDTH):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        pygame.sprite.Sprite.__init__(self)
        self.sizex = 200
        self.sizey = 350
        self.image = pygame.Surface((self.sizex,self.sizey))


        boss_img = pygame.image.load('images/game/mob/cerberwoof.png').convert_alpha()
        self.image = boss_img
        
        self.image = pygame.transform.scale(boss_img, (200, 350))
        self.rect = self.image.get_rect()
        
        self.rect.y = (HEIGHT/2) - 175#spanwns them on x axis outside of screen to the right
        self.rect.x = WIDTH - 200
        self.speedy = 4


    def create_boss_bullet(self, boss):
        return Boss_Bullet(boss.rect.x, boss.rect.y, boss.sizey)


class Boss_Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,sizey):
        super().__init__()
        self.image = pygame.Surface((50, 10))
        boss_bullet_img = pygame.image.load('images/game/mob/bosswoof.png').convert_alpha()
        self.image = boss_bullet_img
        self.y_speed = random.randrange(-2, 2)
        self.image = pygame.transform.scale(boss_bullet_img, (100, 100))
        self.rect = self.image.get_rect(center = (pos_x,pos_y + (sizey/2)))

    def update(self):
        self.rect.x -= 10 #shoots along x axis left
        self.rect.y += self.y_speed

        if self.rect.x < -100: #if bullet goes too far to the left
            self.kill() #bullet will destroy itself to save memory and improve performance


#%% Peggy's code
# Bullets in various directions to be used for the star bullet boost
class RightBullet(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, image):
        super().__init__()
        bullet_img = image.convert_alpha()
        self.image = pygame.Surface((50, 10))
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.downwards = False

        
    def update(self):
        self.rect.x += 5
        # If bullet goes too far to the right, bullet will destroy itself to save memory and improve performance
        if self.rect.x >= screen_width + 100: 
            self.kill() 
            
class LeftBullet(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, image):
        super().__init__()
        bullet_img = image.convert_alpha()
        self.image = pygame.Surface((50, 10))
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.downwards = False

        
    def update(self):
        self.rect.x -= 5
        # If bullet goes too far to the left, bullet will destroy itself to save memory and improve performance
        if self.rect.x < -100: 
            self.kill() 
       
        
class DownBullet(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, image):
        super().__init__()
        bullet_img = image.convert_alpha()
        bullet_img = pygame.transform.rotate(bullet_img, 90)
        self.image = pygame.Surface((10, 50))
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.downwards = False

        
    def update(self):
        self.rect.y += 5
        # If bullet goes too far down, bullet will destroy itself to save memory and improve performance
        if self.rect.y >= screen_height + 100: 
            self.kill() 
       
class UpBullet(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, image):
        super().__init__()
        bullet_img = image.convert_alpha()
        bullet_img = pygame.transform.rotate(bullet_img, 90)
        self.image = pygame.Surface((10, 50))
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.downwards = False

        
    def update(self):
        self.rect.y -= 5
        # If bullet goes too far to up, bullet will destroy itself to save memory and improve performance
        if self.rect.x < -100: 
            self.kill() 
       
               
# Heart Life up class           
class Heart(pygame.sprite.Sprite): 
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        # Image for heart added 
        heart_img = image.convert_alpha()
        heart_img = pygame.transform.scale(heart_img, (100, 100))
        self.image = heart_img
        self.rect = self.image.get_rect()
        
        # Spanwns them on x axis outside of screen to the right
        # Spawn in a random place to the right of the screen
        # Randomises speed movement using speedx 
        self.rect.y = random.randrange(screen_height - self.rect.height)
        self.rect.x = random.randrange(screen_width + 100, screen_width + 500)  
        self.speedx = random.randrange(5, 10) 

    def update(self):
        # Boosts go in left direction
        self.rect.x -= self.speedx 
        if self.rect.x <= -100:
            self.rect.y = random.randrange(screen_height - self.rect.height)  
            self.rect.x = random.randrange(screen_width + 100, screen_width + 500)   
            self.speedx = random.randrange(5, 10) 
     
        # If heart goes too far to the right remove the heart
        if self.rect.x <= -self.rect.width: 
            self.kill()
            

# Star bullet boost class 
class StarBullet(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        # Image for star bullet added
        starbullet_img = image.convert_alpha()
        starbullet_img = pygame.transform.scale(starbullet_img, (100, 100))
        self.image = starbullet_img
        self.rect = self.image.get_rect()
        
        # Spanwns them on x axis outside of screen to the right
        # Spawn in a random place to the right of the screen
        # Randomises speed movement using speedx 
        self.rect.y = random.randrange(screen_height - self.rect.height) 
        self.rect.x = random.randrange(screen_width + 100, screen_width + 500)  
        self.speedx = random.randrange(5, 10)  

    def update(self):
        # Boosts go in left direction
        self.rect.x -= self.speedx 
        if self.rect.x <= -100:
            self.rect.y = random.randrange(screen_height - self.rect.height)  
            self.rect.x = random.randrange(screen_width + 100, screen_width + 500)   
            self.speedx = random.randrange(5, 10) 

        # If star bullet goes too far to the right remove the star bullet
        if self.rect.x <= -self.rect.width: 
            self.kill()
            
# Mute function for sfx button          
def Mute(mute):
    return FuncPeggy.Mute()





