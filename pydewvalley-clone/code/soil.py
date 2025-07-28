import pygame
from support import *
from settings import *
from pytmx.util_pygame import load_pygame
from random import choice
from debug import *
class SoilTile(pygame.sprite.Sprite):
    def __init__(self , pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']
class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, checkIfWatered):
        super().__init__(groups)
        # plant setup
        self.plantType = plant_type
        self.frames = importFolder(f'../graphics/fruit/{self.plantType}')
        self.soil = soil

        self.checkIfWatered = checkIfWatered

        # plant growing
        self.age = 0
        self.maxAge = len(self.frames) - 1
        self.growSpeed = GROW_SPEED[plant_type]
        self.harvestable = False

        # Debug: Print frame info
        print(f"Plant created: {plant_type}")
        print(f"Number of frames: {len(self.frames)}")
        print(f"Max age: {self.maxAge}")
        print(f"Grow speed: {self.growSpeed}")

        # self.spritesetup
        self.image = self.frames[self.age]
        self.yOffSet = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.yOffSet))
        self.z = LAYERS['ground plant']

    def grow(self):
        if self.checkIfWatered(self.rect.center):
            self.age += self.growSpeed
            # Cap the age at maxAge
            if self.age > self.maxAge:
                self.age = self.maxAge
            print(f"Plant growing: {self.plantType}, age: {self.age:.2f}, maxAge: {self.maxAge}")
            print(f"Using frame index: {int(self.age)} out of {len(self.frames)} frames")

            if int(self.age) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26,-self.rect.height * 0.4)

            if self.age >= self.maxAge:
                self.harvestable = True
            
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.yOffSet))

class SoilLayer:
    def __init__(self, allSprites, collisionSprites):
        # sprite groups
        self.allSprites = allSprites
        self.collisionSprites = collisionSprites
        self.soilSprites = pygame.sprite.Group()
        self.waterSprites = pygame.sprite.Group()
        self.plantSprites = pygame.sprite.Group()
        # graphics
        self.soilSurface = pygame.image.load('../graphics/soil/o.png')
        self.soilSurfaces = importFolderDictionary('../graphics/soil/')
        # self.waterSurface = pygame.image.load('../graphics/soil_water/')
        self.waterSurface = importFolder('../graphics/soil_water')

        # requirements
        self.createSoilGrid()
        self.createHitRects()
        
         # sounds
        self.hoeSound = pygame.mixer.Sound('../audio/hoe.wav')
        self.hoeSound.set_volume(0.05)

        self.plantSound = pygame.mixer.Sound('../audio/plant.wav')
        self.plantSound.set_volume(0.2)

    def createSoilGrid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        horizontalTiles = ground.get_width() // TILE_SIZE
        verticalTiles = ground.get_height() // TILE_SIZE
        
        self.grid = [ [         [] for col in range(horizontalTiles)       ] for row in range(verticalTiles)      ] # getting a multi dimensional list for the map grid
        listOfTiles = load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles()
        for x, y, _ in listOfTiles: # x, y, surf but we dont need surf so x, y, _
            self.grid[y][x].append('F')
        # print(self.grid)

    def createHitRects(self):
        self.hitRects = []
        for index_row, row in enumerate(self.grid):
            for index_column, cell in enumerate(row):
                if 'F' in cell:
                    # turning the position of the grid into an actual x, y position in the game
                    x = TILE_SIZE * index_column
                    y = TILE_SIZE * index_row
                    rect = pygame.Rect(x,y, TILE_SIZE, TILE_SIZE)
                    self.hitRects.append(rect)

    def getHit(self, point):
        for rect in self.hitRects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    # print('FARMABLE')
                    self.grid[y][x].append('X') # X means soil Patch
                    self.createSoilTiles()
                    if self.raining:
                        self.water_all()
            
                # Sound
                self.hoeSound.play()
                
    def createSoilTiles(self):
        print("Created a soil tile")
        self.soilSprites.empty() # getting rid of existing soil tiles
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if 'X' in cell:
                    # Boundary checks
                    top = row_idx > 0 and 'X' in self.grid[row_idx - 1][col_idx]
                    bottom = row_idx < len(self.grid) - 1 and 'X' in self.grid[row_idx + 1][col_idx]
                    left = col_idx > 0 and 'X' in row[col_idx - 1]
                    right = col_idx < len(row) - 1 and 'X' in row[col_idx + 1]

                    tileType = 'o' # default tile

                    # all sides
                    if all((top, right, bottom, left)):
                        tileType = 'x'

                    # horizontal tiles
                    if left and not any((top, right, bottom)):
                        tileType = 'r'
                    if right and not any((top, left, bottom)):
                        tileType = 'l'
                    if right and left and not any((top, bottom)):
                        tileType = 'lr'

                    # vertical tiles
                    if top and not any((right, left, bottom)):
                        tileType = 'b'
                    if bottom and not any((right, left, top)):
                        tileType = 't'
                    if top and bottom and not any((left, right)):
                        tileType = 'tb'

                    # corners
                    if left and bottom and not any((top, right)):
                        tileType = 'tr'
                    if left and top and not any((bottom, right)):
                        tileType = 'br'
                    if right and bottom and not any((top, left)):
                        tileType = 'tl'
                    if right and top and not any((bottom, left)):
                        tileType = 'bl'
                    
                    # t-shape pieces
                    if top and bottom and left and not right:
                        tileType = 'tbl'
                    if top and bottom and right and not left:
                        tileType = 'tbr'
                    if left and right and top and not bottom:
                        tileType = 'lrt'
                    if left and right and bottom and not top:
                        tileType = 'lrb'

                    # Corrected tile placement
                    SoilTile((TILE_SIZE * col_idx, TILE_SIZE * row_idx), self.soilSurfaces[tileType], [self.allSprites, self.soilSprites])

    def water(self, point):
        for soilSprite in self.soilSprites.sprites():
            if soilSprite.rect.collidepoint(point):
                # print("WATERREERED")
                # add entry to soil grid
                x = soilSprite.rect.x // TILE_SIZE
                y = soilSprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                # create water sprite
                surf = choice(self.waterSurface)
                WaterTile((x * TILE_SIZE,y * TILE_SIZE), surf ,[self.allSprites, self.waterSprites])

    def water_all(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    WaterTile((col_idx * TILE_SIZE,row_idx * TILE_SIZE), choice(self.waterSurface) ,[self.allSprites, self.waterSprites])

    def removeWater(self):
        # destroy water sprites
        for sprite in self.waterSprites.sprites():
            sprite.kill()
        # clean up the grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def checkIfWatered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        print(f"Checking if watered at {pos}: {is_watered} (cell: {cell})")
        return is_watered

    def plantSeed(self, targetPos, seed):
        print(f"plantSeed called with targetPos: {targetPos}, seed: {seed}")
        for soilSprite in self.soilSprites.sprites():
            if soilSprite.rect.collidepoint(targetPos):
                # sound
                self.plantSound.play()

                # code
                x = soilSprite.rect.x // TILE_SIZE
                y = soilSprite.rect.y // TILE_SIZE
                print("PLANTING SEED 1")

                if not 'P' in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    debug("PLANTING SEED", 20, 40)
                    print("PLANTING SEED 2")
                    Plant(
                        plant_type=seed,
                        groups=[self.allSprites, self.plantSprites, self.collisionSprites],
                        soil=soilSprite,
                        checkIfWatered=self.checkIfWatered
                    )
                    print(f"Plant created! Total plants: {len(self.plantSprites.sprites())}")
                    print(f"New plant age: 0, maxAge: {len(importFolder(f'../graphics/fruit/{seed}')) - 1}")
                else:
                    print("Soil already has a plant!")
            else:
                print(f"Soil not found at targetPos: {targetPos}")
        print(f"No soil found at targetPos: {targetPos}")

    def updatePlants(self):
        for plant in self.plantSprites.sprites():
            plant.grow()

    def update(self, dt):
        # Update all plants for growth
        for plant in self.plantSprites.sprites():
            plant.grow()