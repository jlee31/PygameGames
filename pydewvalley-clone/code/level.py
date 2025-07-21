import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Wildflower, Tree, Interaction
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.allSprites = CameraGroup()
		self.collisionSprites = pygame.sprite.Group()
		self.treeSprites = pygame.sprite.Group()
		self.interactionSprites = pygame.sprite.Group()


		self.soilLayer = SoilLayer(self.allSprites)
		self.setup()
		self.Overlay = Overlay(self.player)

		# missing transition??

		



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

		# Fence
		for x,y,surf in tmxData.get_layer_by_name('Fence').tiles():
			Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=[self.allSprites, self.collisionSprites], z=LAYERS['main'])

		# setting up water
		waterFrames = importFolder('../graphics/water')
		for x,y,surf in tmxData.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE, y * TILE_SIZE), waterFrames, self.allSprites)
		
		# setting up trees
		for obj in tmxData.get_layer_by_name('Trees'):
			Tree((obj.x, obj.y), obj.image, [self.allSprites, self.collisionSprites, self.treeSprites], obj.name, self.playerAdd)
		print(f"Created {len(self.treeSprites.sprites())} trees")
		
		# setting up flowers
		for obj in tmxData.get_layer_by_name('Decoration'):
			Wildflower((obj.x, obj.y), obj.image, [self.allSprites, self.collisionSprites])	

		# Setting up the image
		Generic(pos = (0,0), surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(), groups = self.allSprites, z = LAYERS['ground'])

		# collision tiles
		for x, y, surf in tmxData.get_layer_by_name('Collision').tiles(): 
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collisionSprites)

		# Creating instance of the player here
		# self.player = Player((1000, 1000), self.allSprites, self.collisionSprites, treeSprites=self.treeSprites)

		for obj in tmxData.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player((obj.x, obj.y), self.allSprites, self.collisionSprites, self.treeSprites, self.interactionSprites, self.soilLayer)
			if obj.name == 'Bed':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactionSprites, 'Bed')

		self.transition = Transition(self.resetDay, self.player)

	def resetDay(self):
		# the apples of the trees
		for tree in self.treeSprites.sprites():
			for apple in tree.appleSprites.sprites():
				apple.kill()
			tree.createApple()

	def playerAdd(self, item):
		self.player.itemInventory[item] += 1

	def run(self,dt): 
		self.display_surface.fill('black')
		# self.allSprites.draw(self.display_surface)
		self.allSprites.customDraw(self.player)
		self.allSprites.update(dt)

		self.Overlay.display()

		if self.player.sleep:
			self.transition.play()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.displaySurface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()


	def customDraw(self, player):
		self.offset.x = player.rect.centerx - (SCREEN_WIDTH  / 2)
		self.offset.y = player.rect.centery - (SCREEN_HEIGHT / 2)

		for Layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
				if sprite.z == Layer:
					offsetRect = sprite.rect.copy()
					offsetRect.center -= self.offset
					self.displaySurface.blit(sprite.image, offsetRect)

				# analytics
				# if sprite == player:
				# 	pygame.draw.rect(self.displaySurface, 'red', offsetRect, 5)
				# 	hitboxRect = offsetRect.copy()
				# 	hitboxRect.center = offsetRect.center
				# 	pygame.draw.rect(self.displaySurface, 'green', hitboxRect, 5)
				# 	targetPos = offsetRect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
				# 	pygame.draw.circle(self.displaySurface, 'blue', targetPos, 5)
					