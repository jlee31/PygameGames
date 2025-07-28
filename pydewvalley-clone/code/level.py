import pygame
from random import randint

from pytmx.util_pygame import load_pygame

from overlay import Overlay
from player import Player
from settings import *
from sky import Rain, Sky
from soil import SoilLayer
from sprites import Generic, Interaction, Tree, Water, Wildflower, Particle
from support import *
from transition import Transition
from menu import Menu

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.allSprites = CameraGroup()
		self.collisionSprites = pygame.sprite.Group()
		self.treeSprites = pygame.sprite.Group()
		self.interactionSprites = pygame.sprite.Group()


		self.soilLayer = SoilLayer(self.allSprites, self.collisionSprites)
		self.setup()
		self.Overlay = Overlay(self.player)

		# missing transition??

		# Sky Stuff
			# Rain
		self.rain = Rain(self.allSprites)
		self.raining = randint(0, 10) > 3
		self.soilLayer.raining = self.raining
			# Sky
		self.sky = Sky()

		# Shop / Merchant Stuff
		self.menu = Menu(self.player, self.toggleShop)
		self.shopActive = False

		# Music
		self.success = pygame.mixer.Sound('../audio/success.wav')
		self.success.set_volume(0.3)
		self.bgMusic = pygame.mixer.Sound('../audio/music.mp3')
		self.bgMusic.set_volume(0.2)
		self.bgMusic.play(loops=-1)

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
				self.player = Player((obj.x, obj.y), self.allSprites, self.collisionSprites, self.treeSprites, self.interactionSprites, self.soilLayer, self.toggleShop)
			if obj.name == 'Bed':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactionSprites, 'Bed')

			if obj.name == 'Trader':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interactionSprites, 'Trader')

		self.transition = Transition(self.resetDay, self.player)



	def resetDay(self):
		# the apples of the trees
		for tree in self.treeSprites.sprites():
			for apple in tree.appleSprites.sprites():
				apple.kill()
			tree.createApple()

		# plants
		self.soilLayer.updatePlants( )

		# soil
		self.soilLayer.removeWater()
		self.raining = randint(0, 10) > 8 

		# randomizing rain
		self.soilLayer.raining = self.raining
		if self.raining:
			self.soilLayer.water_all()

		# Sky

		self.sky.startColour = [255,255,255]

	def playerAdd(self, item):
		self.player.itemInventory[item] += 1

		# sound
		self.success.play()

	def toggleShop(self):
		self.shopActive = not self.shopActive

	def plantCollision(self):
		if self.soilLayer.plantSprites:
			for plant in self.soilLayer.plantSprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					plant.kill()
					print("PLANT COLLECTED")
					self.playerAdd(plant.plantType)
					Particle(plant.rect.topleft, plant.image, self.allSprites, LAYERS['main'])
					self.soilLayer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self, dt): 

		# Drawing Logic
		self.display_surface.fill('black')
		# self.allSprites.draw(self.player)
		self.allSprites.customDraw(self.player)

		# Updates
		if self.shopActive:
			self.menu.update()
		else:
			self.allSprites.update(dt)
			# plant collision
			self.plantCollision()

		# Update soil layer (for plant growth)
		self.soilLayer.updatePlants()

		# weather
		self.Overlay.display()

		# Rain Stuff
		if self.raining and not self.shopActive:
			self.rain.update()

		# Daytime
		self.sky.display(dt)

		# Transition Overlay
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

				# anaytics
				# if sprite == player:
				# 	pygame.draw.rect(self.displaySurface,'red',offsetRect,5)						
				# 	hitbox_rect = player.hitbox.copy()
				# 	hitbox_rect.center = offsetRect.center
				# 	pygame.draw.rect(self.displaySurface,'green',hitbox_rect,5)
				# 	target_pos = offsetRect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
				# 	pygame.draw.circle(self.displaySurface,'blue',target_pos,5)
				