from settings import *

class Timer():
    def __init__(self, duration, func = None, repeat = None, autostart = False):
        self.duration = duration
        self.startTime = 0
        self.active = False
        self.func = func
        self.repeat = repeat

        if autostart:
            self.activate() 

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.startTime = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.startTime = 0
        if self.repeat:
            self.activate() # would repeat the code

    def update(self):
        if pygame.time.get_ticks() - self.startTime >= self.duration:
            if self.func and self.startTime != 0:
                self.func()
            self.deactivate()

# Basic Timer Template