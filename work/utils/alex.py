# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:49:06 2020

@author: Alex
"""
# Import libraries and modules
import pygame
import os
import random


# Center window function - os function call 
def CenterWindow():
    os.environ['SDL_VIDEO_CENTERED'] = '1' # This line of code was found on stackoverflow

# Draw menu buttons - center of window (stackabele)
def DrawMenuButton(window, width, height, button_number, image):
    # Set proportions relative to page
    XDIVISOR = 2
    YDIVISOR = 11
    # Set button dimensions
    button_width = width//XDIVISOR
    button_height = height//YDIVISOR
    # Set button location
    x = width//2 - button_width//2
    y = (2 * button_height * button_number) - button_height
    # Draw button on page
    buttonRect = pygame.Rect(x, y, button_width, button_height)
    image = pygame.transform.scale(image, (button_width, button_height))
    window.blit(image, buttonRect)
    
    return buttonRect

# Draw static background - menu screens etc
def DrawStaticBackground(window, width, height, image):
    backgroundRect = pygame.Rect(0, 0, width, height)
    image = pygame.transform.scale(image, (width, height))
    window.blit(image, backgroundRect)
    
# Draw Level Screen    
def DrawLevelScreen(window, width, height, image, level):
    # Draw background
    DrawStaticBackground(window, width, height, image)
    # Draw text over background
    myfont = pygame.font.SysFont('Comic Sans MS', 120)
    level_text = myfont.render("Level " + str(level), False, (153, 0, 153))
    window.blit(level_text, level_text.get_rect(center=(width//2, height//2)))
    pygame.display.flip()
    # Display and pause game for 750 ms
    pygame.time.wait(750)

# Draw infinite scroll
def DrawScrollBackground(window, width, speed, image, fps, x):
    # Move image from right to left
    x -= width // (fps * speed)
    window.blit(image, (x, 0))
    return x
        