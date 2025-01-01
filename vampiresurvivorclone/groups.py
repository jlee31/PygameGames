from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface() # getting the display surface
        self.offset = pygame.Vector2()
        
    
    def draw(self, targetPos):
        self.offset.x = -targetPos[0] + screenWidth // 2
        self.offset.y = -targetPos[1] + screenHeight // 2
        
        groundSprites = [sprite for sprite in self if hasattr(sprite, 'ground')] 
        objectSprites = [sprite for sprite in self if not hasattr(sprite, 'ground')] 

        for layer in [groundSprites, objectSprites]:
            for sprite in sorted(layer, key = lambda sprite : sprite.rect.centery):
                self.displaySurface.blit(sprite.image, sprite.rect.topleft + self.offset) # now you can create an offset
                                                                            # this is the offset for the map
