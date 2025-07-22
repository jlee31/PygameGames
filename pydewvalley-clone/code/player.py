import pygame
from settings import *
from support import *
from debug import debug
from myTimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collisionSprites, treeSprites, interaction, soilLayer):
        super().__init__(group);

        self.importAssets()
        self.status = 'down_idle'        
        self.frameIndex = 0
        self.z= LAYERS['main']

        # Player Model

        self.image = self.animations[self.status][self.frameIndex];
        
        self.rect = self.image.get_rect(center = pos)

        # Setting up Collisions

        self.hitbox = self.rect.copy().inflate(-126, -70)
        # inflate takes the rectangle and keeping the dimension while staying centered


        # Movement Attributes
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200;  

        # Collisions

        self.collisionSprites = collisionSprites
    
        # tools
        self.tools = ['axe', 'water', 'hoe']
        self.toolIndex = 0
        self.selectedTool = self.tools[self.toolIndex]

        # seeds

        self.seeds = ['corn', 'tomato']
        self.seedIndex = 0
        self.selectedSeed = self.seeds[self.seedIndex]

        # inventory

        self.itemInventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }

        

        # timer
        self.timers = {
            'tool use': Timer(350, self.useTool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.useSeed),
            'seed switch': Timer(200)
        }

        # interactions
        self.treeSprites = treeSprites
        self.interaction = interaction
        self.sleep = False
        self.soilLayer = soilLayer

    def getTargetPosition(self):
        self.targetPosition = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
    
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
        if not self.timers['tool use'].active and not self.sleep:
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


            if keys[pygame.K_RETURN]:
                collidedInteractionSprite = pygame.sprite.spritecollide(sprite=self, group=self.interaction, dokill=False)
                if collidedInteractionSprite:
                    if collidedInteractionSprite[0].name == 'Trader':
                        pass
                    else: 
                        self.sleep = True
                        self.status = 'left_idle'

    def getStatus(self):
        # if player is idle, add idle to status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # if player is using some sort of tool, add tooluse to status
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selectedTool

    def collision(self, direction):
        for sprite in self.collisionSprites.sprites():
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.position.x = self.hitbox.centerx

                if direction == 'vertical':
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top

                   # how it works: when   
                
                    self.rect.centery = self.hitbox.centery
                    self.position.y = self.hitbox.centery

    def move(self, dt):
        if (self.direction.magnitude() > 0):
            self.direction = self.direction.normalize()

        # Horizontal movement 
        ''' Old Movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.centerxx = self.position.x
        '''
        
        self.position.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        
        # Vertical movement
        ''' Old Movement 
        self.position.y += self.direction.y * self.speed * dt
        self.rect.centery = self.position.y
        '''
        self.position.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

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
        # Calculate target position when tool is used
        self.getTargetPosition()
        if self.selectedTool == 'hoe':
            self.soilLayer.getHit(self.targetPosition)

        if self.selectedTool == 'axe':
            print(f"Axe used at target position: {self.targetPosition}")
            for tree in self.treeSprites.sprites():
                print(f"Checking tree at {tree.rect.center} with {len(tree.appleSprites.sprites())} apples")
                if tree.rect.collidepoint(self.targetPosition):
                    print(f"Tree hit! Apples before: {len(tree.appleSprites.sprites())}")
                    tree.damage()
                    print(f"Apples after: {len(tree.appleSprites.sprites())}")
                else:
                    print("Tree not hit - no collision")
        if self.selectedTool == 'water':
            self.soilLayer.water(self.targetPosition)

    def useSeed(self):
        debug(self.selectedSeed, 10, 30)

    def update(self, dt):
        self.input()
        self.getStatus()
        self.updateTimers()
        self.getTargetPosition()

        self.move(dt)
        self.animate(dt);