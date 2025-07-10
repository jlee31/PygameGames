import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        
        # General Setup
        self.displaySurface = pygame.display.get_surface()
        self.player = player

        # Importing 
        overlayPath = '../graphics/overlay/'
        self.tool_surfaces = {tool: pygame.image.load(f'{overlayPath}{tool}.png').convert_alpha() for tool in player.tools}
        self.seed_surfaces = {seed: pygame.image.load(f'{overlayPath}{seed}.png').convert_alpha() for seed in player.seeds}

    def display(self):

        # show tools
        toolSurf = self.tool_surfaces[self.player.selectedTool]
        toolRect = toolSurf.get_rect(midbottom=(OVERLAY_POSITIONS['tool']))
        self.displaySurface.blit(toolSurf, toolRect)


        # show seeds
        seedSurf = self.seed_surfaces[self.player.selectedSeed]
        seedRect = toolSurf.get_rect(midbottom=(OVERLAY_POSITIONS['seed']))
        self.displaySurface.blit(seedSurf, seedRect)