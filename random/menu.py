# Imports
import pygame, sys
from pygame.locals import *

# Defining Pygame Window
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Full Screen Method")
screen = pygame.display.set_mode((500,500), 0, 32)

font = pygame.font.SysFont(None, 20)

# Functions
def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def main_menu():
    click = False
    while True:
        screen.fill((0,0,0))
        draw_text('main menu', font, (255,255,255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        pygame.draw.rect(screen, (255,0,0), button_1)
        pygame.draw.rect(screen, (255,0,0), button_2)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        mainClock.tick(60)

def game():
    running = True
    while running:
        screen.fill((0,0,0))
        draw_text('GAME', font, (255,255,255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)

def options():
    running = True
    while running:
        screen.fill((0,0,0))
        draw_text('OPTIONS', font, (255,255,255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)
     
main_menu()

