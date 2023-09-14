import pygame
import random
import os
from sys import exit

#create vars for the contents of /ressources

pygame.mixer.init()
dir_ressource = './ressources/'
files = os.listdir(dir_ressource)
for file in files:
    if file.endswith(".png"):
        globals()[str(file).removesuffix('.png')] = pygame.image.load(dir_ressource+file)
    if file.endswith(".mp3"):
        globals()[str(file).removesuffix('.mp3')] = dir_ressource + file
    if file.endswith(".wav"):
        globals()[str(file).removesuffix('.wav')] = pygame.mixer.Sound(dir_ressource+file)

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
Game_Over = gameover#font.render("Oh, You Died!", True, "Red")
Game_Over2 = font.render("Press Enter to Restart", True, "Red")
score = 0


#Hauptfunktion, die die Positionen unserer Elemente angibt
def display_state(wall1_pos: int, wall2_pos:int, hole1_pos: int, hole2_pos: int, player_pos: int, points: int, flappy: any):
    global game_active
    screen.blit(bg, (0, 0))
    screen.blit(wall1_top, (wall1_pos - (width/gwidth)/2,0))
    screen.blit(wall1_bottom, (wall1_pos - (width/gwidth)/2,hole1_pos + 3*(height/gheight)))
    screen.blit(wall2_top, (wall2_pos - (width/gwidth)/2,0))
    screen.blit(wall2_bottom, (wall2_pos - (width/gwidth)/2,hole2_pos + 3*(height/gheight)))
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
        if player_pos < (hole1_pos + (height/gheight)/2) or player_pos > (hole1_pos + 3*(height/gheight)):
            game_active = True
    if (wall2_pos - (width/gwidth)/2) <= (width/gwidth):
        if player_pos < (hole2_pos + (height/gheight)/2) or player_pos > (hole2_pos + 3*(height/gheight)):
            game_active = True
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
hole1 = center(random.randint(0,6))
hole2 = center(random.randint(0,6))


#Startwerte für die Counter die Schnelligkeit und Frequenz von Wänden steuern
wall1_top_resize = ((width/gwidth,hole1))
wall1_bottom_resize = ((width/gwidth),int(height - (hole1 + 3*(height/gheight))))
wall2_top_resize = ((width/gwidth,hole2))
wall2_bottom_resize = ((width/gwidth),int(height - (hole2 + 3*(height/gheight))))


wall_speed = (height/gheight)/14
player_speed = 0
gravity = (height/gheight)/70

wall1_top = pipe
wall1_top = pygame.transform.scale(wall1_top, wall1_top_resize)
wall1_top = pygame.transform.rotate(wall1_top, 180)
wall1_bottom = pipe
wall1_bottom = pygame.transform.scale(wall1_bottom, wall1_bottom_resize)
wall2_top = pipe
wall2_top = pygame.transform.scale(wall2_top, wall2_top_resize)
wall2_top = pygame.transform.rotate(wall2_top, 180)
wall2_bottom = pipe
wall2_bottom = pygame.transform.scale(wall2_bottom, wall2_bottom_resize)


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
            hole1 = center(random.randint(0,6))
            wall1_top_resize = ((width/gwidth,hole1))
            wall1_bottom_resize = ((width/gwidth),int(height - (hole1 + 3*(height/gheight))))
            wall1_top = pipe
            wall1_top = pygame.transform.scale(wall1_top, wall1_top_resize)
            wall1_top = pygame.transform.rotate(wall1_top, 180)
            wall1_bottom = pipe
            wall1_bottom = pygame.transform.scale(wall1_bottom, wall1_bottom_resize)
            score += 1
        if wall2 <= -(width/gwidth):
            wall2 = center(20)
            hole2 = center(random.randint(0,6))
            wall2_top_resize = ((width/gwidth,hole2))
            wall2_bottom_resize = ((width/gwidth),int(height - (hole2 + 3*(height/gheight))))
            wall2_top = pipe
            wall2_top = pygame.transform.scale(wall2_top, wall2_top_resize)
            wall2_top = pygame.transform.rotate(wall2_top, 180)
            wall2_bottom = pipe
            wall2_bottom = pygame.transform.scale(wall2_bottom, wall2_bottom_resize)
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
