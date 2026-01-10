import pygame
from pygame.locals import *
import random
import os

# ===================== CONSTANTS =====================
SCREEN_SIZE = 600
BLOCK_SIZE = 20
UI_HEIGHT = 40

GRID_WIDTH = SCREEN_SIZE // BLOCK_SIZE
GRID_HEIGHT = (SCREEN_SIZE - UI_HEIGHT) // BLOCK_SIZE

GAME_SPEED = 100
HIGH_SCORE_FILE = "highscore.txt"

# ===================== GAME CLASS =====================
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake & Apple")

        self.font = pygame.font.SysFont("arial", 28)
        self.game_over_font = pygame.font.SysFont("arial", 48)

        self.high_score = self.load_high_score()
        self.reset_game()

    # ---------- High Score ----------
    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(self.high_score))

    # ---------- Game Reset ----------
    def reset_game(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.paused = False
        self.game_over_flag = False

    # ---------- UI ----------
    def score_display(self):
        current_score = self.snake.length - 3

        score_text = self.font.render(
            f"Score: {current_score}", True, (255, 255, 255)
        )
        high_score_text = self.font.render(
            f"High Score: {self.high_score}", True, (255, 215, 0)
        )

        self.surface.blit(score_text, (10, 5))
        self.surface.blit(high_score_text, (10, 22))

    def pause_display(self):
        text = self.game_over_font.render("PAUSED", True, (255, 255, 0))
        rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
        self.surface.blit(text, rect)

    def game_over_screen(self):
        title = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
        score = self.font.render(
            f"Your Score: {self.snake.length - 3}", True, (255, 255, 255)
        )
        high = self.font.render(
            f"High Score: {self.high_score}", True, (255, 215, 0)
        )
        restart = self.font.render(
            "Press R to Restart | ESC to Quit", True, (200, 200, 200)
        )

        self.surface.blit(title, title.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2 - 50)))
        self.surface.blit(score, score.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2)))
        self.surface.blit(high, high.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2 + 30)))
        self.surface.blit(restart, restart.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2 + 65)))

    # ---------- Collision ----------
    def check_wall_collision(self):
        x, y = self.snake.x[0], self.snake.y[0]
        return (
            x < 0 or x >= SCREEN_SIZE or
            y < UI_HEIGHT or y >= SCREEN_SIZE
        )

    def update_high_score(self):
        current_score = self.snake.length - 3
        if current_score > self.high_score:
            self.high_score = current_score
            self.save_high_score()

    # ---------- Main Loop ----------
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if self.game_over_flag:
                        if event.key == K_r:
                            self.reset_game()
                        continue

                    if event.key == K_p:
                        self.paused = not self.paused

                    if not self.paused:
                        if event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                        elif event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()

            if not self.paused and not self.game_over_flag:
                self.snake.walk()

                # Apple collision
                if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
                    self.snake.increase_length()
                    self.apple.move()

                # Wall collision
                if self.check_wall_collision():
                    self.game_over_flag = True
                    self.update_high_score()

                # Self collision
                for i in range(1, self.snake.length):
                    if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                        self.game_over_flag = True
                        self.update_high_score()

            # DRAW
            self.surface.fill((0, 0, 0))
            self.snake.draw()
            self.apple.draw()
            self.score_display()

            if self.paused and not self.game_over_flag:
                self.pause_display()

            if self.game_over_flag:
                self.game_over_screen()

            pygame.display.flip()
            pygame.time.delay(GAME_SPEED)

        pygame.quit()

# ===================== APPLE CLASS =====================
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("./Resources/apple.jpg").convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
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
        self.original_block = pygame.transform.scale(self.original_block, (BLOCK_SIZE, BLOCK_SIZE))
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
