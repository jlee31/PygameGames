import pygame

class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.function = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True;
        self.start_time = pygame.time.get_ticks()


    def deactivate(self):
        self.start_time = 0
        self.active = False

    def update(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.start_time >= self.duration:
            self.deactivate()
            if self.function:
                self.function()