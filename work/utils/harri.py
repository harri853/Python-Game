# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:49:03 2020

@author: Harri
"""
# Import libraries and modules
import pygame, sys
# Import individual contribuutions
import utils.alex as FuncAlex
import utils.hongyuan as FuncHongyuan
import utils.peggy as FuncPeggy
#inspiration taken from https://www.youtube.com/watch?v=JmpA7TU_0Ms
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100,100))#100pixels wide and high
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center=(screen_width/2,screen_height/2))
        self.life = 1

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    
    def create_rightbullet(self):
        return RightBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) #return bullet and has the position of wherever the mouse is

    def create_leftbullet(self):
        return LeftBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) #return bullet and has the position of wherever the mouse is

    def create_downbullet(self):
        return DownBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) #return bullet and has the position of wherever the mouse is

    def create_upbullet(self):
        return UpBullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) #return bullet and has the position of wherever the mouse is


##Inspiration taken from https://www.youtube.com/watch?v=-5GNbL33hz0&t=328s @ 3:00
#
#class Bullet(pygame.sprite.Sprite):
#    def __init__(self,pos_x,pos_y):
#        super().__init__()
#        self.image = pygame.Surface((50, 10))
#        self.image.fill((255,0,0))#colour
#        self.rect = self.image.get_rect(center = (pos_x,pos_y))
#
#    def update(self):
#        self.rect.x += 5 #bullet speed
#
#        if self.rect.x >= screen_width + 200: #if bullet goes too far to the right,
#            self.kill() #bullet will destroy itself to save memory and improve performance
            
class Mob(pygame.sprite.Sprite): #spawn enemies
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(screen_height - self.rect.height)#spanwns them on x axis outside of screen to the right
        self.rect.x = random.randrange(screen_width + 100, screen_width + 500)
        self.speedx = random.randrange(3, 8)# randomise their speed

    def update(self):
        self.rect.x -= self.speedx #mobs go in left direction
        if self.rect.x <= 0:
            self.rect.y = random.randrange(screen_height - self.rect.height)  # spanwns them on x axis outside of screen to the right
            self.rect.x = random.randrange(screen_width + 100, screen_width + 500)  # spawn in a random place to the right of the screen
            self.speedx = random.randrange(3, 8)  # randomise their speed

           

   
      
