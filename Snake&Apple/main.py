import pygame
from pygame.locals import *


def draw_block():
    surface.fill((0, 0, 0))
    surface.blit(block, (block_x, block_y))
    pygame.display.flip()

if __name__ == "__main__":
    pygame.init()

    surface = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Snake & Apple")
    surface.fill((0, 0, 0))

    block = pygame.image.load("./Resources/block.jpg").convert()
    block_x, block_y = 300, 300
    block = pygame.transform.scale(block, (40, 40))
    surface.blit(block, (block_x, block_y))

    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_UP:
                    block_y -= 20
                    draw_block()
                if event.key == K_DOWN:
                    block_y += 20
                    draw_block()
                if event.key == K_LEFT:
                    block_x -= 20
                    draw_block()
                if event.key == K_RIGHT:
                    block_x += 20
                    draw_block()
            elif event.type == QUIT:
                running = False