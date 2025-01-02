from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
            super().__init__(groups)

            # Image
            self.image = pygame.Surface(size['paddle'], pygame.SRCALPHA)  # 40 pixels wide 100 pixels tall
            pygame.draw.rect(self.image, colours['paddle'], pygame.FRect((0,0), size['paddle']), 0, 4) # rounds the corners of the paddle

            self.shadowSurf = self.image.copy()
            pygame.draw.rect(self.shadowSurf, colours['paddleShadow'], pygame.FRect((0,0), size['paddle']), 0, 4) # rounds the corners of the paddle

            self.rect = self.image.get_frect(center = (screenWidth - 50, screenHeight/2))
            self.oldRect = self.rect.copy()

            self.direction = 0

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt

        if self.rect.top < 0:
            self.rect.top = 0
        else:
            self.rect.top
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
        else:
            self.rect.bottom

    def update(self, dt):
        self.oldRect = self.rect.copy()
        self.getDirection()
        self.move(dt)

class Player(Paddle): #inheriting from the paddle class
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = speed['player']

    def getDirection(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.speed = speed['opponent']
        self.rect = self.image.get_frect(center = (50, screenHeight/2))
        self.ball = ball

    def getDirection(self):
    # Real Person using up and down key
    #     keys = pygame.key.get_pressed()
    #     self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

    # Simple AI   
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddleSprites, updateScore):
        super().__init__(groups)
        self.paddleSprites = paddleSprites
        self.updateScore = updateScore

        # image
        self.image = pygame.Surface(size['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, colours['ball'], (size['ball'][0] / 2, size['ball'][1] / 2), size['ball'][0] / 2)

        # adding a shadow
        self.shadowSurf = self.image.copy()
        pygame.draw.circle(self.shadowSurf, colours['ball'], (size['ball'][0] / 2, size['ball'][1] / 2), size['ball'][0] / 2)

        # rect & movement
        self.rect = self.image.get_frect(center = (screenWidth/2, screenHeight/2))
        self.oldRect = self.rect.copy()
        self.direction = pygame.Vector2(choice((1,-1)), uniform(0.7,0.8) * choice((1,-1)))
        self.speedMod = 0
        self.speed = speed['ball']

        # timer
        self.startTime = pygame.time.get_ticks()
        self.duration = 1500

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt * self.speedMod
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt * self.speedMod
        self.collision('vertical')

    def wallCollision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight
            self.direction.y *= -1

        # for testing
        # if self.rect.left <= 0:
        #     self.rect.left = 0
        #     self.direction.x *= -1

        if self.rect.right >= screenWidth or self.rect.left <= 0:
            self.updateScore('player' if self.rect.x < screenWidth / 2 else 'opponent') 
            self.reset()
    
        # if self.rect.right >= screenWidth:
        #     self.rect.right = screenWidth
        #     self.direction.x *= -1
    
    def reset(self):
        self.rect.center = (screenWidth/2, screenHeight/2)
        self.direction = pygame.Vector2(choice((1,-1)), uniform(0.7,0.8) * choice((1,-1)))
        self.startTime = pygame.time.get_ticks()
    
    def timer(self):
        if pygame.time.get_ticks() - self.startTime >= self.duration:
            self.speedMod = 1
        else:
            self.speedMod = 0
        



    def collision(self, direction):
        for sprite in self.paddleSprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.oldRect.right <= sprite.oldRect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= self.rect.right and self.oldRect.left >= sprite.oldRect.right:
                        self.rect.left = sprite.rect.right 
                        self.direction.x *= -1
                else: #direction == 'vertical'
                    if self.rect.bottom > sprite.rect.top and self.oldRect.bottom <= sprite.oldRect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top >= self.rect.bottom and self.oldRect.top <= sprite.oldRect.bottom:
                        self.rect.top = sprite.rect.bottom 
                        self.direction.y *= -1


    def update(self,dt):
        self.oldRect = self.rect.copy() # this stores the rect one frame before its updated
        self.timer()
        self.move(dt)
        self.wallCollision()


