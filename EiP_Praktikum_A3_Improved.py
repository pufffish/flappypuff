#EiP Praktikum A3 Improved

import pygame
from sys import exit
import random

#Bildschirmgröße und Spielpixel festlegen
width = 800
height = 400
gwidth = 20
gheight = 10


#pygame Engine starten und Hintergrund weiß machen
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Aufgabe 2")
clock = pygame.time.Clock()

#3 Surface Typen für den Spieler, die Wände und die Löcher in den Wänden
player = pygame.Surface((width/gwidth,height/gheight))
player.fill("Red")
wall = pygame.Surface((width/gwidth, height))
wall.fill("Black")
hole = pygame.Surface((width/gwidth, (height/gheight)*3))
hole.fill("White")

#Hauptfunktion, die die Positionen unserer Elemente angibt
def display_state(wall1_pos: int, wall2_pos:int, hole1_pos: int, hole2_pos: int, player_pos: int):
    screen.blit(wall, (wall1_pos - (width/gwidth)/2, 0))
    screen.blit(wall, (wall2_pos - (width/gwidth)/2, 0))
    screen.blit(hole, (wall1_pos - (width/gwidth)/2, hole1_pos))
    screen.blit(hole, (wall2_pos - (width/gwidth)/2, hole2_pos))
    screen.blit(player, (0, player_pos - (height/gheight)/2))
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_speed = 0
                player_speed -= (height/gheight)/4
    
    wall1 -= wall_speed
    wall2 -= wall_speed
    if wall1 <= -(width/gwidth):
        wall1 = center(20)
        hole1 = center(random.randint(0,7))
    if wall2 <= -(width/gwidth):
        wall2 = center(20)
        hole2 = center(random.randint(0,7))

    #Spielerposition verändert sich um Geschwindigkeit und die Geschwindigkeit wird geupdated
    player_center += calc_speed(player_speed, gravity)
    player_speed = calc_speed(player_speed, gravity)
    
    #Damit Spieler nicht außerhalb des Spielfeldes gelangen kann
    if player_center < center(0):
        player_center = center(0)
    if player_center > center(9):
        player_center = center(9)
    clock.tick(60)
    display_state(wall1, wall2, hole1, hole2, player_center)
    pygame.display.update()
    #Resettet den Bildschirm nach jedem Frame
    screen.fill("White")