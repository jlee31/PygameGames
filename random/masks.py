import sys, pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('learning masks')

screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

img1 = pygame.image.load('hood.png')
img2 = pygame.transform.scale(img1, (150, 150))
img1Loc = (50,50)
img2.set_colorkey((247,247,247))

# masks
mask = pygame.mask.from_surface(img2)
mask2 = pygame.mask.from_surface(img2)
showMask = False

while True:
    mx, my = pygame.mouse.get_pos()
    screen.fill((247,247,247))
    if not showMask:
        screen.blit(img2, img1Loc)
        screen.blit(img2, (mx - img2.width // 2, my - img2.height // 2))
    else:
        screen.blit(mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,255)), img1Loc)
        screen.blit(mask2.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,255)), (mx - img2.width // 2, my - img2.height // 2))
        overlapMask = mask.overlap_mask(mask2, ((mx - img2.width // 2) - img1Loc[0], (my - img2.height // 2) - img1Loc[1]))
        screen.blit(overlapMask.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,0,0,255)), img1Loc)
        OFFSET = ((mx - img2.width // 2) - img1Loc[0], (my - img2.height // 2) - img1Loc[1])
        overlapMask = mask.overlap_mask(mask2, OFFSET)
        overlapCentroid = overlapMask.centroid()
        if overlapCentroid:
            pos = (overlapCentroid[0] + img1Loc[0], overlapCentroid[1] + img1Loc[1])
            pygame.draw.circle(screen, (0, 200, 255), pos, 10, 3)
            pygame.draw.circle(screen, (0, 200, 255), pos, 3)
        print(overlapMask.count(), mask.overlap_area(mask2, OFFSET), mask.overlap(mask, OFFSET))
 
 # Events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_m:
                showMask = not showMask

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()