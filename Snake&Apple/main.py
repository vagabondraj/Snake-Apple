import pygame
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Snake & Apple")

        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
    
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.snake.draw()
        pygame.display.flip()

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

            self.snake.walk()

            # DRAW ORDER MATTERS
            self.surface.fill((0, 0, 0))
            self.snake.draw()
            self.apple.draw()

            pygame.display.flip()
            pygame.time.delay(150)

        pygame.quit()


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("./Resources/apple.jpg").convert()
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.x = 100
        self.y = 100

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length

        self.original_block = pygame.image.load("./Resources/block.jpg").convert()
        self.original_block = pygame.transform.scale(self.original_block, (20, 20))
        self.block = self.original_block

        self.x = [300 - i * 20 for i in range(length)]
        self.y = [300] * length

        self.direction = "RIGHT"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_up(self):
        if self.direction == "DOWN":
            return
        self.direction = "UP"
        self.block = pygame.transform.rotate(self.original_block, 90)

    def move_down(self):
        if self.direction == "UP":
            return
        self.direction = "DOWN"
        self.block = pygame.transform.rotate(self.original_block, -90)

    def move_left(self):
        if self.direction == "RIGHT":
            return
        self.direction = "LEFT"
        self.block = pygame.transform.rotate(self.original_block, 180)

    def move_right(self):
        if self.direction == "LEFT":
            return
        self.direction = "RIGHT"
        self.block = self.original_block

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "UP":
            self.y[0] -= 20
        elif self.direction == "DOWN":
            self.y[0] += 20
        elif self.direction == "LEFT":
            self.x[0] -= 20
        elif self.direction == "RIGHT":
            self.x[0] += 20


if __name__ == "__main__":
    game = Game()
    game.run()
