import pygame
import random
import math
from pygame import mixer
# initialize pygame
pygame.init()

# create game window
screen = pygame.display.set_mode((800, 600))  # screen creation (width, height)

# title and icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# background image
background = pygame.image.load("bgimg.png")

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# player
playerimg = pygame.image.load("player.png")
playerX = 340
playerY = 480
playerX_change = 0

textX = 10
textY = 10

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# Ready- you can't see the bullet on screen
# fire - the bullet is currently moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('fonty.otf', 30) #(fontname, size)


# display score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255)) #(string,true,rgb value)
    screen.blit(score,(x,y)) # displaying score

#game over text
game_over = pygame.font.Font('fonty.otf', 80)  # (fontname, size)
def game_over_text():
    over_text=game_over.render("GAME OVER ",True,(255,255,255))
    screen.blit(over_text,(200,230))


# plotting player
def player(x, y):
    screen.blit(playerimg, (x, y))  # draw player on  surface


# plotting enemy
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))  # draw enemy on surface


# firing bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # giving rgb values to fill the screen
    screen.fill((255, 255, 255))
    # background image
    screen.blit(background, (0, 0))
    # event means when we want some user action to produce changes on screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # checking if a key is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # right arrow key
                playerX_change = 5
            if event.key == pygame.K_LEFT:  # left arrow key
                playerX_change = -5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")        
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)
            # moving up and down
            # if event.key == pygame.K_DOWN:#down arrow key
            #     playerY_change = 0.3
            # if event.key == pygame.K_UP:#up arrow key
            #     playerY_change = -0.3
        # checks if a key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #     playerY_change = 0

    playerX += playerX_change
    # checking spaceship boundaries to stop it from going out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i]>450:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    # updating the display/game window
    pygame.display.update()
