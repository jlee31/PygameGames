from settings import * 
from player import Player
from sprites import *
from random import randint, choice
from math import degrees
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game():
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("Vampire Survivor Clone")
        self.clock = pygame.time.Clock()
        self.running = True 

        # groups
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.bulletSprites = pygame.sprite.Group()
        self.enemySprites = pygame.sprite.Group()
        

        # GUN mechinaics / timer
        self.canShoot = True
        self.shootTime = 0
        self.gunCooldown = 100

        # Enemy Timer
        self.enemyEvent = pygame.event.custom_type()
        pygame.time.set_timer(self.enemyEvent, 500)
        self.spawnPos = []

        # setup
        self.loadImage()
        self.setup()

        #audio
        self.shootSound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shootSound.set_volume(0.1)
        self.impactSound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.1)
        self.music.play(loops=-1)

    def loadImage(self):
         self.bullet = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

         folders = list(walk(join('images', 'enemies')))[0][1]
         self.enemyFrames = {}
         
         for folder in folders:
              for folderPath, _, fileNames in walk(join('images', 'enemies', folder)):
                   self.enemyFrames[folder] = []
                   for fileName in sorted(fileNames, key = lambda name: int(name.split('.')[0])):
                        fullPath = join(folderPath, fileName)
                        surf = pygame.image.load(fullPath).convert_alpha()
                        self.enemyFrames[folder].append(surf)

    def gunTimer(self):
         if not self.canShoot:
                currenttime = pygame.time.get_ticks()
                if currenttime - self.shootTime >= self.gunCooldown:
                    self.canShoot = True

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.canShoot:
            self.shootSound.play()
            pos = self.gun.rect.center + self.gun.playerDirection * 50
            Bullet(self.bullet, pos, self.gun.playerDirection, (self.allSprites, self.bulletSprites)) # you need a surf, position, direction and a group
            self.canShoot = False
            self.shootTime = pygame.time.get_ticks()
            

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        
        for x,y,image in map.get_layer_by_name('Ground').tiles(): # these need to be changed to their pixel values
             Sprite((x * tileSize,y * tileSize), image, self.allSprites) # this shows the ground
             # order of creation matters, the ground goes first then the objects nexta 

        for obj in map.get_layer_by_name('Objects'):
              CollisionSprite((obj.x, obj.y), obj.image, (self.allSprites, self.collisionSprites)) # this shows the trees & objects

        for obj in map.get_layer_by_name('Collisions'):
             CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collisionSprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                # player - instead of making it in the init method, you would create it here
                self.player = Player((obj.x, obj.y), self.allSprites, self.collisionSprites)
                self.gun = Gun(self.player, self.allSprites) 
            else:
                self.spawnPos.append((obj.x, obj.y))

    def bulletCollisions(self):
        if self.bulletSprites:
            for bullet in self.bulletSprites:
                CollisionSprite = pygame.sprite.spritecollide(bullet, self.enemySprites, False, pygame.sprite.collide_mask)
                if CollisionSprite:
                    for sprite in CollisionSprite:
                        sprite.destroy()
                        self.impactSound.play()
                    bullet.kill()

    def playerCollision(self):
         if pygame.sprite.spritecollide(self.player, self.enemySprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemyEvent:
                    Enemy(choice(self.spawnPos), choice(list(self.enemyFrames.values())), (self.allSprites, self.enemySprites), self.player, self.collisionSprites)
            
            # update
            self.gunTimer()
            self.input()
            self.allSprites.update(dt)
            self.bulletCollisions()
            self.playerCollision()

            # draw
            self.screen.fill('black')
            self.allSprites.draw(self.player.rect.center)
            pygame.display.update()

if __name__ == '__main__': # only runs this main file
	game = Game()
	game.run()