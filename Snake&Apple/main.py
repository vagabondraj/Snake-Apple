import pygame
from pygame.locals import *


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Snake & Apple Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen with black
        pygame.display.flip()

    pygame.quit()