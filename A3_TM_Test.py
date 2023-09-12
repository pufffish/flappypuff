#EiP Praktikum A4, Flappy Bird working

import pygame
import random
import os
from sys import exit

# initiate mixer
pygame.mixer.init()

#create vars for the contents of /ressources
mp3_music = {}
dir_ressource = './ressources/'
files = os.listdir(dir_ressource)
for file in files:
    if file.endswith(".png"):
        globals()[str(file).removesuffix('.png')] = pygame.image.load(dir_ressource+file)
    else:
        mp3_music[file.removesuffix('.mp3')] = dir_ressource + file

# play menu music in an endless loop
pygame.mixer.music.load(mp3_music["menuMusic"])
pygame.mixer.music.play(-1)


#flappy status quo
flappy = flappyd

#Bildschirmgröße und Spielpixel festlegen
width = 800
height = 400
gwidth = 20
gheight = 10


#pygame Engine starten und Hintergrund weiß machen
pygame.init()
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
pygame.display.set_caption("FlappyPuff")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_active = True

#3 Surface Typen für den Spieler, die Wände und die Löcher in den Wänden
player = pygame.Surface((width/gwidth,height/gheight))
player.fill("Red")
wall = pygame.Surface((width/gwidth, height))
wall.fill("Black")
hole = pygame.Surface((width/gwidth, (height/gheight)*3))
hole.fill("White")
Game_Over = gameover #font.render("Oh, You Died!", True, "Red")
Game_Over2 = font.render("Press Enter to Restart", True, "Red")
score = 0


#Hauptfunktion, die die Positionen unserer Elemente angibt
def display_state(wall1_pos: int, wall2_pos:int, hole1_pos: int, hole2_pos: int, player_pos: int, points: int, flappy: any):
    global game_active
    screen.blit(bg, (0, 0))
    screen.blit(pipe, (wall1_pos - (width/gwidth)/2, 0))
    screen.blit(wall, (wall2_pos - (width/gwidth)/2, 0))
    screen.blit(hole, (wall1_pos - (width/gwidth)/2, hole1_pos))
    screen.blit(hole, (wall2_pos - (width/gwidth)/2, hole2_pos))
    screen.blit(flappy, (10, player_pos - (height/gheight)/2))
    if score > 9:
        x = points//10
        i = points//1
        score_board = font.render("Score:", True, "Green")
        screen.blit(score_board,(630, 25))
        screen.blit(globals()[f'num{x}'],(750, 25))
        screen.blit(globals()[f'num{i}'],(780, 25))
    else:
        i = points//1
        score_board = font.render("Score:", True, "Green")
        screen.blit(score_board,(630, 25))
        screen.blit(globals()[f'num{i}'],(750, 25))
    if (wall1_pos - (width/gwidth)/2) <= (width/gwidth):
        if player_pos < (hole1_pos + (height/gheight)/2) or player_pos > (hole1_pos + 3*(height/gheight) - ((height/gheight)/2)):
            game_active = False
    if (wall2_pos - (width/gwidth)/2) <= (width/gwidth):
        if player_pos < (hole2_pos + (height/gheight)/2) or player_pos > (hole2_pos + 3*(height/gheight) - ((height/gheight)/2)):
            game_active = False
    return

#Funktion die Mittelpunkt in Bildschirmkoordinaten berechnet
def center(game_y:int):
    screen_y = game_y*(height/gheight)
    middle = screen_y + ((height/gheight)/2)
    return middle

#Funktion die Geschwindigkeit berechnet
def calc_speed(speed_old, acceleration):
    speed_new = speed_old + acceleration
    return speed_new


#Startwerte für Spieler, Wände und Löcher
player_center = center(9)
wall1 = center(19)
wall2 = center(29)
hole1 = center(random.randint(0,7))
hole2 = center(random.randint(0,7))
holes_start = [0]*(gwidth-1) +  [random.randint(0,7)]

#Startwerte für die Counter die Schnelligkeit und Frequenz von Wänden steuern
wall_speed = (height/gheight)/14
player_speed = 0
gravity = (height/gheight)/70

#Game-Loop
while True:
    #Möglichkeit das Spiel zu schließen und Leertaste mit "Springen" belegen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif  event.type == pygame.VIDEORESIZE:
            bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
            flappym = pygame.transform.scale(flappym, (34*(screen.get_width()/width), 24*(screen.get_height()/height)))
            flappyd = pygame.transform.scale(flappyd, (34*(screen.get_width()/width), 24*(screen.get_height()/height)))
            flappyu = pygame.transform.scale(flappyu, (34*(screen.get_width()/width), 24*(screen.get_height()/height)))
            pipe = pygame.transform.scale(pipe, (34*(screen.get_width()/width), 24*(screen.get_height()/height)))
            pygame.display.update()
        elif game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_speed = 0
                    player_speed -= (height/gheight)/5
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                wall1 = center(19)
                wall2 = center(29)
                score = 0
                player_center = center(9)
                flappy = flappym
                game_active = True
        
    
    #Game-Screen
    if game_active:
        wall1 -= wall_speed
        wall2 -= wall_speed
        if wall1 <= -(width/gwidth):
            wall1 = center(20)
            hole1 = center(random.randint(0,7))
            score += 1
        if wall2 <= -(width/gwidth):
            wall2 = center(20)
            hole2 = center(random.randint(0,7))
            score += 1

        #Spielerposition verändert sich um Geschwindigkeit und die Geschwindigkeit wird geupdated
        player_center += calc_speed(player_speed, gravity)
        player_speed = calc_speed(player_speed, gravity)

        #Damit Spieler nicht außerhalb des Spielfeldes gelangen kann
        if player_center < center(0):
            player_center = center(0)
        elif player_center > center(9):
            player_center = center(9)
        elif player_speed < 0:
            flappy = flappyd
        elif player_speed > 0:
            flappy = flappyu
        clock.tick(60)

        #Bildschirm wird geupdated
        display_state(wall1, wall2, hole1, hole2, player_center, score, flappy)

    #Game-over-Screen
    else:
        screen.fill("Blue")
        screen.blit(Game_Over,(275,50))
        screen.blit(Game_Over2,(200, 200))
        score_board = font.render(f"Score: {score}", True, "Green")
        screen.blit(score_board,(630, 25))
   
    pygame.display.update()
    #Resettet den Bildschirm nach jedem Frame
    screen.fill("White")