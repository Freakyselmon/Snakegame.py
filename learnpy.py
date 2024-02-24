import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10  # Increased speed

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return True  # Game over
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return False

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Draw grid function
def draw_grid(surface):
    # Draw outer border
    pygame.draw.rect(surface, WHITE, (0, 0, WIDTH, HEIGHT), GRID_SIZE)

# Show game over function
def show_game_over(surface, score):
    font = pygame.font.Font(None, 36)
    game_over_text = font.render(f"Game Over - Score: {score}", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(game_over_text, text_rect)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    # If game over, reset the game on key press
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                else:
                    if event.key == pygame.K_UP:
                        if snake.direction != DOWN:
                            snake.direction = UP
                    elif event.key == pygame.K_DOWN:
                        if snake.direction != UP:
                            snake.direction = DOWN
                    elif event.key == pygame.K_LEFT:
                        if snake.direction != RIGHT:
                            snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT:
                        if snake.direction != LEFT:
                            snake.direction = RIGHT

        if not game_over:
            game_over = snake.update()

            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

        surface.fill((0, 0, 0))
        draw_grid(surface)
        snake.render(surface)
        food.render(surface)

        if game_over:
            show_game_over(surface, snake.score)

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
def show_game_over(surface, score):
            font = pygame.font.Font(None, 36)
            game_over_text = font.render(f"Game Over - Score: {00}", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 10, HEIGHT // 10))
            surface.blit(game_over_text, text_rect)


if __name__ == "__main__":
    main()
