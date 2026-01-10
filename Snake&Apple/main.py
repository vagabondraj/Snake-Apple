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
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake & Apple")

        # Fonts
        self.font = pygame.font.SysFont("arial", 26)
        self.big_font = pygame.font.SysFont("arial", 48)

        # Background
        self.background = pygame.image.load("Resources/background.jpg").convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_SIZE, SCREEN_SIZE)
        )

        # Audio
        self.volume = 0.5
        self.muted = False

        pygame.mixer.music.load("Resources/BGM.mp3")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)   # play once, loop forever

        self.eat_sound = pygame.mixer.Sound("Resources/Eat.mp3")
        self.crash_sound = pygame.mixer.Sound("Resources/Crash.mp3")
        self.eat_sound.set_volume(self.volume)
        self.crash_sound.set_volume(self.volume)

        # Game state
        self.high_score = self.load_high_score()
        self.reset_game()

    # ================= HIGH SCORE =================
    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                return int(open(HIGH_SCORE_FILE).read())
            except:
                return 0
        return 0

    def save_high_score(self):
        open(HIGH_SCORE_FILE, "w").write(str(self.high_score))

    # ================= RESET =================
    def reset_game(self):
        self.snake = Snake(3)
        self.apple = Apple()
        self.paused = False
        self.game_over = False

    # ================= UI =================
    def draw_ui(self):
        score = self.snake.length - 3

        s1 = self.font.render(f"Score: {score}", True, (255, 255, 255))
        s2 = self.font.render(f"High: {self.high_score}", True, (255, 215, 0))
        s3 = self.font.render(f"Vol: {int(self.volume*100)}%", True, (200, 200, 200))

        self.surface.blit(s1, (10, 5))
        self.surface.blit(s2, (10, 25))
        self.surface.blit(s3, (540, 5))

    def draw_pause(self):
        t = self.big_font.render("PAUSED", True, (255, 255, 0))
        self.surface.blit(t, t.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2)))

    def draw_game_over(self):
        t1 = self.big_font.render("GAME OVER", True, (255, 0, 0))
        t2 = self.font.render("R - Restart | ESC - Quit", True, (220, 220, 220))

        self.surface.blit(t1, t1.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2 - 25)))
        self.surface.blit(t2, t2.get_rect(center=(SCREEN_SIZE//2, SCREEN_SIZE//2 + 25)))

    # ================= LOGIC =================
    def wall_collision(self):
        x, y = self.snake.x[0], self.snake.y[0]
        return x < 0 or x >= SCREEN_SIZE or y < UI_HEIGHT or y >= SCREEN_SIZE

    def update_high_score(self):
        score = self.snake.length - 3
        if score > self.high_score:
            self.high_score = score
            self.save_high_score()

    # ================= MAIN LOOP =================
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if self.game_over and event.key == K_r:
                        self.reset_game()

                    if event.key == K_p:
                        self.paused = not self.paused

                    if event.key == K_m:
                        self.muted = not self.muted
                        vol = 0 if self.muted else self.volume
                        pygame.mixer.music.set_volume(vol)
                        self.eat_sound.set_volume(vol)
                        self.crash_sound.set_volume(vol)

                    if event.key == K_LEFTBRACKET:
                        self.volume = max(0, self.volume - 0.05)
                    if event.key == K_RIGHTBRACKET:
                        self.volume = min(1, self.volume + 0.05)

                    vol = 0 if self.muted else self.volume
                    pygame.mixer.music.set_volume(vol)
                    self.eat_sound.set_volume(vol)
                    self.crash_sound.set_volume(vol)

                    if not self.paused and not self.game_over:
                        if event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                        elif event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()

            if not self.paused and not self.game_over:
                self.snake.walk()

                # Eat apple (NO BGM restart)
                if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
                    self.eat_sound.play()
                    self.snake.increase_length()
                    self.apple.move()

                # Wall collision
                if self.wall_collision():
                    self.crash_sound.play()
                    self.game_over = True
                    self.update_high_score()

                # Self collision
                for i in range(1, self.snake.length):
                    if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                        self.crash_sound.play()
                        self.game_over = True
                        self.update_high_score()

            # DRAW
            self.surface.blit(self.background, (0, 0))
            self.snake.draw(self.surface)
            self.apple.draw(self.surface)
            self.draw_ui()

            if self.paused:
                self.draw_pause()
            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            pygame.time.delay(GAME_SPEED)

        pygame.quit()

# ===================== APPLE =====================
class Apple:
    def __init__(self):
        self.image = pygame.image.load("Resources/apple.jpg").convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.move()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, GRID_WIDTH-1) * BLOCK_SIZE
        self.y = random.randint(0, GRID_HEIGHT-1) * BLOCK_SIZE + UI_HEIGHT

# ===================== SNAKE =====================
class Snake:
    def __init__(self, length):
        self.length = length
        self.image = pygame.image.load("Resources/block.jpg").convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.x = [300 - i*BLOCK_SIZE for i in range(length)]
        self.y = [300]*length
        self.direction = "RIGHT"

    def draw(self, surface):
        for i in range(self.length):
            surface.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def move_up(self):
        if self.direction != "DOWN": self.direction = "UP"

    def move_down(self):
        if self.direction != "UP": self.direction = "DOWN"

    def move_left(self):
        if self.direction != "RIGHT": self.direction = "LEFT"

    def move_right(self):
        if self.direction != "LEFT": self.direction = "RIGHT"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "UP": self.y[0] -= BLOCK_SIZE
        if self.direction == "DOWN": self.y[0] += BLOCK_SIZE
        if self.direction == "LEFT": self.x[0] -= BLOCK_SIZE
        if self.direction == "RIGHT": self.x[0] += BLOCK_SIZE

# ===================== MAIN =====================
if __name__ == "__main__":
    game = Game()
    game.run()
