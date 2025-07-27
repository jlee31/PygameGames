import pygame
from settings import *
from myTimer import Timer

class Menu:
    def __init__(self, player, toggleMenu):
        
        # General Setup

        self.player = player
        self.toggleMenu = toggleMenu
        self.displaySurface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        # Options

        self.width = 400
        self.space = 10
        self.padding = 8

        # Menu Entries
        print(f"Player itemInventory: {self.player.itemInventory}")
        print(f"Player seedInventory: {self.player.seedInventory}")
        self.options = list(self.player.itemInventory.keys()) + list(self.player.seedInventory.keys())
        print(f"Created options: {self.options}")
        self.sellBorder = len(self.player.itemInventory) - 1     
        self.setup()

        # Movement
        self.index = 0
        self.timer = Timer(200) # duration = 200 ms


    def setup(self):
         # create text surface
        self.textSurfs = []
        self.totalHeight = 0

        print(f"Setup - options: {self.options}")
        print(f"Setup - number of options: {len(self.options)}")

        for item in self.options:
              textSurf = self.font.render(item, False, 'black')
              self.textSurfs.append(textSurf)
              self.totalHeight += textSurf.get_height() + (self.padding * 2)
              print(f"Setup - item: {item}, text height: {textSurf.get_height()}, totalHeight so far: {self.totalHeight}")

        self.totalHeight += (len(self.textSurfs) - 1) * self.space
        self.menuTop = (SCREEN_HEIGHT / 2) - (self.totalHeight / 2)
        self.menuSide = (SCREEN_WIDTH / 2) - (self.width / 2)
        
        print(f"Setup - SCREEN_HEIGHT: {SCREEN_HEIGHT}, SCREEN_WIDTH: {SCREEN_WIDTH}")
        print(f"Setup - menuTop calculation: ({SCREEN_HEIGHT} / 2) - ({self.totalHeight} / 2) = {self.menuTop}")
        print(f"Setup - menuSide calculation: ({SCREEN_WIDTH} / 2) - ({self.width} / 2) = {self.menuSide}")
        
        self.boundingBox = pygame.Rect(left=self.menuSide, top=self.menuTop, width=self.width, height=self.totalHeight)
        self.boundbox2 = pygame.Rect(440, 188,self.width, self.totalHeight)


        print(f"Setup - final totalHeight: {self.totalHeight}")
        print(f"Setup - boundingBox: {self.boundbox2}")

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
                self.toggleMenu()

        if not self.timer.active: 
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
                if self.index < 0:
                    self.index = len(self.options) - 1
                
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
                if self.index >  len(self.options) - 1:
                    self.index = 0

    def displayMoney(self):
        textSurf = self.font.render(f'${self.player.money}', False, 'Black')
        textRect = textSurf.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))
        pygame.draw.rect(self.displaySurface, 'White', textRect.inflate(10,10), 0, 6)
        self.displaySurface.blit(textSurf, textRect)

    def showEntry(self, textSurf, amount, top, selected):
        # background
        bgRect = pygame.Rect(self.boundbox2.left, top, self.width, textSurf.get_height() + self.padding * 2)
        pygame.draw.rect(self.displaySurface, 'White', bgRect, 0, 4)

        # text
        textRect = textSurf.get_rect(midleft = (self.boundbox2.left + 20, bgRect.centery))
        self.displaySurface.blit(textSurf, textRect)

        # show amount
        amountSurf = self.font.render(str(amount), False, 'Black')
        amountRect = amountSurf.get_rect(midright = (self.boundbox2.right - 20, bgRect.centery))
        self.displaySurface.blit(amountSurf, amountRect)

        # selected
        if selected:
            pygame.draw.rect(self.displaySurface, 'black', bgRect, 4, 4)
        

    def update(self):
        self.input()
        self.displayMoney()
        # print(f"Menu update called - boundingBox: {self.boundbox2}")
        # pygame.draw.rect(self.displaySurface, 'red', self.boundbox2)
        amountList =  list(self.player.itemInventory.values()) + list(self.player.seedInventory.values())

        for textIndex, textSurface in enumerate(self.textSurfs):
            top = self.boundbox2.top + textIndex * (textSurface.get_height() + self.padding * 2 + self.space)
            amount = amountList[textIndex]
            self.showEntry(textSurface, amount, top, self.index == textIndex)
            print(self.index)

            # self.displaySurface.blit(textSurface, (100, index * 50))
             