import pygame
from pygame.locals import *
import random
import os

# ===================== CONSTANTS =====================
SCREEN_SIZE = 600
BLOCK_SIZE = 20
UI_HEIGHT = 50   # bottom panel height

GRID_WIDTH = SCREEN_SIZE // BLOCK_SIZE
GRID_HEIGHT = (SCREEN_SIZE - UI_HEIGHT) // BLOCK_SIZE

DIFFICULTY = {
    "Easy": 160,
    "Medium": 120,
    "Hard": 80,
    "Hardcore": 50
}

HIGH_SCORE_FILE = "highscore.txt"

# COLORS
WHITE = (255, 255, 255)
GRAY = (190, 190, 190)
DARK = (20, 20, 20)
RED = (255, 80, 80)
GREEN = (0, 220, 0)
YELLOW = (255, 255, 0)

# ===================== GAME CLASS =====================
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake & Apple")

        self.font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 44)

        # Background
        self.background = pygame.image.load("Resources/background.jpg").convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_SIZE, SCREEN_SIZE)
        )

        # Audio
        self.muted = False
        pygame.mixer.music.load("Resources/BGM.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.eat_sound = pygame.mixer.Sound("Resources/Eat.mp3")
        self.crash_sound = pygame.mixer.Sound("Resources/Crash.mp3")

        # Difficulty
        self.level_names = list(DIFFICULTY.keys())
        self.level_index = 1
        self.speed = DIFFICULTY[self.level_names[self.level_index]]

        self.high_score = self.load_high_score()
        self.show_start_screen = True

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
    def draw_bottom_panel(self):
        panel = pygame.Surface((SCREEN_SIZE, UI_HEIGHT))
        panel.fill(DARK)
        self.surface.blit(panel, (0, SCREEN_SIZE - UI_HEIGHT))

    def draw_ui(self):
        score = self.snake.length - 3
        level = self.level_names[self.level_index]

        texts = [
            f"Score: {score}",
            f"High: {self.high_score}",
            f"Level: {level}",
            "P:Pause  R:Restart  M:Mute  1-4:Level"
        ]

        x_positions = [10, 140, 280, 10]

        for i, text in enumerate(texts):
            y = SCREEN_SIZE - UI_HEIGHT + (5 if i < 3 else 28)
            self.surface.blit(
                self.font.render(text, True, WHITE if i < 3 else GRAY),
                (x_positions[i], y)
            )

    def start_screen(self):
        self.surface.blit(self.background, (0, 0))
        title = self.big_font.render("SNAKE & APPLE", True, GREEN)
        info = self.font.render("Press ENTER to Start", True, WHITE)
        hint = self.font.render("1-4 Difficulty | M Mute | P Pause", True, GRAY)

        self.surface.blit(title, title.get_rect(center=(SCREEN_SIZE//2, 240)))
        self.surface.blit(info, info.get_rect(center=(SCREEN_SIZE//2, 300)))
        self.surface.blit(hint, hint.get_rect(center=(SCREEN_SIZE//2, 340)))
        pygame.display.flip()

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))

        text = self.big_font.render("PAUSED", True, YELLOW)
        hint = self.font.render("Press P to Resume", True, GRAY)

        self.surface.blit(text, text.get_rect(center=(SCREEN_SIZE//2, 260)))
        self.surface.blit(hint, hint.get_rect(center=(SCREEN_SIZE//2, 300)))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))

        title = self.big_font.render("GAME OVER", True, RED)
        score = self.font.render(f"Score: {self.snake.length - 3}", True, WHITE)
        restart = self.font.render("R - Restart | ESC - Quit", True, GRAY)

        self.surface.blit(title, title.get_rect(center=(SCREEN_SIZE//2, 250)))
        self.surface.blit(score, score.get_rect(center=(SCREEN_SIZE//2, 300)))
        self.surface.blit(restart, restart.get_rect(center=(SCREEN_SIZE//2, 340)))

    # ================= LOGIC =================
    def wall_collision(self):
        x, y = self.snake.x[0], self.snake.y[0]
        return x < 0 or x >= SCREEN_SIZE or y < 0 or y >= SCREEN_SIZE - UI_HEIGHT

    def update_high_score(self):
        score = self.snake.length - 3
        if score > self.high_score:
            self.high_score = score
            self.save_high_score()

    # ================= MAIN LOOP =================
    def run(self):
        running = True
        while running:

            if self.show_start_screen:
                self.start_screen()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        self.show_start_screen = False
                continue

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

                    if event.key in [K_1, K_2, K_3, K_4]:
                        self.level_index = int(event.unicode) - 1
                        self.speed = DIFFICULTY[self.level_names[self.level_index]]

                    if event.key == K_m:
                        self.muted = not self.muted
                        vol = 0 if self.muted else 0.5
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

                if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
                    self.eat_sound.play()
                    self.snake.increase_length()
                    self.apple.move()

                if self.wall_collision():
                    self.crash_sound.play()
                    self.game_over = True
                    self.update_high_score()

                for i in range(1, self.snake.length):
                    if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                        self.crash_sound.play()
                        self.game_over = True
                        self.update_high_score()

            self.surface.blit(self.background, (0, 0))
            self.snake.draw(self.surface)
            self.apple.draw(self.surface)

            self.draw_bottom_panel()
            self.draw_ui()

            if self.paused:
                self.draw_pause()
            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            pygame.time.delay(self.speed)

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
        self.x = random.randint(0, GRID_WIDTH - 1) * BLOCK_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * BLOCK_SIZE

# ===================== SNAKE =====================
class Snake:
    def __init__(self, length):
        self.length = length
        self.image = pygame.image.load("Resources/block.jpg").convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.x = [300 - i * BLOCK_SIZE for i in range(length)]
        self.y = [300] * length
        self.direction = "RIGHT"

    def draw(self, surface):
        for i in range(self.length):
            surface.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def move_up(self):
        if self.direction != "DOWN":
            self.direction = "UP"

    def move_down(self):
        if self.direction != "UP":
            self.direction = "DOWN"

    def move_left(self):
        if self.direction != "RIGHT":
            self.direction = "LEFT"

    def move_right(self):
        if self.direction != "LEFT":
            self.direction = "RIGHT"

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
