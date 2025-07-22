import pygame
from support import *
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__(self , pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

class SoilLayer:
    def __init__(self, allSprites):
        # sprite groups
        self.allSprites = allSprites
        self.soilSprites = pygame.sprite.Group()
        

        # graphics
        self.soilSurface = pygame.image.load('../graphics/soil/o.png')
        self.soilSurfaces = importFolderDictionary('../graphics/soil/')

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
                    self.grid[x][y].append('X') # X means soil Patch
                    self.createSoilTiles()

    def createSoilTiles(self):
        print("Created a soil tile")
        self.soilSprites.empty() # getting rid of existing soil tiles
        for index_row, row in enumerate(self.grid):
            for index_column, cell in enumerate(row):
                if 'X' in cell:
                    # TILE options
                    top = 'X' in self.grid[index_row - 1][index_column]
                    right = 'X' in row[index_column + 1]
                    left = 'X' in row[index_column - 1]
                    bottom = 'X' in self.grid[index_row + 1][index_column]

                    tileType = 'o' # default tile

                    # all sides
                    if all((top, right, bottom, left)):
                        tileType = 'x'

                    # horizontal tiles
                    if left and not any((top, right, bottom)):
                        


                    SoilTile((TILE_SIZE * index_row, TILE_SIZE * index_column), self.soilSurfaces[tileType], [self.allSprites, self.soilSprites])

    
