
import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # Adjust snake speed as needed

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()

        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Initialize snake
        self.snake = [(5, 5)]
        self.snake_direction = RIGHT

        # Initialize food
        self.food = self.spawn_food()

        # Initialize score
        self.score = 0

        self.running = True

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != DOWN:
                    self.snake_direction = UP
                elif event.key == pygame.K_DOWN and self.snake_direction != UP:
                    self.snake_direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake_direction != RIGHT:
                    self.snake_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake_direction != LEFT:
                    self.snake_direction = RIGHT

    def move_snake(self):
        x, y = self.snake[0]
        new_head = (x + self.snake_direction[0], y + self.snake_direction[1])

        # Check for collision with food
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        # Check for collision with walls or self
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
            or new_head in self.snake
        ):
            self.running = False

        self.snake.insert(0, new_head)

    def draw_game(self):
        # Draw background
        self.screen.fill(BLACK)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(
                self.screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

        # Draw food
        pygame.draw.rect(
            self.screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.move_snake()
            self.draw_game()
            self.clock.tick(SNAKE_SPEED)

        self.game_over()

    def game_over(self):
        # Display game over screen
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, RED)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()

        # Wait for a few seconds before quitting
        pygame.time.delay(2000)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()