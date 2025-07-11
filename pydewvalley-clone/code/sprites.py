import pygame 
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

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

class Tree(Generic):
    def __init__(self, pos, surf, groups, names):
        super().__init__(pos, surf, groups, names)

    
