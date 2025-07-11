import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic
from pytmx.util_pygame import load_pygame

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.allSprites = CameraGroup()

		self.setup()
		self.Overlay = Overlay(self.player)

	def setup(self):
		# setting up actual map
		tmxData = load_pygame('../data/map.tmx')
		# house
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x,y,surf in tmxData.get_layer_by_name(layer).tiles():
				Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=self.allSprites, z=LAYERS['house bottom'])
		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x,y,surf in tmxData.get_layer_by_name(layer).tiles():
				Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=self.allSprites, z=LAYERS['main'])
		for x,y,surf in tmxData.get_layer_by_name('Fence').tiles():
			Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=self.allSprites, z=LAYERS['main'])

		# setting up water
	
		# setting up trees

		# setting up flowers



		# Setting up the image
		Generic(pos = (0,0), surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(), groups = self.allSprites, z = LAYERS['ground'])
		self.player = Player((1000, 1000), self.allSprites)

	def run(self,dt): 
		self.display_surface.fill('black')
		# self.all_sprites.draw(self.display_surface)
		self.allSprites.customDraw(self.player)
		self.allSprites.update(dt)

		self.Overlay.display()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.displaySurface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()


	def customDraw(self, player):
		self.offset.x = player.rect.centerx - (SCREEN_WIDTH  / 2)
		self.offset.y = player.rect.centery - (SCREEN_HEIGHT / 2)


		for Layer in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == Layer:
					offsetRect = sprite.rect.copy()
					offsetRect.center -= self.offset
					self.displaySurface.blit(sprite.image, offsetRect)