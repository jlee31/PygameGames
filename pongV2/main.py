from settings import *
from sprites import Player, Ball
import pygame

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("PONG V2")
        self.clock = pygame.time.Clock()
        self.running = True

        # sprites

        self.allSprites = pygame.sprite.Group()
        self.paddleSprite = pygame.sprite.Group() # used for collisions between the ball and the paddles
        self.player = Player((self.allSprites, self.paddleSprite), screenWidth-50)
        self.ball = Ball(self.allSprites, self.paddleSprite)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # Delta time in seconds
            self.screen.fill(colours['bg'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.allSprites.update(dt)
            self.allSprites.draw(self.screen)

            pygame.display.flip()
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()