import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import gfxdraw
import numpy as np

'''

    draw arc

    '''


RED = pygame.Color("red")
WHITE = pygame.Color("white")

# def draw_arc(surface, center, radius, start_angle, stop_angle, color):
#     x,y = center
#     start_angle = int(start_angle%360)
#     stop_angle = int(stop_angle%360)
#     if start_angle == stop_angle:
#         gfxdraw.circle(surface, x, y, radius, color)
#     else:
#         gfxdraw.arc(surface, x, y, radius, start_angle, stop_angle, color)


pygame.init()
screen = pygame.display.set_mode([500,500])
x,y = 250, 250
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0,0,0))

    #Arcs

    r1 = 25
    r2 = 50
    r3 = 75
    r4 = 100


    q1 = np.pi/4
    q2 = 3 * np.pi/4
    q3 = -3 * np.pi/4
    q4 = -np.pi/4
    pygame.draw.arc(screen, RED, [x-r1, y-r1, 2*r1, 2*r1], q1, 0, 3)
    pygame.draw.arc(screen, RED, [x-r2, y-r2, 2*r2, 2*r2], q2, 0, 3)
    pygame.draw.arc(screen, RED, [x-r3, y-r3, 2*r3, 2*r3], q3, 0, 3)
    pygame.draw.arc(screen, RED, [x-r4, y-r4, 2*r4, 2*r4], q4, 0, 3)

    # q1 = int(q1 * 180/np.pi)
    # q2 = int(q2 * 180/np.pi)
    # q3 = int(q3 * 180/np.pi)
    # q4 = int(q4 * 180/np.pi)
    # gfxdraw.arc(screen, x, y, r1, 0, q1, RED)
    # gfxdraw.arc(screen, x, y, r2, 0, q2, RED)
    # gfxdraw.arc(screen, x, y, r3, 0, q3, RED)
    # gfxdraw.arc(screen, x, y, r4, 0, q4, RED)

    # # Horizontal and vertical lines for comparison
    # pygame.draw.line(screen, RED, screen_rect.center, screen_rect.midright)
    # pygame.draw.line(screen, RED, screen_rect.center, screen_rect.midtop)
    # pygame.draw.line(screen, RED, screen_rect.topleft, screen_rect.bottomright)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
