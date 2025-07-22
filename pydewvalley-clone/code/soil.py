import pygame
from support import *
from settings import *
from pytmx.util_pygame import load_pygame
from random import choice

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

class SoilLayer:
    def __init__(self, allSprites):
        # sprite groups
        self.allSprites = allSprites
        self.soilSprites = pygame.sprite.Group()
        self.waterSprites = pygame.sprite.Group()

        # graphics
        self.soilSurface = pygame.image.load('../graphics/soil/o.png')
        self.soilSurfaces = importFolderDictionary('../graphics/soil/')
        # self.waterSurface = pygame.image.load('../graphics/soil_water/')
        self.waterSurface = importFolder('../graphics/soil_water')

        # requirements
        self.createSoilGrid()
        self.createHitRects()
        # checking if the area is farmable

        # checking if the soil is watered

        # checking if the soil has a plant

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
                
