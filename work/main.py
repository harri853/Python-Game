# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:46:22 2020

@author: Alex
"""

# Import libraries and modules
import pygame
import game
import utils.engine as eng

# Global variables
WIDTH = 800
HEIGHT = 600
FRAMERATE = 60

# Load menu assets
# All images were drawn by Peggy
play_img = pygame.image.load('images/menu/play.jpeg')
options_img = pygame.image.load('images/menu/options.jpeg')
quit_img = pygame.image.load('images/menu/quit.jpeg')
background_img = pygame.image.load('images/menu/background.jpeg')

comic1_img = pygame.image.load('images/comic1.jpeg')
comic2_img = pygame.image.load('images/comic2.jpeg')
cheatsheet_img = pygame.image.load('images/cheatsheet.png')

bgmusic_img = pygame.image.load('images/menu/options/bgmusic.jpeg')
bgmusicoff_img = pygame.image.load('images/menu/options/bgmusicoff.jpeg')
sfx_img = pygame.image.load('images/menu/options/sfx.jpeg')
sfxoff_img = pygame.image.load('images/menu/options/sfxoff.jpeg')

back_img = pygame.image.load('images/menu/options/back.jpeg')


# Initialise modules
pygame.init()

# Center screens
eng.CenterWindow()

# Initialise clock
clock = pygame.time.Clock()

# Initialise screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(pygame.Color("Black")) 
pygame.display.flip()

# Variables for bg music, sfx and screen flags for navigation
bg_on = True
mute = False
screen_flag = "main_menu"

# Loads music (music made by Harri)
pygame.mixer.music.load('sound/longspookydogmusic.mp3')
pygame.mixer.music.play(-1)

# Loads menu sfx
# Source: 
menu_sound = pygame.mixer.Sound("sound/music for game/spookymenubuttonpress.wav")   


# Application Loop
while True:
    # Set screen mode
    # Ensure mouse is visible
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mouse.set_visible(True) 
    
    # Use of screen flags to navigate through the main menu
    # Set screen title of main menu
    # Set menu background image 
    if screen_flag == "main_menu":
        pygame.display.set_caption("Main Menu") 
        eng.DrawStaticBackground(screen, WIDTH, HEIGHT, background_img) 
        
        # Draw main menu buttons
        play_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 3, play_img)
        options_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 4, options_img)
        quit_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 5, quit_img)
    
    # Repeat for options menu
    elif screen_flag == "options":
        pygame.display.set_caption("Options")
        eng.DrawStaticBackground(screen, WIDTH, HEIGHT, background_img)
        
        # Draw options buttons, includes an on/ off img version for each button
        # bg_on and mute used to determine which img version to use
        if bg_on == True:
            bgmusic_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 3, bgmusic_img)
        elif bg_on == False:
            bgmusic_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 3, bgmusicoff_img)
            
            
        if mute == False:
            sfx_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 4, sfx_img)
        elif mute == True:
            sfx_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 4, sfxoff_img)

        # Back button used to navigate back to main menu if needed   
        back_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 5, back_img)
    
    # Screen flags here for comic images 
    elif screen_flag == "comic_1":
        pygame.display.set_caption("Bone Voyage") 
        eng.DrawStaticBackground(screen, WIDTH, HEIGHT, comic1_img) 
    
    elif screen_flag == "comic_2":
        pygame.display.set_caption("Bone Voyage") 
        eng.DrawStaticBackground(screen, WIDTH, HEIGHT, comic2_img) 


    # Screen flags here for cheat sheet after the comics have been cycled through
    # Includes play button which will lead to the game screen 
    # Game takes mute in order to maintain sfx choices made earlier
    elif screen_flag == "cheat_sheet":
        eng.DrawStaticBackground(screen, WIDTH, HEIGHT, cheatsheet_img) 
        pygame.display.set_caption("Instructions")
        play_button = eng.DrawMenuButton(screen, WIDTH, HEIGHT, 5.3, play_img)
        
    elif screen_flag == "game":
        screen_flag = "main_menu"
        game.Game(screen, mute)
        
    
    # Click down events for buttons
    # With each click of a button a screen flag is triggered sending player to another screen    
    # Get mouse location
    mouse_xpos, mouse_ypos = pygame.mouse.get_pos() 
    for event in pygame.event.get():
        # Window close event
        if event.type == pygame.QUIT: 
            eng.Shutdown()
        # Click down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # All button events for main menu here
                # Includes play, options and quit
                # Use of mute variable to play/ not play a sfx
                if screen_flag == "main_menu":
                    if play_button.collidepoint(mouse_xpos, mouse_ypos):
                        if mute == False:
                            pygame.mixer.Sound.play(menu_sound)
                        screen_flag = "comic_1"
                    if options_button.collidepoint(mouse_xpos, mouse_ypos):
                        if mute == False:
                            pygame.mixer.Sound.play(menu_sound)
                        screen_flag = "options"
                    if quit_button.collidepoint(mouse_xpos, mouse_ypos):
                        eng.Shutdown()
                        
                # Cheat sheet shows instructions with a play button which takes
                # player to the game screen 
                elif screen_flag == "cheat_sheet":
                    if play_button.collidepoint(mouse_xpos, mouse_ypos):
                        if mute == False:
                            pygame.mixer.Sound.play(menu_sound)
                        screen_flag = "game"
                
                # Options menu button events here 
                # If back button is pressed player is taken back to main menu
                # Bg music button changes depending on click and previous bg_on value
                # Repeated for sfx
                # Mute function used to allow for storage and changing of mute variable
                elif screen_flag == "options":
                    if back_button.collidepoint(mouse_xpos, mouse_ypos):
                        if mute == False:
                            pygame.mixer.Sound.play(menu_sound)
                        screen_flag = "main_menu"
                        
                    if bgmusic_button.collidepoint(mouse_xpos, mouse_ypos):
                        if mute == False:
                            pygame.mixer.Sound.play(menu_sound)
                        if bg_on == True: 
                                pygame.mixer.music.pause()
                                bg_on = False
                        else:
                            pygame.mixer.music.load('sound/longspookydogmusic.mp3')
                            pygame.mixer.music.play(-1)
                            bg_on = True
                            
                    if sfx_button.collidepoint(mouse_xpos, mouse_ypos):
                        if mute == False:
                            pygame.mixer.Sound.play(menu_sound)
                        mute = eng.FuncPeggy.Mute(mute)
                
                # comic1 and comic2 is chained with each other
                # Requires a click to go to next one 
                elif screen_flag == "comic_1":
                     screen_flag = "comic_2"
                     
                elif screen_flag == "comic_2":
                    screen_flag = "cheat_sheet"
                        
                        
                        

    clock.tick(FRAMERATE)
    pygame.display.flip()   
            
 