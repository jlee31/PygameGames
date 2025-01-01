from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collisionSprites):
        super().__init__(groups)
        self.loadImages()
        self.state, self.frameIndex = 'down', 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitboxRect = self.rect.inflate(-60, -90) # removes the whitespace / overlap from the image
    
        self.direction = pygame.Vector2()
        self.speed = 400
        self.collisionSprites = collisionSprites # used later to check for collisions with, enabling collision handling logic to be implemented within the class

    def loadImages(self):
        self.frames = {'left': [],
                       'right': [],
                       'up': [],
                       'down': []}
        
        for state in self.frames.keys():
            for folderPath, subFolders, fileNames in walk(join('images', 'player', state)):
                if fileNames:
                    for fileName in sorted(fileNames, key=lambda name: int(name.split('.')[0])):
                        fullPath = join(folderPath, fileName) # this is the proper way to join paths
                        surf = pygame.image.load(fullPath).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        self.keys = pygame.key.get_pressed()
        self.direction.y = int(self.keys[pygame.K_s]) - int(self.keys[pygame.K_w])
        self.direction.x = int(self.keys[pygame.K_d]) - int(self.keys[pygame.K_a])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitboxRect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal') # checks for collision
        self.hitboxRect.y += self.direction.y * self.speed * dt
        self.collisions('vertical')
        self.rect.center = self.hitboxRect.center

    def collisions(self, direction):
        for sprite in self.collisionSprites:
            if sprite.rect.colliderect(self.hitboxRect):
                if direction == 'horizontal':
                    if self.direction.x > 0: # moving right
                        self.hitboxRect.right = sprite.rect.left # moves the player to the left side of the sprite
                    if self.direction.x < 0: # moving left
                        self.hitboxRect.left = sprite.rect.right 
                if direction == 'vertical':
                    if self.direction.y < 0: # moving up
                        self.hitboxRect.top = sprite.rect.bottom
                    if self.direction.y > 0: # moving down
                        self.hitboxRect.bottom = sprite.rect.top 

    def animate(self, dt): # need to study this more
        if self.direction.length() == 0:
            self.frameIndex = 0
            self.image = self.frames[self.state][self.frameIndex]
        else:
            # 1) get the state
            if self.direction.x != 0:
                self.state = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.state = 'down' if self.direction.y > 0 else 'up'
            # 2) animation
            self.frameIndex += 5 * dt
            self.image = self.frames[self.state][int(self.frameIndex) % len(self.frames[self.state])] # this will loop through the frames


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
    

        
        
