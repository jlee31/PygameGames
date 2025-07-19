import pygame 
from settings import LAYERS
from settings import *
from random import randint, choice
from myTimer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name
class Water(Generic):

    def __init__(self, pos, frames, groups):
        

        # Animation setup
        self.frames = frames
        self.frameIndex = 0

        # Sprite setup
        super().__init__(pos, self.frames[self.frameIndex], groups, z = LAYERS['water']) 

    def animate(self, dt):
        self.frameIndex += 5 * dt;
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0;
        self.image = self.frames[int(self.frameIndex)]

    def update(self, dt):
        self.animate(dt)

class Wildflower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Tree(Generic):
    def __init__(self, pos, surf, groups, names, playerAdd):
        super().__init__(pos, surf, groups, z=LAYERS['main'])

        # tree attributes
        self.health = 5
        self.alive = True
        self.stumpSurface = pygame.image.load(f'../graphics/stumps/{"small" if names == "Small" else "large"}.png').convert_alpha()
        self.invulTimer = Timer(200)
        

        # apple
        self.appleSurf = pygame.image.load('../graphics/fruit/apple.png') 
        self.applePos = APPLE_POS[names]
        self.appleSprites = pygame.sprite.Group()
        self.createApple()

        self.playerAdd = playerAdd
    
    def createApple(self):
        for pos in self.applePos:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(pos=(x,y), surf= self.appleSurf, groups=[self.appleSprites, self.groups()[0]], z=LAYERS['fruit'])
                

    def damage(self):
        # hit the tree
        self.health -= 1
        print(f"Tree damaged! Health: {self.health}, Apples: {len(self.appleSprites.sprites())}")

        # remove an apple
        if len(self.appleSprites.sprites()) > 0:
            randomApple = choice(self.appleSprites.sprites())
            randomApple.kill()
            Particle( pos= randomApple.rect.topleft,
                      surf= randomApple.image,
                    groups= self.groups()[0],
                    z= LAYERS['fruit'])
            self.playerAdd('apple')
            print(f"Apple removed! Remaining apples: {len(self.appleSprites.sprites())}")
        else:
            print("No apples to remove!")

    def checkDeath(self):
        if self.health <= 0:
            Particle(pos=self.rect.topleft, surf=self.image, groups=self.groups()[0], z=LAYERS['fruit'], duration=500)
            self.image = self.stumpSurface
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.playerAdd('wood')

        
    def update(self, dt):
        if self.alive: self.checkDeath()

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.startTime = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        maskSurface = pygame.mask.from_surface(self.image)
        newSurface = maskSurface.to_surface()
        newSurface.set_colorkey((0,0,0))
        self.image = newSurface
    
    def update(self, dt):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.startTime > self.duration:
            self.kill()

    
