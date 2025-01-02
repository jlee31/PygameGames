from settings import *
from sprites import Player, Ball, Opponent
from groups import AllSprites
import pygame
import json

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("PONG V2")
        self.clock = pygame.time.Clock()
        self.running = True


        # sprites

        self.allSprites = AllSprites()
        self.paddleSprite = pygame.sprite.Group() # used for collisions between the ball and the paddles
        self.player = Player((self.allSprites, self.paddleSprite))
        self.ball = Ball(self.allSprites, self.paddleSprite, self.updateScore)
        Opponent((self.allSprites, self.paddleSprite), self.ball)

        # score
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0, 'opponent': 0} # making a new dict if there is no original dict

        self.font = pygame.font.Font(None, 150)

    def displayScore(self):
        # player surf
        playerScoreSurf = self.font.render(str(self.score['player']), True, (255,255,255))
        playerScoreRect = playerScoreSurf.get_frect(center = (screenWidth/2 + 100, screenHeight / 2))
        self.screen.blit(playerScoreSurf, playerScoreRect)
        # opponent surf
        opponentScoreSurf = self.font.render(str(self.score['opponent']), True, (255,255,255))
        opponentScoreRect = opponentScoreSurf.get_frect(center = (screenWidth/2 - 100, screenHeight / 2))
        self.screen.blit(opponentScoreSurf, opponentScoreRect)
        # line
        pygame.draw.line(self.screen, (255,255,255), (screenWidth/2, 0), (screenWidth/2, screenHeight), 5)
        # title
        titleSurf = self.font.render("PONG YEAH", True, (255,255,255))
        titleRect = titleSurf.get_frect(center = (screenWidth/2, 100))
        self.screen.blit(titleSurf, titleRect)

    def updateScore(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1 

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # Delta time in seconds
            self.screen.fill(colours['bg'])
            self.displayScore()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open(join('data', 'score.txt'), 'w') as score_file: # how to save files
                        json.dump(self.score, score_file)

            # update 
            self.allSprites.update(dt)

            # draw 
            self.screen.fill(colours['bg'])
            self.displayScore()
            self.allSprites.draw()
            pygame.display.update()

        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()