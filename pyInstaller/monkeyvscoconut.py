import pygame
from random import randint, uniform

# General Setup
pygame.init()
screenWidth, screenHeight = 1280, 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Monkeys V.S Coconuts")
running = True
clock = pygame.time.Clock()
MONKEY = pygame.image.load("images/monkey 1.png")
MONKEY = pygame.transform.scale_by(MONKEY,2)
bg = pygame.image.load("images/voodoo_cactus_island.png")

# Sounds

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (screenWidth/2, screenHeight/2))
        self.direction = pygame.Vector2()
        self.speed = 400

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
    
class Coconut(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original = surf
        self.image = self.original
        self.rect = self.image.get_frect(center = pos)
        self.life = pygame.time.get_ticks()
        self.lifetime = 4000
        self.speed = randint(400,500)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
        self.rotationSpeed = randint(0,100)
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.life >= self.lifetime:
            self.kill()
        self.rotation += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.original, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Banana(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.life = pygame.time.get_ticks()
        self.lifetime = 4000
        self.speed = randint(300,600)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.life >= self.lifetime:
            self.kill()

# Initiating The Sprites
allSprites = pygame.sprite.Group()
monkey = Player(allSprites, MONKEY)
coconutSprites = pygame.sprite.Group()
bananaSprites = pygame.sprite.Group()

coconut = pygame.image.load("images/fluzzycoconut2.png")
coconutSurf = pygame.transform.scale_by(coconut, 0.1)
coconutRect = coconutSurf.get_frect(center = (screenWidth/2, screenHeight/2))

banana = pygame.image.load("images/fruit_banana.png")
bananaSurf = pygame.transform.scale_by(banana, 0.20)
bananaRect = bananaSurf.get_frect(center = (screenWidth/2, screenHeight/2))

# timer
coconutEvent = pygame.event.custom_type()
pygame.time.set_timer(coconutEvent, 500) 

bananaEvent = pygame.event.custom_type()
pygame.time.set_timer(bananaEvent, randint(3000,6000))

# Game Loop
while running:
    dt = clock.tick() / 1000
    screen.blit(bg, (0,-600))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == coconutEvent:
            x, y = randint (0, screenWidth), randint(-200, -100)
            Coconut(coconutSurf, (x,y), (allSprites, coconutSprites))
        if event.type == bananaEvent:
            a, b = randint (0, screenWidth), randint(-200, -100)
            Banana(bananaSurf, (a, b), (allSprites, bananaSprites))

    # RENDER YOUR GAME HERE
    allSprites.update(dt)
    allSprites.draw(screen)  

    pygame.display.flip()
pygame.quit()