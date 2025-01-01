from settings import *
from math import atan2, degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos) 
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos) #usually with tiled you should put the stuff in the topleft

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):

        self.player = player
        self.distance = 120
        self.playerDirection = pygame.Vector2(1,0) #direction of the gun to the player

        super().__init__(groups)
        self.gunSurf = pygame.image.load(join('images', 'gun' ,'gun.png')).convert_alpha()
        self.image = self.gunSurf
        self.rect = self.gunSurf.get_frect(center = self.player.rect.center + self.playerDirection * self.distance)

    def getDirection(self):
        mousePosition = pygame.Vector2(pygame.mouse.get_pos()) # turning the mouse x and y coords into a vector
        playerPosition = pygame.Vector2(screenWidth/2, screenHeight/2) # the player's position
        self.playerDirection = (mousePosition - playerPosition).normalize() # the direction of the gun

    def rotateGun(self):
        angle = degrees(atan2(self.playerDirection.x, self.playerDirection.y)) - 90 # gets the angle of the gun
        if self.playerDirection.x > 0:
            self.image = pygame.transform.rotozoom(self.gunSurf, angle, 1) # rotates the gun
        else:
            self.image = pygame.transform.rotozoom(self.gunSurf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.getDirection()
        self.rotateGun()
        self.rect.center = self.player.rect.center + self.playerDirection * self.distance # this is the gun's position

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = surf.get_frect(center = pos)
        self.spawnTime = pygame.time.get_ticks()
        self.lifetime = 1000
    
        self.direction = direction
        self.speed = 1000

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt # this moves the bullet in its respective direction
        if pygame.time.get_ticks() - self.spawnTime >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collisionSprites):
        super().__init__(groups)
        self.player = player
    
        self.frames, self.frameIndex = frames, 0
        self.image = self.frames[self.frameIndex]
        self.animationSpeed = 6

        # rect
        self.rect = self.image.get_frect(center = pos)
        self.hitboxRect = self.rect.inflate(-25, -50)
        self.collisionSprites = collisionSprites 
        self.direction = pygame.Vector2
        self.speed = 300

        # timer
        self.deathtime = 0
        self.deathduration = 400

    def animate(self, dt):
        self.frameIndex += self.animationSpeed * dt
        self.image = self.frames[int(self.frameIndex % len(self.frames))]

    def move(self, dt):
        # get direction
        playerPos = pygame.Vector2(self.player.rect.center)
        enemyPos = pygame.Vector2(self.rect.center)
        self.direction = (playerPos - enemyPos).normalize()

        # update rect position + collision logic
        self.hitboxRect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
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

    def destroy(self):
        # start a timer
        self.deathtime = pygame.time.get_ticks()
        # change the image
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def deathTimer(self):
        if pygame.time.get_ticks() - self.deathtime >= self.deathduration:
            self.kill()

    def update(self, dt):
        if self.deathtime == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.deathTimer()
