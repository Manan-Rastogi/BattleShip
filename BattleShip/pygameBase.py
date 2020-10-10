import pygame
import random
from PIL import Image
import math
from pygame import mixer


# initializing pygame
pygame.init()

# creating screen
screen = pygame.display.set_mode((800,600))                    # (w,h)

# Changing title and icon : display                            https://www.flaticon.com/
pygame.display.set_caption("BattleShip")
icon = pygame.image.load('ss.png')
pygame.display.set_icon(icon)

# SpaceShip
spaceship = pygame.image.load('SpShip.png')
spaceshipX = 370
spaceshipY = 480
changeX = 0
changeY = 0

# Score
score = 0
totalKill = 0
font = pygame.font.Font('freesansbold.ttf',32)

textx = 10
texty = 10

def show_score(x,y):
    points = totalKill*5 + score
    tot_score = font.render("Score : " + str(points), True, (0,255,0))
    screen.blit(tot_score,(x,y))

def showKills(x,y):
    kills = font.render("Kills : " + str(totalKill), True, (255,0,0))
    screen.blit(kills,(x,y))


def gameplay(x,y):
    screen.blit(spaceship,(x,y))

# Missile
missile = pygame.image.load('bullet.png')
missilex = 370
missiley = 480
mchangex = 0
mchangey = 10
m_state = "ready"

def shoot(x,y):
    global m_state
    m_state = "fire"
    screen.blit(missile,(x+16,y+10))

def is_Collision(ex,ey,mx,my):
    dist = math.sqrt(math.pow(ex-mx,2) + math.pow(ey-my,2))
    if dist <= 60:
        return True
    else:
        return False


#Enemy - Alien Monster
alien = pygame.image.load('alien.png')
alienx = random.randint(0,672)
alieny = 40
achangex = 0
achangey = 0

def alienspawn(x,y):
    screen.blit(alien,(x,y))

# Background

# img = Image.open('155.jpg')
# img = img.resize((800,600))
# img.save('background2.jpg')

background = pygame.image.load('background2.jpg')

# Music
pygame.mixer.init()
mixer.music.load('backgroundMusic.wav')
mixer.music.play(-1)                                      # -1 to play in loop

# GameOver
font_over = pygame.font.Font('freesansbold.ttf',64)
def game_over(x,y):
    over = font_over.render("GAME OVER!!!", True, (255,0,0))
    screen.blit(over, (x,y))


# Permanent entities will be stored here...
# screen will remain open till running = true

running = True
while running:

    # setting screen background
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check for key press event       
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changeX = -(totalKill/2 + 3)
            if event.key == pygame.K_RIGHT:
                changeX = (totalKill/2 + 3)
            if event.key == pygame.K_SPACE:
                if m_state is "ready" and spaceshipY < 1000:
                    launch = mixer.Sound('launch.wav')
                    launch.play()
                    missilex = spaceshipX
                    shoot(missilex,missiley)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                changeX = 0
    
    # game

    spaceshipX += changeX                                   #Spaceship movement
    
    if spaceshipX <= 0:
        spaceshipX = 600
    elif spaceshipX >=736:
        spaceshipX = 0

    
    if missiley <= 0 :                                     # Missile Movement
        missiley = 480
        m_state = "ready"



    if m_state is "fire":
        shoot(missilex,missiley)
        missiley -= mchangey    
    

    # Collision
    collision = is_Collision(alienx,alieny ,missilex,missiley)
    if collision:
        missiley = 480
        m_state = "ready"
        score += 1
        explosion = mixer.Sound('explosion.wav')
        explosion.play() 
        # print(score)
        if score is 5:
            respawn = mixer.Sound('respawn.wav')
            respawn.play()
            alienx = random.randint(0,672)
            alieny = 40
            score = 0
            totalKill += 1
    
    
    
    
    achangex = totalKill/1.5 + 1
    if(alienx <= 0 or alienx >= 672) and spaceshipY < 1000:                  #Alien movement
        alienx = random.randint(230,572)
        alieny += (totalKill*0.5) + 10

    if spaceshipY<1000:    
        if alienx >= 380:
            alienx += achangex
        else:
            alienx -= achangex
    
    
    
    


    
    gameplay(spaceshipX,spaceshipY)
    # shoot(missilex,missiley)
    alienspawn(alienx, alieny)

    show_score(textx,texty)
    showKills(textx+600,texty)


    # Game Over
    if alieny > 380:
        game_over(150,275)
        spaceshipY = 10000
        



    pygame.display.update()                     # add this after every update

