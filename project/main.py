import pygame
import random
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800,600))

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./assets/images/ufo.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('./assets/images/background.jpg')
background = pygame.transform.scale(background,(800,600))
mixer.music.load('./assets/sounds/background.wav')
mixer.music.play(-1)

# player image and init
playerImg = pygame.image.load('./assets/images/spaceship.png')
playerImg = pygame.transform.scale(playerImg,(64,64))
playerX = 368
playerY = 500
playerX_change = 0

# score init
player_score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# enemy
enemyImg = pygame.image.load('./assets/images/alien.png')
enemyImg = pygame.transform.scale(enemyImg,(64,64))
enemyX = random.randint(0,736)
enemyY = 20
enemyX_change = 0.2
enemyY_change = 50

# bullet
bulletImg = pygame.image.load('./assets/images/bullet.png')
bulletImg = pygame.transform.scale(bulletImg,(64,64))
bulletImg = pygame.transform.rotate(bulletImg, 90)
bulletState = 'ready'
bulletX = 368
bulletY = 480+64
bulletX_change = 0
bulletY_change = 1


def player(x,y):
    screen.blit(playerImg,(x,y))
def displayScore(x,y):
    score = font.render("Score : "+str(player_score), True, (255,255,255))
    screen.blit(score,(x,y))
def enemy(x,y):
    screen.blit(enemyImg,(x,y))
def fire_bullet(x,y):
    global bulletState
    bulletState = 'fire'
    global bulletX
    bulletX = x
    screen.blit(bulletImg,(x,y-32))
def initialize():
    global playerX,playerY,playerX_change
    playerX = 368
    playerY = 500
    playerX_change = 0
    global enemyX,enemyY,enemyX_change,enemyY_change
    enemyX = random.randint(0,736)
    enemyY = 20
    enemyX_change = 0.2
    enemyY_change = 50
    global player_score,bulletState,bulletX,bulletY
    player_score = 0
    bulletState = 'ready'
    bulletX = 368
    bulletY = 480+64
    global font
    font = pygame.font.Font('freesansbold.ttf',32)
    mixer.music.play()


# game loop
running = True
while running:
    screen.fill((0,255,0))
    screen.blit(background,(0,0))
    pygame.draw.line(screen, (255,255,255), (0, 484), (800, 484), 3)
    displayScore(textX,textY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.25
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.25
            if event.key == pygame.K_SPACE:
                if(bulletState == 'ready'):
                    fire_bullet(playerX,playerY+64)
                    bulletSound = mixer.Sound('./assets/sounds/fire.wav')
                    bulletSound.play()    
        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change
    enemyX += enemyX_change 

    if(playerX<0):
        playerX = 0
    elif(playerX>736):
        playerX = 736
    if(enemyX>736 or enemyX<0):
        enemyX_change = -enemyX_change    
        enemyY += enemyY_change
    if bulletState == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    # collision
    bulletRect = pygame.Rect(bulletX+24,bulletY-24,16,16)  
    enemyRect = pygame.Rect(enemyX,enemyY,64,64)  
    # pygame.draw.rect(screen,(0,255,0),bulletRect)    
    # pygame.draw.rect(screen,(0,255,0),enemyRect)    
    if pygame.Rect.colliderect(enemyRect,bulletRect):
        explosionSound = mixer.Sound('./assets/sounds/explosion.wav')
        explosionSound.play()
        player_score += 10   
        bulletY = 480+64
        # respawn enemy
        bulletState = 'ready'
        enemyX = random.randint(0,736)
        enemyY = 20
        if enemyX_change > 0:
            enemyX_change += 0.1
        else:
            enemyX_change -= 0.1

    if bulletY < 20: 
        bulletY = 480+64
        bulletState = 'ready'

    player(playerX,playerY)
    enemy(enemyX,enemyY)

    # if enemy win 
    if(enemyY>=484-64):
        font = pygame.font.Font('freesansbold.ttf',16)
        alert = font.render("Press 'enter' to re-play", True, (255,255,255))
        screen.blit(alert,(300,280))
        alert = font.render("Press 'esc' to exit", True, (255,255,255))
        screen.blit(alert,(320,300))
        font = pygame.font.Font('freesansbold.ttf',64)
        gameOverText = font.render("Game Over!", True, (255,255,255))
        screen.blit(gameOverText,(200,200))
        pygame.display.update()         
        print("wait")
        mixer.music.stop()
        flag = 1
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quit")
                    flag = 0
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        initialize()
                        flag = 0
                    elif event.key == pygame.K_ESCAPE:
                        print("quit")
                        flag = 0
                        running = False  

    pygame.display.update()         