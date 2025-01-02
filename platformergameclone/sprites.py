from settings import *
from timer import Timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        # adjustment
        self.image = pygame.transform.flip(self.image, direction == -1, False)

        self.direction = direction
        self.speed = 800
    
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart=True, func = self.kill)
        self.yOffset = pygame.Vector2(0,8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.yOffset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.yOffset

    def update(self, ___):
        self.timer.update()

        if self.player.flip: # this is used because if you jump and shoot there is a weird offset between the fire animation and the player pos
            self.rect.midright = self.player.rect.midleft + self.yOffset
        else:
            self.rect.midleft = self.player.rect.midright + self.yOffset

        if self.flip != self.player.flip:
            self.kill()
        
class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames = frames
        self.frameIndex = 0
        self.animationSpeed = 10
        super().__init__(pos, self.frames[self.frameIndex], groups)

    def animate(self, dt):
        self.frameIndex += self.animationSpeed * dt
        self.image = self.frames[int(self.frameIndex) % len(self.frames)]

    # the code above is the basic animation class framework

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.deathTimer = Timer(200, func = self.kill)

    def destroy(self):
        self.deathTimer.activate()
        self.animationSpeed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        self.deathTimer.update()
        if not self.deathTimer:
            self.move(dt)
            self.animate(dt)
            self.constraint()
            
class Bee(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(500,600)
        self.frequency = randint(300,600)

    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.right <= 0:
            self.kill()
    
class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.speed = randint(50,150)
        self.mainRect = rect
        self.rect.bottomleft = rect.bottomleft
        self.direction = 1

    def move(self, dt):
        self.rect.x += self.speed * self.direction * dt
    
    def constraint(self):
        if not self.mainRect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames] # this flips the image if they are moving in the opposite direction

class Player(AnimatedSprite): # inheriting from sprite

    def __init__(self, pos, groups, collisionSprites, frames, createBullet):
        # surf = pygame.Surface((40,80))
        super().__init__(frames, pos, groups) # the ordering matters
        self.flip = False
        self.createBullet = createBullet

        # movement & collision
        self.direction = pygame.Vector2()
        self.collisionSprites = collisionSprites
        self.speed = 400
        self.gravity = 50
        self.onFloor = False

        # timer
        self.shootTimer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        # self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        # self.direction = self.direction.normalize() if self.direction else self.direction
        if keys[pygame.K_SPACE] and self.onFloor:
            self.direction.y = -20

        if keys[pygame.K_e] and not self.shootTimer:
            self.createBullet(self.rect.center, -1 if self.flip else 1) # pos and direction
            self.shootTimer.activate()
            
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical movement
        # self.rect.y += self.direction.y * self.speed * dt
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collisionSprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def checkFloor(self):
        bottomRect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        levelRects = [sprite.rect for sprite in self.collisionSprites] # lists of rectangles 
        self.onFloor = True if bottomRect.collidelist(levelRects) >= 0 else False

    def animate(self, dt):
        if self.direction.x:
            self.frameIndex += self.animationSpeed * dt
            self.flip = self.direction.x < 0
        else:
            self.frameIndex = 0

        if not self.onFloor: # jumping frame
            self.frameIndex = 1

        self.image = self.frames[int(self.frameIndex) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, dt):
        self.shootTimer.update()
        self.checkFloor()
        self.input()
        self.move(dt)
        self.animate(dt)


    