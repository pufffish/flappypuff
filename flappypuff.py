import pygame, random, os
from sys import exit

# initiate mixer
pygame.mixer.init()

#create vars for the contents of /ressources
dir_ressource = './ressources/'
files = os.listdir(dir_ressource)
for file in files:
    if file.endswith(".png"):
        globals()[str(file).removesuffix('.png')] = pygame.image.load(dir_ressource+file)
    if file.endswith(".mp3"):
        globals()[str(file).removesuffix('.mp3')] = dir_ressource + file
    if file.endswith(".wav"):
        globals()[str(file).removesuffix('.wav')] = pygame.mixer.Sound(dir_ressource+file)

# play menu music in an endless loop
pygame.mixer.music.load(menuMusic)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

#flappy status quo
flappy = flappyd

#set screen size
width = 800
height = 400
gwidth = 20
gheight = 10

#start pygame engine and make background white
pygame.init()
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
pygame.display.set_caption("FlappyPuff")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_active = True

#create 3 surfaces for the player, the walls and the holes in the walls
player = pygame.Surface((width/gwidth,height/gheight))
player.fill("Red")
wall = pygame.Surface((width/gwidth, height))
wall.fill("Black")
hole = pygame.Surface((width/gwidth, (height/gheight)*3))
hole.fill("White")
Game_Over = gameover
Game_Over2 = font.render("Press Enter to Restart", True, "Black")
score = 0

#central function that sets the positions of the elements
def display_state(wall1_pos: int, wall2_pos:int, hole1_pos: int, hole2_pos: int, player_pos: int, points: int, flappy: any):
    global game_active

    #use rect_obj
    player_rect = pygame.Rect(10, player_pos - (height/gheight)/2, flappy.get_width(), flappy.get_height())
    wall1_rect = pygame.Rect(wall1_pos - (width/gwidth)/2, hole1_pos-375, pipe.get_width(), pipe.get_height())
    wall2_rect = pygame.Rect(wall2_pos - (width/gwidth)/2, hole2_pos, pipe.get_width(), pipe.get_height())
    hole1_rect = pygame.Rect(wall1_pos - (width/gwidth)/2, hole1_pos, hole.get_width(), hole.get_height())
    hole2_rect = pygame.Rect(wall2_pos - (width/gwidth)/2, hole2_pos, hole.get_width(), hole.get_height())

    #draw the objects
    screen.blit(bg, (0, 0))
    screen.blit(pipe, wall1_rect.topleft)
    screen.blit(pipe, wall2_rect.topleft)
    print(flappy)
    if flappy == flappyd:
        flappy = pygame.transform.rotate(flappy, -345)
    elif flappy == flappyu:
        flappy = pygame.transform.rotate(flappy, -380)
    else:
        flappy = pygame.transform.rotate(flappy, -360)
    
    screen.blit(flappy, player_rect.topleft)
    screen.blit(base, (0, 382))

    #check collision if not score up
    if wall1_rect.colliderect(player_rect):
        if not hole1_rect.contains(player_rect):
            hit.play()
            game_active = False
    elif wall2_rect.colliderect(player_rect):
        if not hole2_rect.contains(player_rect):
            hit.play()
            game_active = False
    else:
        x = points//10
        points -= x*10
        i = points//1
        screen.blit(globals()[f'num{x}'],(364, 25))
        screen.blit(globals()[f'num{i}'],(389, 25))
        
# function calculate center of screen
def center(game_y:int):
    screen_y = game_y*(height/gheight)
    middle = screen_y + ((height/gheight)/2)
    return middle

# function calculate speed
def calc_speed(speed_old, acceleration):
    speed_new = speed_old + acceleration
    return speed_new

#start values for the player, walls and holes
player_center = center(9)
wall1 = center(9)
wall2 = center(39)
hole1 = center(random.randint(0,7))
hole2 = center(random.randint(0,7))
holes_start = [0]*(gwidth-1) +  [random.randint(0,7)] 

#start values for the counter and the speed and frequency that draws walls
wall_speed = (height/gheight)/14
player_speed = 0
gravity = (height/gheight)/70
speedUp = 0

#game loop
while True:
    #check any events that can occur if you do smth with the windows or keyboard
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
                player_center = center(9)
                flappy = flappym
                game_active = True
                score = 0

    #change the values of the walls dynamicly
    if game_active:
        wall1 -= wall_speed + speedUp
        wall2 -= wall_speed + speedUp
        if wall1 <= -(width/gwidth):
            wall1 = center(20)
            hole1 = center(5)
            score += 1
            speedUp += 0.05 # accelerate wall speed
        if wall2 <= -(width/gwidth):
            wall2 = center(20)
            hole2 = center(random.randint(0,7))
            score += 1
            speedUp += 0.05 # accelerate wall speed

        #player position changes an the speed of the player also changes
        player_center += calc_speed(player_speed, gravity)
        player_speed = calc_speed(player_speed, gravity)

        #check that the player is not outbound
        if player_center < center(0):
            player_center = center(0)
        elif player_center > center(9):
            player_center = center(9)
        elif player_speed < 0:
            flappy = flappyd
        elif player_speed > 0:
            flappy = flappyu
        clock.tick(60)

        #update the screen
        display_state(wall1, wall2, hole1, hole2, player_center, score, flappy)

    #display game over
    else:
        screen.blit(Game_Over,(304,70))
        screen.blit(Game_Over2,(200, 200))
        score_go = score
        x = score_go//10
        screen.blit(globals()[f'num{x}'],(364, 25))
        score_go -= x*10
        i = score_go//1
        screen.blit(globals()[f'num{i}'],(389, 25))
        
   
    pygame.display.update()
    