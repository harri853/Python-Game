# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 19:05:08 2020

@author: wongp
"""
import pygame
import utils.engine as eng
import random


# Global variables
WIDTH = 1600
HEIGHT = 900
FRAMERATE = 60
GREEN = (0, 255, 0)
BLACK = (0,0,0)

# Load assests
# All images were drawn by Peggy
backgrounds_all = [[pygame.image.load('images/game/background/garden (low).jpeg')],
                   [pygame.image.load('images/game/background/graveyard (high).jpeg')]]
backgrounds = backgrounds_all[1]
level_img = pygame.image.load('images/game/background/graveyard (low).jpeg')
gameover_img = pygame.image.load('images/game/gameover.jpeg')

player_animations = [pygame.image.load('images/game/player/skull' + str(i) + ".png") for i in range (1, 9)]
mob_animations = [pygame.image.load('images/game/mob/woof' + str(i) + ".png") for i in range (1, 3)]
heart_animations = [pygame.image.load('images/game/boosts/heart' + str(i) + ".png") for i in range (1, 3)]

cheatsheet_img = pygame.image.load('images/boss_instructions.jpeg')
bullet_img = pygame.image.load('images/game/player/bullet.png')
starbullet_img = pygame.image.load('images/game/boosts/starbullet.png')
heart_img = pygame.image.load('images/game/boosts/heart1.png')

victory1_img = pygame.image.load('images/game/victory1.jpeg')
victory2_img = pygame.image.load('images/game/victory2.jpeg')


def Boss(screen, mute, score, level, lives):
    global backgrounds_all, backgrounds   
    
    # We do not own sfx sounds 
    # Source: 
    gameover_sound = pygame.mixer.Sound("sound/music for game/gameover.wav") 
    lifeup_sound = pygame.mixer.Sound("sound/music for game/lifeupsound.wav") 
    mobgothit_sound = pygame.mixer.Sound("sound/music for game/mobgothit.wav") 
    playergothit_sound = pygame.mixer.Sound("sound/music for game/playergothit.wav") 
    spookyplayershoot_sound = pygame.mixer.Sound("sound/music for game/spookyplayershoot.wav") 
    starbulletpickup_sound = pygame.mixer.Sound("sound/music for game/starbulletpickup.wav") 

    
    # Initialise clock
    clock = pygame.time.Clock()
    offset = pygame.time.get_ticks() // 1000

    # Initialise screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color("White")) 
    pygame.display.flip()
    
    # Set screen title
    pygame.display.set_caption("Bone Voyage") 
    
    pygame.mouse.set_visible(False) # Hide mouse 
    
    
    # Player group
    player_loop, player_frame = 0, 0
    player = eng.Player(player_animations[player_frame])
    player_group = pygame.sprite.Group()
    player_group.add(player)

    #Player bullet group
    bullet_group = pygame.sprite.Group()

    #boss bullet group
    boss_bullet_group = pygame.sprite.Group()

    # Bullet group one group for each bullet direction
    rightbullet_group = pygame.sprite.Group()
    leftbullet_group = pygame.sprite.Group()
    downbullet_group = pygame.sprite.Group()
    upbullet_group = pygame.sprite.Group()
    
    # Mob group
    # With adjustable number of mobs using mob_number
    mob = pygame.sprite.Group()
    mob_number = 5
    for i in range(mob_number):
        m = eng.Mob(mob_animations, 1)
        mob.add(m)

    # Boss Group
    boss = eng.Boss(HEIGHT, WIDTH)
    boss_group = pygame.sprite.Group()
    boss_group.add(boss)
    previous_time = pygame.time.get_ticks()
        
    # Heart group
    # With adjustable number of hearts
    heart = pygame.sprite.Group()
    heart_number = 1
    for i in range(heart_number):
        h = eng.Heart(heart_img)
        heart.add(h)
        
    # Bullet star group
    # With adjustable number of bullet stars
    starbullet = pygame.sprite.Group()
    for i in range(1):
        s = eng.StarBullet(starbullet_img)
        starbullet.add(s)  
    
    # Score and a separate variable for kill counter
    score_init = score
    kills = 0
    
    boss_life = 100
    lives_init = lives
    player.life = lives_init

    # Init background
    scroll_bg = [0, WIDTH]
    bg=[0, 0]
    for i in range(2):
        index = random.randint(0, len(backgrounds)-1)
        bg[i] = backgrounds[index]
    
    speed = 2
    
    
    # Pausing element added here 
    # Theory for the pausing is taken from another person
    # Source: https://stackoverflow.com/questions/30744237/how-to-create-a-pause-button-in-pygame
    pause = False
    game_running = True
    state = game_running
    while game_running:
        # Event loop
        # Get mouse location
        mouse_xpos, mouse_ypos = pygame.mouse.get_pos() 
        left_click = False
        for event in pygame.event.get():
            # Window close event
            if event.type == pygame.QUIT: 
                eng.Shutdown()
            
            # Key down events for escape button and pause button 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                if event.key == pygame.K_p:
                    if state == pause:
                        state = game_running
                    elif state == game_running:
                        state = pause
                        
            # Mouse click down
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    left_click = True
                    
        # State and game running used for pausing screen
        # If the game isn't paused...
        if state == game_running:
         
        # State and game running used for pausing screen
        # If the game isn't paused...
        
            """ SCROLL BACKGROUND """
            for i in range(2):
                scroll_bg[i] = eng.DrawScrollBackground(screen, WIDTH, speed, bg[i], FRAMERATE, scroll_bg[i])
            
            # reset background loop
            # This code is overcomplicated for current use
            # It was intended to take n backgrounds
            # and display them in a random sequence
            # Currently it only used one background on an infinite loop
            if scroll_bg[1] < 0:
                scroll_bg = [0, WIDTH]
                bg[0] = bg[1]
                index = random.randint(0, len(backgrounds)-1)
                bg[1] = backgrounds[index]
            
            """ TIMER AND SCORE """
            # Calculates the total number of seconds at current point in time
            # Code is built from http://programarcadegames.com/python_examples/f.php?file=timer.py
            # Also calculates score based on time spent in game and number of kills
            # Set offset for game timer
            total_seconds = (pygame.time.get_ticks() // 1000) - offset
             
            # Seconds and kills combine to form total score shown to player
            seconds = total_seconds % 60
            if kills > 1 or kills == 1:
                score = seconds + (kills*5) + score_init
            else:
                score = seconds + score_init
            
            
            """ PLAYER MECHANICS """
            # Increment player frame
            player_loop += 1
            if player_loop >= FRAMERATE // (len(player_animations) * speed): # Sync player roll to background
                player_loop = 0
                player_frame += 1
            if player_frame >= len(player_animations):
                player_frame = 0
                
            # Shoots bullet on left click
            if left_click:
                if mute == False:
                    pygame.mixer.Sound.play(spookyplayershoot_sound)
                bullet_group.add(player.create_bullet(bullet_img))
            
             # If player life is 0 game stops
            # Set game over background and updates with wait time
            # Loop stops and game exits
            if player.life == 0:
                if mute == False:
                    pygame.mixer.Sound.play(gameover_sound)
                eng.DrawStaticBackground(screen, WIDTH, HEIGHT, gameover_img) 
                pygame.display.flip() 
                pygame.time.wait(5000) 
                return False 

            
            """ COLLISIONS """
            # Check to see if a bullet hits a mob
            # Bullet needs to run into mob and vice versa so 2 Trues
            #inspiration drawn from https://www.youtube.com/watch?v=1_H7InPMjaY&t=64s 8:00
            bullet_groups = [leftbullet_group, rightbullet_group, upbullet_group, downbullet_group]
            for bullet in bullet_groups:
                mob_hit = pygame.sprite.groupcollide(mob, bullet, True, True)
                # This loop adds a mob if a mob dies
                for hit in mob_hit: 
                    if mute == False:    
                        pygame.mixer.Sound.play(mobgothit_sound)
                    m = eng.Mob(mob_animations, level)
                    mob.add(m)
                    kills += 1
            
            # Separate loop for now for player bullet
            mob_player_hit = pygame.sprite.groupcollide(mob, bullet_group, True, True) 
            # This loop adds a mob if a mob dies
            for hit in mob_player_hit:
                if mute == False:    
                    pygame.mixer.Sound.play(mobgothit_sound)
                
                m = eng.Mob(mob_animations, level) 
                mob.add(m)
                kills += 1
            
            # If the player is hit by a mob the player loses a life 
            # Mob is removed to prevent too many collisions and loss of multiple lives
            player_hit = pygame.sprite.spritecollide(player, mob, True) 
            if player_hit:
                if mute == False:
                    pygame.mixer.Sound.play(playergothit_sound)
                player.life -= 1
                mob.remove(m)
                m = eng.Mob(mob_animations, level)
                mob.add(m)

            player_hit_by_boss = pygame.sprite.spritecollide(player, boss_bullet_group, True)
            if player_hit_by_boss:
                if mute == False:
                    pygame.mixer.Sound.play(playergothit_sound)
                player.life -= 1

            boss_hit_by_player = pygame.sprite.spritecollide(boss, bullet_group,True)
            if boss_hit_by_player:
               boss_life -= 1

            """BOSS"""
            # Boss bullet timing (random intervals within a tolerance of 100ms)
            #inspiration taken from https://stackoverflow.com/questions/48356638/python-how-to-delay-bullet-shooting
            current_time = pygame.time.get_ticks()
            if current_time - previous_time > random.randrange(1000, 2500):
                previous_time = current_time
                boss_bullet_group.add(boss.create_boss_bullet(boss))
                current_time = 0
                
                
            """ BOOSTS """
            # If the player touches heart boost gains a life
            # Heart is removed to prevent too many collisions and gaining of multiple lives
            life_up = pygame.sprite.spritecollide(player, heart, True) 
            if life_up:
                if mute == False:
                    pygame.mixer.Sound.play(lifeup_sound)
                player.life += 1
                heart.remove(h)
            
            # Caps the amount of lives the player can gain
            # Spawns a new life every 20 to 30 seconds
            if player.life < 5:
                if seconds % 25 == 0:
                    h.rect.y = random.randrange(HEIGHT - h.rect.height)  # spanwns them on x axis outside of screen to the right
                    h.rect.x = random.randrange(WIDTH + 100, WIDTH + 500)  # spawn in a random place to the right of the screen
                    heart.add(h)
            
            # If the player touches starbullet, cause bullets to shoot in 4 directions
            # Bullet boost is removed to prevent too many collisions and gaining of multiple, multiple bullets
            bullet_up = pygame.sprite.spritecollide(player, starbullet, True)
            if bullet_up:
                if mute == False:
                    pygame.mixer.Sound.play(starbulletpickup_sound)
                    pygame.mixer.Sound.play(spookyplayershoot_sound)
                leftbullet_group.add(player.create_leftbullet(bullet_img))
                downbullet_group.add(player.create_downbullet(bullet_img))
                rightbullet_group.add(player.create_rightbullet(bullet_img))
                upbullet_group.add(player.create_upbullet(bullet_img))
                starbullet.remove(s)
                
            # Spawns a new star bullet every 30 seconds    
            if seconds % 20 == 0:
                s.rect.y = random.randrange(HEIGHT- s.rect.height)  # spanwns them on x axis outside of screen to the right
                s.rect.x = random.randrange(WIDTH + 100,WIDTH + 500)  # spawn in a random place to the right of the screen
                starbullet.add(s)  
                
            
            
            # Updates and draws everything to screen
            mob.update()
            player_group.update(player_animations[player_frame])
            heart.update()
            starbullet.update()
        
            mob.draw(screen)
            heart.draw(screen)
            rightbullet_group.draw(screen)
            leftbullet_group.draw(screen)
            downbullet_group.draw(screen)
            upbullet_group.draw(screen)
            player_group.draw(screen)
            starbullet.draw(screen)
            bullet_group.draw(screen)
            bullet_group.update()
            rightbullet_group.update()
            leftbullet_group.update()
            downbullet_group.update()
            upbullet_group.update()

            # boss stuff

            boss_bullet_group.update()
            boss_bullet_group.draw(screen)
            boss_group.draw(screen)
    
                
        
            # Section to write score and lives to screen 
            myfont = pygame.font.SysFont(pygame.font.get_default_font(), 50)
            str_lives = str(player.life)
            str_score = str(score)
            
            lives = myfont.render("Lives: " + str_lives, False, (153, 0, 153))
            score_total = myfont.render("Score: " + str_score, False, (153, 0, 153))
            
            screen.blit(lives,(0,20))
            screen.blit(score_total,(0,80))
            
            
            # Draws boss life bar at the bottom of the screen 
            pygame.draw.rect(screen, BLACK ,(50, 800, 800, 50))
            pygame.draw.rect(screen, GREEN, (50, 800, (8*(boss_life)), 50))
            
            
            if boss_life == 0:
                eng.DrawStaticBackground(screen, WIDTH, HEIGHT, victory1_img)
                pygame.display.flip()
                pygame.time.wait(5000) 
                eng.DrawStaticBackground(screen, WIDTH, HEIGHT, victory2_img)
                pygame.display.flip()
                pygame.time.wait(5000)
                return False
                

        # If the game is paused the instructions are shown on screen
        elif state == pause:
            screen.blit(cheatsheet_img, ((WIDTH/2 - 400),(HEIGHT/2 - 300)))
       
    
        # Add to frame count for the timer
        clock.tick(FRAMERATE)
        pygame.display.flip()
    
    
    
    
