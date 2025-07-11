import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.allSprites = CameraGroup()

		self.setup()
		self.Overlay = Overlay(self.player)

	def setup(self):
		# Setting up the image
		Generic(pos = (0,0), surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(), groups = self.allSprites, z = LAYERS['ground'])
		self.player = Player((100, 100), self.allSprites)

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