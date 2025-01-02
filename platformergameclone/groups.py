from settings import * 

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos): # this is the camera
        self.offset.x = - (target_pos[0] - screenWidth / 2) # horizontal value of player - half the screen
        self.offset.y = - (target_pos[1] - screenHeight / 2) # vertical value of player - half the screen

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset) # camera complete