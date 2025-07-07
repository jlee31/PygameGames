import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group);

        self.importAssets()

        self.status = 'down_idle'
        self.frameIndex = 0



        # Player Model

        self.image = self.animations[self.status][self.frameIndex];
        
        self.rect = self.image.get_rect(center = pos)

        # Movement Attributes
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200;  

    def importAssets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
        
        for animation in self.animations.keys():
            fullPath = '../graphics/character/' + animation
            self.animations[animation] = importFolder(fullPath)

        print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed();

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt):
        if (self.direction.magnitude() > 0):
            self.direction = self.direction.normalize()


        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = self.position.x
        self.position.y += self.direction.y * self.speed * dt
        self.rect.y = self.position.y

    def update(self, dt):
        self.input()
        self.move(dt)