import pygame
from settings import *
from support import *
from sprites import Generic
from random import randint

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
class Rain:
    def __init__(self, allSprites):
        self.allSprites = allSprites
        self.raindrops = importFolder('../graphics/rain/drops')
        self.rainfloor = importFolder('../graphics/rain/floor')
        self.floorW, self.floorH = pygame.image.load('../graphics/world/ground.png').get_size()

    def createFloor(self):
        Drop()
    def createDrops(self):
        pass
    def update(self):
        self.createFloor()
        self.createDrops()