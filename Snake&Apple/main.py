import pygame
from pygame.locals import *
import random

# ===================== CONSTANTS =====================
SCREEN_SIZE = 700
BLOCK_SIZE = 20
UI_HEIGHT = 40

GRID_WIDTH = SCREEN_SIZE // BLOCK_SIZE
GRID_HEIGHT = (SCREEN_SIZE - UI_HEIGHT) // BLOCK_SIZE

GAME_SPEED = 100

# ===================== GAME CLASS =====================
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake & Apple")

        self.font = pygame.font.SysFont("arial", 30)

        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2

    def score_display(self):
        score = self.font.render(
            f"Score: {self.snake.length - 3}",
            True,
            (255, 255, 255)
        )
        self.surface.blit(score, (10, 5))

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

            # Move snake
            self.snake.walk()

            # Check apple collision
            if self.is_collision(
                self.snake.x[0], self.snake.y[0],
                self.apple.x, self.apple.y
            ):
                self.snake.increase_length()
                self.apple.move()

            # Draw everything
            self.surface.fill((0, 0, 0))
            self.snake.draw()
            self.apple.draw()
            self.score_display()
            pygame.display.flip()

            pygame.time.delay(GAME_SPEED)

        pygame.quit()

# ===================== APPLE CLASS =====================
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("./Resources/apple.jpg").convert()
        self.image = pygame.transform.scale(
            self.image, (BLOCK_SIZE, BLOCK_SIZE)
        )
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, GRID_WIDTH - 1) * BLOCK_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * BLOCK_SIZE + UI_HEIGHT

# ===================== SNAKE CLASS =====================
class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length

        self.original_block = pygame.image.load("./Resources/block.jpg").convert()
        self.original_block = pygame.transform.scale(
            self.original_block, (BLOCK_SIZE, BLOCK_SIZE)
        )
        self.block = self.original_block

        self.x = [300 - i * BLOCK_SIZE for i in range(length)]
        self.y = [300] * length

        self.direction = "RIGHT"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def move_up(self):
        if self.direction != "DOWN":
            self.direction = "UP"
            self.block = pygame.transform.rotate(self.original_block, 90)

    def move_down(self):
        if self.direction != "UP":
            self.direction = "DOWN"
            self.block = pygame.transform.rotate(self.original_block, -90)

    def move_left(self):
        if self.direction != "RIGHT":
            self.direction = "LEFT"
            self.block = pygame.transform.rotate(self.original_block, 180)

    def move_right(self):
        if self.direction != "LEFT":
            self.direction = "RIGHT"
            self.block = self.original_block

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "UP":
            self.y[0] -= BLOCK_SIZE
        elif self.direction == "DOWN":
            self.y[0] += BLOCK_SIZE
        elif self.direction == "LEFT":
            self.x[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            self.x[0] += BLOCK_SIZE

# ===================== MAIN =====================
if __name__ == "__main__":
    game = Game()
    game.run()
