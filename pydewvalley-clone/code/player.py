import pygame
from settings import *
from support import *
from debug import debug
from myTimer import Timer

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
    
        # tools
        self.tools = ['axe', 'water', 'hoe']
        self.toolIndex = 0
        self.selectedTool = self.tools[self.toolIndex]

        # seeds

        self.seeds = ['corn', 'tomato']
        self.seedIndex = 0
        self.selectedSeed = self.seeds[self.seedIndex]

        # timer
        self.timers = {
            'tool use': Timer(350, self.useTool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.useSeed),
            'seed switch': Timer(200)
        }
    
    def importAssets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                            'up_idle': [],'down_idle': [],'left_idle': [],'right_idle': [],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[], 'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
        
        for animation in self.animations.keys():
            fullPath = '../graphics/character/' + animation
            self.animations[animation] = importFolder(fullPath)

        # print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed();
        if not self.timers['tool use'].active:
            # Movement Direction
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
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # Tool Use

            if keys[pygame.K_SPACE]:
                # timer for the tool use
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frameIndex = 0

            # Change Tool

            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.toolIndex += 1
                if self.toolIndex >= len(self.tools):
                    self.toolIndex = 0
                self.selectedTool = self.tools[self.toolIndex]

            # Seeds Use

            if keys[pygame.K_w]:
                # timer for the tool use
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frameIndex = 0

            # Change Seed

            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seedIndex += 1
                self.seedIndex = self.seedIndex if self.seedIndex < len(self.seeds) else 0
                self.selectedSeed = self.seeds[self.seedIndex]

    def getStatus(self):
        # if player is idle, add idle to status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # if player is using some sort of tool, add tooluse to status
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_axe'

    def move(self, dt):
        if (self.direction.magnitude() > 0):
            self.direction = self.direction.normalize()


        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = self.position.x
        self.position.y += self.direction.y * self.speed * dt
        self.rect.y = self.position.y

    def animate(self, dt):
        self.frameIndex += 4 * dt;
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0;
        self.image = self.animations[self.status][int(self.frameIndex)]

    def updateTimers(self):
        for timer in self.timers.values():
            timer.update()

    def useTool(self):
        debug(self.selectedTool)

    def useSeed(self):
        debug(self.selectedSeed, 10, 30)

    def update(self, dt):
        self.input()
        self.getStatus()
        self.updateTimers()

        self.move(dt)
        self.animate(dt);