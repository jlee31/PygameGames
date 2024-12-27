import pygame
from os.path import join # this is related to importing images 
from random import randint, uniform
# General Setup
pygame.init()
screenWidth, screenHeight = 1280, 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Space Shooter Clone')
running = True
clock = pygame.time.Clock()
font = pygame.font.Font("images/Oxanium-Bold.ttf", 50)

# sounds
laserSound = pygame.mixer.Sound("audio/laser.wav")
laserSound.set_volume(0.05)
BGMusic = pygame.mixer.Sound("audio/game_music.wav")
BGMusic.set_volume(0.05)
BGMusic.play()
BGMusic.play(loops= -1)
explosion = pygame.mixer.Sound("audio/explosion.wav")

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_frect(center = (screenWidth/2, screenHeight/2))
        self.direction = pygame.Vector2()
        self.speed = 400

        # cooldown part
        self.canShoot = True
        self.laserTime = 0
        self.cooldown = 1000

        # masks
        self.mask = pygame.mask.from_surface(self.image)
        
    def laserTimer(self):
        if not self.canShoot:
            currentTime = pygame.time.get_ticks() # gets the time since the pygame.init()
            if currentTime - self.laserTime >= self.cooldown:
                self.canShoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recentKeys = pygame.key.get_just_pressed()
        if recentKeys[pygame.K_SPACE] and self.canShoot:
            Laser(laserSurf, self.rect.midtop, (allSprites, laserSprites))
            self.canShoot = False
            self.laserTime = pygame.time.get_ticks()
            laserSound.play()
        self.laserTimer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,screenWidth), randint(0,screenHeight)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
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

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frameIndex = 0
        self.image = frames[self.frameIndex]
        self.rect = self.image.get_frect(center = pos)
        explosion.play()
        
    def update(self, dt):
        self.frameIndex += 20 * dt
        if self.frameIndex <= len(self.frames):
            self.image = self.frames[int(self.frameIndex % len(self.frames))]
        else:
            self.kill()
        
def collisions(): 
    global running
    collisionsSprites = pygame.sprite.spritecollide(plane, meteorSprites, True, pygame.sprite.collide_mask)
    if collisionsSprites:
        running = False
     
    for laser in laserSprites:
        collididSprites = pygame.sprite.spritecollide(laser, meteorSprites, True)
        if collididSprites:
            laser.kill()
            AnimatedExplosion(explosionFrames, laser.rect.midtop, allSprites)
            

def score():
    currentTime = pygame.time.get_ticks()
    textSurface = font.render(str(int (currentTime // 1000)), True, (255,255,255))
    textRect = textSurface.get_frect(midbottom = (screenWidth/2, screenHeight - 50))
    padding = 10
    screen.blit(textSurface,textRect)
    pygame.draw.rect(screen, 'white', textRect.inflate(padding * 2, padding * 2).move(0,-10), 5, 10)

# Sprites
allSprites  = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()

starSurf = pygame.image.load("images/star.png").convert_alpha()
for i in range(20):
    Star(allSprites, starSurf)
plane = Player(allSprites)

meteorSurf = pygame.image.load("images/meteor.png").convert_alpha()
meteorRect = meteorSurf.get_frect(center = (screenWidth/2, screenHeight/2))

laserSurf = pygame.image.load("images/laser.png")
laserRect = laserSurf.get_frect(bottomleft = (20, screenHeight - 20))

explosionFrames = []
for i in range(21):
    explosionFrames.append(pygame.image.load(f'images/explosion/{i}.png').convert_alpha())
# timer
meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500) 

while running:
    # Random Stuff
    dt = clock.tick() / 1000
    screen.fill('#1f4277') #background
    

    # Game Loop   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteorEvent:
            x, y = randint (0, screenWidth), randint(-200, -100)
            Meteor(meteorSurf, (x,y), (allSprites, meteorSprites))

    allSprites.update(dt)
    collisions()
    allSprites.draw(screen)

    score()
    pygame.display.flip() # loads the image
pygame.quit()
