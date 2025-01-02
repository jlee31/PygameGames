from settings import *
from sprites import Sprite, Player, Bee, Worm, Bullet, Fire
from groups import AllSprites
from support import *
from timer import Timer
from random import randint

class Game():
    def loadAssets(self):
        # graphics
        self.playerFrames = import_folder('images', 'player')
        self.bulletSurf = import_image('images', 'gun', 'bullet')
        self.fireSurf = import_image('images', 'gun', 'fire')
        self.beeFrames = import_folder('images', 'enemies', 'bee')
        self.wormFrames = import_folder('images', 'enemies', 'worm')

        # sounds
        # either you can import them like this
        bGmusic = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.shootSound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.impactSound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        # or create a function that just makes it into a dictionary
        self.audio = audioImport('audio')
        # self.audio['music'].play()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("Platformer Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.bulletSprites = pygame.sprite.Group()

        # enemy sprite group
        self.enemySprites = pygame.sprite.Group()

        # Loading the Game
        self.loadAssets()
        self.setup()

        #timers
        self.beeTimer = Timer(2000, func = self.createBee)
        self.beeTimer.activate()

    def createBee(self):
        Bee(frames= self.beeFrames, 
            pos = (self.levelWidth + screenWidth,randint(0,self.levelHeight)), 
            groups = (self.allSprites, self.enemySprites),
            speed = randint(300,500))

    def createBullet(self, pos, direction):
        x = pos[0] + direction * 35 if direction == 1 else pos[0] + direction * 35 - self.bulletSurf.get_width()
        Bullet(self.bulletSurf, (x, pos[1]), direction, (self.allSprites, self.bulletSprites))
        Fire(self.fireSurf, pos, self.allSprites, self.player)
        self.shootSound.play()

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx')) # loading the map
        self.levelWidth = map.width * TILE_SIZE
        self.levelHeight = map.height * TILE_SIZE

        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, (self.allSprites, self.collisionSprites)) # loading the main thing 
            #       coordinates of the thing      image   sprites
        
        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.allSprites)
        
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.allSprites, self.collisionSprites, self.playerFrames, self.createBullet) # creating the player starting point
            if obj.name == 'Worm':
                Worm(self.wormFrames, pygame.FRect(obj.x,obj.y, obj.width, obj.height), (self.allSprites, self.enemySprites))

        self.audio['music'].play(loops = -1)
        
    def collision(self):
        # bullets and enemies
        for bullet in self.bulletSprites:
            spriteCollision = pygame.sprite.spritecollide(bullet, self.enemySprites, False, pygame.sprite.collide_mask)
            if spriteCollision:
                bullet.kill()
                for sprite in spriteCollision:
                    sprite.destroy()
                    self.impactSound.play()

        # enemies and player
        if pygame.sprite.spritecollide(self.player, self.enemySprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Update
            self.beeTimer.update()
            self.allSprites.update(dt)
            self.collision()

            # Draw
            self.screen.fill(BG_COLOR)
            self.allSprites.draw(self.player.rect.center) # allSprites is now using the Allsprites clas and its finding the player position to move the camera
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()