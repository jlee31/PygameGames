# Example file showing a basic pygame "game loop"
import pygame, sys, pymunk

def createApple(space, pos):
    body = pymunk.Body(1,100,body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body=body, radius=40)
    space.add(body, shape)
    return shape # pygame is used to visualize the shape

def drawApples(apples):
    for apple in apples:
        x = int(apple.body.position.x)
        y = int(apple.body.position.y)
        pygame.draw.circle(screen, (0,0,0), (x,y), int(apple.radius))

def createStaticBall(space): #making a static body
    body = pymunk.Body(body_type = pymunk.Body.STATIC) # no mass or inertia
    body.position = (300, 300)
    shape = pymunk.Circle(body=body, radius=30)
    space.add(body, shape)
    return shape

def drawBalls(balls):
    for ball in balls:
        x = int(ball.body.position.x)
        y = int(ball.body.position.y)
        pygame.draw.circle(screen, (0,0,0), (x,y), int(ball.radius))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

# pymunk
space = pymunk.Space()
space.gravity = (0, 500)

apples = []
apples.append(createApple(space, (250, 0)))

balls = []
balls.append(createStaticBall(space))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            apples.append(createApple(space, event.pos))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((127,127,127))

    # RENDER YOUR GAME HERE
    drawApples(apples)
    drawBalls(balls)
    space.step(1/50)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()