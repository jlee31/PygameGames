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
                            'up_idle': [],'down_idle': [],'left_idle': [],'right_idle': [],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
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
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'right'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'left'
        else:
            self.direction.x = 0

    def getStatus(self):
        # if player is idle, add idle to status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def animate(self, dt):
        self.frameIndex += 4 * dt;
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0;
        self.image = self.animations[self.status][int(self.frameIndex)]
    
    def move(self, dt):
        if (self.direction.magnitude() > 0):
            self.direction = self.direction.normalize()


        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = self.position.x
        self.position.y += self.direction.y * self.speed * dt
        self.rect.y = self.position.y

    def update(self, dt):
        self.input()
        self.getStatus()
        self.move(dt)
        self.animate(dt);