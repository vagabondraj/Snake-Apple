import pygame
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Snake & Apple")
        self.snake = Snake(self.surface)
        self.snake.draw()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            pygame.time.delay(100)

        pygame.quit()


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

        # Load and scale base image
        self.original_block = pygame.image.load("./Resources/block.jpg").convert()
        self.original_block = pygame.transform.scale(self.original_block, (20, 20))

        # Current displayed block
        self.block = self.original_block

        self.x = 300
        self.y = 300
        self.direction = "RIGHT"

    def draw(self):
        self.parent_screen.fill((0, 0, 0))
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move_up(self):
        self.direction = "UP"
        self.block = pygame.transform.rotate(self.original_block, 90)
        self.y -= 20
        self.draw()

    def move_down(self):
        self.direction = "DOWN"
        self.block = pygame.transform.rotate(self.original_block, -90)
        self.y += 20
        self.draw()

    def move_left(self):
        self.direction = "LEFT"
        self.block = pygame.transform.rotate(self.original_block, 180)
        self.x -= 20
        self.draw()

    def move_right(self):
        self.direction = "RIGHT"
        self.block = self.original_block
        self.x += 20
        self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
