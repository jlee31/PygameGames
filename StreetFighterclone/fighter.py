from settings import *

class Fighter():
    def __init__(self, player, x, y, flip, data, spritesheet, animationsteps, hitsound):
        self.player = player
        self.size = data[0]
        self.imageScale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animationList = self.loadImages(spritesheet, animationsteps)
        self.action = 0 # idle, run, jump, attack1, attack2, hit, death
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()
        self.rect = pygame.Rect((x,y, 80, 180))
        self.velY = 0
        self.jump = False
        self.running = False
        self.attackType = 0
        self.attackCooldown = 0
        self.hit = False
        self.attacking = False
        self.health = 100
        self.alive = True
        self.hitsound = hitsound

    def loadImages(self, spriteSheet, FrameSteps):
        animationList = []
        for y, animation in enumerate(FrameSteps):
            tempImgLst = []
            for i in range(animation):
                tempImg = spriteSheet.subsurface(i * self.size, y * self.size ,self.size, self.size)
                tempImg = pygame.transform.scale(tempImg, (self.size * self.imageScale, self.size * self.imageScale))
                tempImgLst.append(tempImg)
            animationList.append(tempImgLst)
        return animationList

    def move(self, surface, target, roundOver):
        self.speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attackType = 0


        # input
        key = pygame.key.get_pressed()
        if self.player == 1 and self.alive and roundOver == False:
            if not self.attacking:
                if key[pygame.K_a]:
                    dx = -self.speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = self.speed
                    self.running = True
                if not self.jump:
                    if key[pygame.K_w]:
                        self.velY = -30
                        self.jump = True

                # Attacks
                if key[pygame.K_e]:
                    self.attackType = 1
                    self.attack(target)
                if key[pygame.K_r]:
                    self.attackType = 2
                    self.attack(target)

            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

        elif self.player == 2 and self.alive and roundOver == False: 
            if not self.attacking:
                if key[pygame.K_LEFT]:
                    dx = -self.speed
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = self.speed
                    self.running = True
                if not self.jump:
                    if key[pygame.K_UP]:
                        self.velY = -30
                        self.jump = True

                # Attacks
                if key[pygame.K_m]:
                    self.attackType = 1
                    self.attack(target)
                    
                if key[pygame.K_n]:
                    self.attackType = 2
                    self.attack(target)


            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

        # cooldown
        if self.attackCooldown > 0:
            self.attackCooldown -= 1

        # Y movement
        self.velY += gravity
        dy += self.velY

        # bounds
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screenWidth:
            dx = screenWidth - self.rect.right
        if self.rect.bottom + dy > screenHeight - 110:
            self.velY = 0
            dy = screenHeight - 110 - self.rect.bottom
            self.jump = False


        self.rect.x += dx
        self.rect.y += dy

    # updates
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.updateAction(6)
        elif self.hit == True:
            self.updateAction(5)
        elif self.attacking:
            if self.attackType == 1:
                self.updateAction(3)
            elif self.attackType == 2:
                self.updateAction(4)
        elif self.jump:
            self.updateAction(2)
        elif self.running:
            self.updateAction(1)
        else:
            self.updateAction(0)

        animationCooldown = 100
        #updating image
        self.image = self.animationList[self.action][self.frameIndex]
        #checking if enough time passed since last update
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        #check if animation finishes
        if self.frameIndex >= len(self.animationList[self.action]):
            #checking if player died
            if self.alive == False:
                self.frameIndex = len(self.animationList[self.action]) - 1
            else: 
                self.frameIndex = 0
                # checking if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attackCooldown = 50
                # cehck if damage was taken
                if self.action == 5:
                    self.hit = False
                # if player was hit when doing a hit, stop the attack
                    self.attacking = False
                    self.attackCooldown = 50




    def attack(self, target): 
        if self.attackCooldown == 0:
            self.attacking = True
            self.hitsound.play()
            attackingRect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            # pygame.draw.rect(surface, (255,255,0), attackingRect)
            if attackingRect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def updateAction(self, newAction):
        # check if new action is diff to prev action
        if newAction != self.action:
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255,0,0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.imageScale), self.rect.y - (self.offset[1] * self.imageScale)))