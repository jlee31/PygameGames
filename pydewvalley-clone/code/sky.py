import pygame
from settings import *
from support import *
from sprites import Generic
from random import randint, choice

class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):
        super().__init__(pos, surf, groups, z)
    
        # Generic Setup for a drop
        self.lifetime = randint(400, 500)
        self.startTime = pygame.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)
            # ^^^ the above three attributes are the things you need to move anything in pygame

    def update(self, dt):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # timer
        if pygame.time.get_ticks() - self.startTime >= self.lifetime:
            self.kill()
            
class Rain:
    def __init__(self, allSprites):
        self.allSprites = allSprites
        self.raindrops = importFolder('../graphics/rain/drops')
        self.rainfloor = importFolder('../graphics/rain/floor')
        self.floorW, self.floorH = pygame.image.load('../graphics/world/ground.png').get_size()

    def createFloor(self):
        Drop(choice(self.rainfloor), (randint(0, self.floorW), randint(0, self.floorH)), False, self.allSprites, LAYERS['rain floor'])
    def createDrops(self):
        Drop(choice(self.raindrops), (randint(0, self.floorW), randint(0, self.floorH)), False, self.allSprites, LAYERS['rain drops'])

    def update(self):
        self.createFloor()
        self.createDrops()