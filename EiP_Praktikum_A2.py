#EiP Praktikum A2

import pygame
from sys import exit
import random

#Bildschirmgröße und Spielkoordinaten festlegen
width = 800
height = 400
gwidth = 20
gheight = 10

#pygame Engine starten und Hintergrund weiß machen
pygame.init()
screen = pygame.display.set_mode((width,height))
screen.fill("White")
pygame.display.set_caption("Aufgabe 2")
clock = pygame.time.Clock()

#3 Surface Typen für den Spieler, die Wände und die Löcher in den Wänden
player = pygame.Surface((width/gwidth,height/gheight))
player.fill("Red")
wall = pygame.Surface((width/gwidth, height))
wall.fill("Black")
hole = pygame.Surface((width/gwidth, (height/gheight)*2))
hole.fill("White")

#Hauptfunktion, die die Positionen unserer Elemente angibt
def display_state(walls: list[bool], holes: list[int], player_pos: int):
    for i in range(len(walls)):
        if walls[i]:
            screen.blit(wall, (i * (width/gwidth), 0))
        for i in range(len(holes)):
            screen.blit(hole, (i * (width/gwidth), holes[i] * (height/gheight)))
    screen.blit(player, ((0, player_pos * (height/gheight))))
    return

#Startwerte für Spieler, Wände und Löcher
player_start = 9
walls_start = [False]*(gwidth-1) + [True]
holes_start = [0]*(gwidth-1) +  [random.randint(0,8)]
#Startwerte für die Counter die Schnelligkeit und Frequenz von Wänden steuern
wall_movement_counter = 0
wall_counter = 0

#Game-Loop
while True:
    #Möglichkeit das Spiel zu schließen erstellen und Pfeiltaste nach Oben/Unten mit Bewegung des Spieler-Quadrats belegen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_start -= 1
            if event.key == pygame.K_DOWN:
                player_start += 1
    #In jeder Iteration wird der Counter hochgesetzt -> alle so und so viele Iterationen wird die Wand bewegt
    wall_movement_counter += 1
    if wall_movement_counter >= 10:  # Je höher die Zahl desto langsamer die Wände
        wall_movement_counter = 0
        wall_counter += 1
        walls_start = walls_start[1:] + [False] 
        holes_start = holes_start[1:] + [0]
    
    #Bestimmt wie oft neue Wände gesetzt werden
    if wall_counter >= 10:
        wall_counter = 0
        walls_start = walls_start[1:] + [True]
        holes_start = holes_start[1:] + [random.randint(0,8)]   #Erstellt ein zufälliges Loch für jede neue Wand die gesetzt wird
    
    #Damit Spieler nicht außerhalb des Spielfeldes gelangen kann
    if player_start < 0:
        player_start = 0
    if player_start > 9:
        player_start = 9
    clock.tick(60)
    display_state(walls_start, holes_start, player_start)
    pygame.display.update()
    #Resettet den Bildschirm nach jedem Frame
    screen.fill("White")