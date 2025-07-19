import pygame
from settings import *

class Transition:
    def __init__(self, reset, player):
        # setup
        self.displaySurface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # overlay image
        self.transitionImage = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.speed = -2
        self.color = 255
        

    def play(self):
        #3) set speed to -2 at end of the transition

        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2

        self.transitionImage.fill((self.color, self.color, self.color))
        self.displaySurface.blit(self.transitionImage, (0,0), special_flags=pygame.BLEND_RGBA_MULT)