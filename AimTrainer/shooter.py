import pygame, sys, random
from pygame.locals import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture):
        super().__init__()
        self.image = pygame.image.load(picture)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("SupportFiles/laser-gun-81720.mp3")
    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(crosshair, targetGroup, True)
    def update(self):
        self.rect.center = pygame.mouse.get_pos() # X and Y position of the mouse

def background_set(screen: pygame.Surface, image: pygame.Surface):
    screen_width, screen_height = screen.get_size()
    image_width, image_height = image.get_size()

    # Calculate how many tiles we need to draw in x and y axes
    tiles_x = screen_width // image_width + 1
    tiles_y = screen_height // image_height + 1

    # Draw the tiles
    for y in range(tiles_y):
        for x in range(tiles_x):
            screen.blit(image, (x * image_width, y * image_height))

class Target(pygame.sprite.Sprite):
    def __init__(self, picture, posX, posY):
        super().__init__()
        self.image = pygame.image.load(picture)
        self.rect = self.image.get_rect()
        self.rect.center = [posX, posY]

# Initiation
pygame.init()
clock = pygame.time.Clock()

# Variables
screenWidth = 1920
screenHeight = 1080
window = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Learning Sprites')

background = pygame.image.load("SupportFiles/bg_wood.png")
pygame.transform.scale(background, (100,100))
# Creating an Object from the class
crosshair = Crosshair("SupportFiles/crosshair.png")
# Creating a group that holds the sprites which can then be projected
crosshairGroup = pygame.sprite.Group() # initialized the group
crosshairGroup.add(crosshair) # added the group
pygame.mouse.set_visible(False)

# Targets
targetGroup = pygame.sprite.Group()
for target in range(25):
    new_target = Target("SupportFiles/duck_target_yellow.png", random.randrange(0,screenWidth), random.randrange(0,screenHeight))
    targetGroup.add(new_target) # Now targetGroup has 25 different targets
# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

    pygame.display.flip()
    background_set(window, background)
    targetGroup.draw(window)
    crosshairGroup.draw(window)
    crosshairGroup.update()
     
    clock.tick(60)
    
