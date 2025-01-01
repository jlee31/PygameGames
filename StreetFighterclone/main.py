from settings import *
from fighter import Fighter
from os.path import join
import pygame

# Initialize Game
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
frames = 60
pygame.display.set_caption("Magestic Street Brawling")
running = True
bgImage = pygame.image.load(join('assets', 'images', 'background', 'background.jpg')).convert_alpha()
bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight))

introCount = 3
lastCountUpdate = pygame.time.get_ticks()
score = [0,0] # [p1, p2]
roundOver = False
roundOverCooldown = 2000
victory = pygame.image.load(join('assets', 'images', 'icons', 'victory.png')).convert_alpha()

bgMusic = pygame.mixer.Sound(join('assets', 'audio', 'music.mp3'))
bgMusic.set_volume(0.5)
bgMusic.play(loops=-1)

swordSound = pygame.mixer.Sound(join('assets', 'audio', 'sword.wav'))
swordSound.set_volume(0.5)
magicSound = pygame.mixer.Sound(join('assets', 'audio', 'magic.wav'))
swordSound.set_volume(0.5)

warriorSize = 162
warriorScale = 4
warriorOffset = [72, 56]
warriorData = [warriorSize, warriorScale, warriorOffset]
wizardSize = 250
wizardScale = 3
wizardOffset = [112, 107]
wizardData = [wizardSize, wizardScale, wizardOffset]

warriorSheet = pygame.image.load(join('assets', 'images', 'warrior', 'Sprites', 'warrior.png')).convert_alpha()
warriorFrames = [10, 8, 1, 7, 7, 3, 7]
wizardSheet = pygame.image.load(join('assets', 'images', 'wizard/Sprites', 'wizard.png')).convert_alpha()
wizardFrames = [8, 8, 1, 8, 8, 3, 7]

# Initialize Other Characters
fighterA = Fighter(1,200,430, False, warriorData, warriorSheet, warriorFrames, swordSound)
fighterB = Fighter(2,700,430, True, wizardData, wizardSheet, wizardFrames, magicSound)

# Game Functions
def drawBg():
    screen.blit(bgImage, (0,0))

def drawHealthBar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, (255,255,255), (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, (255,0,0), (x,y,400,30))
    pygame.draw.rect(screen, (0,128,0), (x,y,400 * ratio,30))
    
countFont = pygame.font.Font(join('assets', 'fonts', 'turok.ttf'), 100)
scoreFont = pygame.font.Font(join('assets', 'fonts', 'turok.ttf'), 30)

# Drawing Text
def drawText(text, font, color, x,y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

# Game Loop
while running:
    clock.tick(frames)
    # Event Loops
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    drawBg()
    drawHealthBar(fighterA.health, 20, 20)
    drawHealthBar(fighterB.health, 580, 20)
    drawText("P1: " + str(score[0]), scoreFont, (255,0,0), 20,60)
    drawText("P2: " + str(score[1]), scoreFont, (255,0,0), 580,60)

    # movement
    if introCount <= 0:
        fighterA.move(screen, fighterB, roundOver)
        fighterB.move(screen, fighterA, roundOver)
    else:
        drawText(str(introCount), countFont, (255,0,0), screenWidth/2, screenHeight/2)
        if (pygame.time.get_ticks() - lastCountUpdate) >= 1000:
            introCount -= 1
            lastCountUpdate = pygame.time.get_ticks()

    fighterA.update()
    fighterB.update()
    
    # Round Over
    if roundOver == False:
        if fighterA.alive == False:
            score[1] += 1
            roundOver = True
            roundOverTime = pygame.time.get_ticks()
        elif fighterB.alive == False:
            score[0] += 1
            roundOver = True
            roundOverTime = pygame.time.get_ticks()
    else: 
        screen.blit(victory, (360, 150))
        if pygame.time.get_ticks() - roundOverTime > roundOverCooldown:
            roundOver = False
            introCount = 3
            fighterA = Fighter(1,200,430, False, warriorData, warriorSheet, warriorFrames, swordSound)
            fighterB = Fighter(2,700,430, True, wizardData, wizardSheet, wizardFrames, magicSound)


    # Update
    fighterA.draw(screen)
    fighterB.draw(screen)
    
    pygame.display.flip()

pygame.quit()