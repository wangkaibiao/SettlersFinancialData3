#-*-coding:utf8-*-
#qpy:pygame
"""
Pygame support is builtin from QPython >= 2.4.0
"""

import sys
import pygame
from pygame.locals import *

pygame.init()
# Resolution is ignored on Android
surface = pygame.display.set_mode((640, 480))
# Only one built in font is available on Android
myfont = pygame.font.SysFont("DejaVuSans", 64)
label = myfont.render("Hello, world!", 1, (255, 255, 255))
clock = pygame.time.Clock()

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
    # Framelimiter
    clock.tick(60)
    surface.fill((0, 0, 0))
    surface.blit(label, (0, 0))
    pygame.display.flip()
