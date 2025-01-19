import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10  # Increased speed

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)
SOFT_GRASS = (107, 142, 35)
DARK_GRASS = (85, 107, 47)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize mixer for sound
pygame.mixer.init()
# Load the background music
try:
    BACKGROUND_MUSIC_PATH = "/Users/shabbirshaikh/Downloads/retro-game-arcade-short-236130.mp3"  # Path to the uploaded music file
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.set_volume(0.1)  # Optional: Adjust the volume (range: 0.0 to 1.0)
except pygame.error as e:
    print(f"Error loading background music: {e}")
    sys.exit()

# Load the eating sound
try:
    EAT_SOUND = pygame.mixer.Sound("/Users/shabbirshaikh/Downloads/food_G1U6tlb.wav")
    EAT_SOUND.set_volume(0.5)  # Optional: Adjust the volume (range: 0.0 to 1.0)
except pygame.error as e:
    print(f"Error loading sound: {e}")
    sys.exit()

# Load the game over sound
try:
    GAME_OVER_SOUND = pygame.mixer.Sound("/Users/shabbirshaikh/Downloads/game-over-2-sound-effect-230463.mp3")
    GAME_OVER_SOUND.set_volume(0.5)  # Optional: Adjust the volume (range: 0.0 to 1.0)
except pygame.error as e:
    print(f"Error loading game over sound: {e}")
    sys.exit()


# File to store the highest score
HIGHSCORE_FILE = "highscore.txt"

# Function to load the highest score
def load_high_score():
    try:
        with open(HIGHSCORE_FILE, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to save the highest score
def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(score))

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
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
        for i, p in enumerate(self.positions):
            if i == 0:  # Render the triangular head
                x, y = p
                if self.direction == UP:
                    points = [(x + GRID_SIZE // 2, y),  # Top vertex
                              (x, y + GRID_SIZE),  # Bottom-left vertex
                              (x + GRID_SIZE, y + GRID_SIZE)]  # Bottom-right vertex
                    # Eye positions
                    eye1 = (x + GRID_SIZE // 3, y + GRID_SIZE // 2)
                    eye2 = (x + 2 * GRID_SIZE // 3, y + GRID_SIZE // 2)
                elif self.direction == DOWN:
                    points = [(x, y),  # Top-left vertex
                              (x + GRID_SIZE, y),  # Top-right vertex
                              (x + GRID_SIZE // 2, y + GRID_SIZE)]  # Bottom vertex
                    # Eye positions
                    eye1 = (x + GRID_SIZE // 3, y + GRID_SIZE // 2)
                    eye2 = (x + 2 * GRID_SIZE // 3, y + GRID_SIZE // 2)
                elif self.direction == LEFT:
                    points = [(x + GRID_SIZE, y),  # Top-right vertex
                              (x + GRID_SIZE, y + GRID_SIZE),  # Bottom-right vertex
                              (x, y + GRID_SIZE // 2)]  # Left vertex
                    # Eye positions
                    eye1 = (x + GRID_SIZE // 2, y + GRID_SIZE // 3)
                    eye2 = (x + GRID_SIZE // 2, y + 2 * GRID_SIZE // 3)
                elif self.direction == RIGHT:
                    points = [(x, y),  # Top-left vertex
                              (x, y + GRID_SIZE),  # Bottom-left vertex
                              (x + GRID_SIZE, y + GRID_SIZE // 2)]  # Right vertex
                    # Eye positions
                    eye1 = (x + GRID_SIZE // 2, y + GRID_SIZE // 3)
                    eye2 = (x + GRID_SIZE // 2, y + 2 * GRID_SIZE // 3)

                # Draw the triangular head
                pygame.draw.polygon(surface, RED, points)

                # Draw the eyes
                pygame.draw.circle(surface, BLACK, eye1, 3)  # Eye 1
                pygame.draw.circle(surface, BLACK, eye2, 3)  # Eye 2
            else:  # Render the body
                # Draw the main body segment
                rect = pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, DARK_RED, rect)

                # Add small black patches on the body
                patch_size = GRID_SIZE // 4  # Size of the patch
                patch_x = p[0] + random.randint(0, GRID_SIZE - patch_size)
                patch_y = p[1] + random.randint(0, GRID_SIZE - patch_size)
                pygame.draw.rect(surface, BLACK, (patch_x, patch_y, patch_size, patch_size))


# Food class
class Food:
    def __init__(self, image_path):
        self.scaling_factor = 2  # Scale the food 2x larger than GRID_SIZE
        self.image = pygame.image.load(image_path)  # Load the cherry image
        self.image = pygame.transform.scale(
            self.image,
            (GRID_SIZE * self.scaling_factor, GRID_SIZE * self.scaling_factor)
        )  # Scale it up
        self.randomize_position()

    def randomize_position(self):
        # Randomize the food position on the grid
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        # Adjust position for the scaled size
        adjusted_position = (
            self.position[0] - (GRID_SIZE * (self.scaling_factor - 1)) // 2,
            self.position[1] - (GRID_SIZE * (self.scaling_factor - 1)) // 2,
        )
        surface.blit(self.image, adjusted_position)  # Draw the image at its position


# Show game over function
def show_game_over(surface, score, highest_score):
    font = pygame.font.Font(pygame.font.match_font('bold'), 65)
    game_over_text = font.render(f"Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    high_score_text = font.render(f"Highest Score: {highest_score}", True, BLACK)
    restart_text = font.render("Click Replay to Play Again", True, WHITE)

    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height()))
    surface.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2))
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.6))

    # Draw replay button
    button_width, button_height = 150, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 1.1 - button_height
    pygame.draw.rect(surface, LIGHT_GREEN, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(surface, DARK_GREEN, (button_x, button_y, button_width, button_height), 3)
    button_font = pygame.font.Font(pygame.font.match_font('bold'), 40)
    button_text = button_font.render("Replay", True, BLACK)
    surface.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2,
                               button_y + button_height // 2 - button_text.get_height() // 2))
    return (button_x, button_y, button_width, button_height)

# Initialize the Pygame screen before loading images
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load the grass image and scale it to the screen size
GRASS_IMAGE_PATH = "/Users/shabbirshaikh/Downloads/green-grass-texture-vector-background-field-with-pattern-squares-surface-chess-soccer_390775-754 (1).png"  # Path to the uploaded grass image
GRASS_IMAGE = pygame.image.load(GRASS_IMAGE_PATH).convert()
GRASS_IMAGE = pygame.transform.scale(GRASS_IMAGE, (WIDTH, HEIGHT))

# Draw textured background using the grass image
def draw_textured_background(surface):
    surface.blit(GRASS_IMAGE, (0, 0))

# Load the game start sound
try:
    GAME_START_SOUND = pygame.mixer.Sound("/Users/shabbirshaikh/Downloads/gamestart-272829.mp3")
    GAME_START_SOUND.set_volume(0.5)  # Optional: Adjust the volume (range: 0.0 to 1.0)
except pygame.error as e:
    print(f"Error loading game start sound: {e}")
    sys.exit()

# Show start screen
def show_start_screen(surface):
    START_SCREEN_IMAGE_PATH = "/Users/shabbirshaikh/Downloads/pngtree-simple-yet-striking-background-template-design-featuring-solid-colors-and-a-vibrant-red-snake-vector-png-image_37155440.jpg"
    START_SCREEN_IMAGE = pygame.image.load(START_SCREEN_IMAGE_PATH).convert()
    START_SCREEN_IMAGE = pygame.transform.scale(START_SCREEN_IMAGE, (WIDTH, HEIGHT))

    surface.blit(START_SCREEN_IMAGE, (0, 0))
    font_large = pygame.font.Font(pygame.font.match_font('bold'), 60)
    font_small = pygame.font.Font(pygame.font.match_font('bold'), 60)

    title_text = font_large.render("Welcome to Snake Game", True, BLACK)
    start_text = font_large.render("Press Enter to Start", True, WHITE)
    surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 7.1))
    surface.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GAME_START_SOUND.play()  # Play sound when the game starts
                    return
#Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption("Snake Game")
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    # Start background music
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    snake = Snake()

    # Path to your cherry image (change this path as needed)
    cherry_image_path = "/Users/shabbirshaikh/Downloads/cherry_food-removebg-preview.png"
    food = Food(cherry_image_path)  # Pass the image path to the Food object

    game_over = False
    highest_score = load_high_score()  # Load highest score from file

    # Show the start screen
    show_start_screen(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(highest_score)  # Save highest score before exiting
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                replay_button = show_game_over(screen, snake.score, highest_score)
                button_x, button_y, button_width, button_height = replay_button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                    pygame.mixer.music.play(-1)  # Restart the background music

        if not game_over:
            game_over = snake.update()
            if game_over:
                pygame.mixer.Sound.play(GAME_OVER_SOUND)  # Play the game over sound
                pygame.mixer.music.stop()  # Stop the background music

            if not game_over:
                if snake.get_head_position() == food.position:
                    pygame.mixer.Sound.play(EAT_SOUND)  # Play the eating sound
                    snake.length += 1  # Increase the snake's length
                    snake.score += 1  # Increment the score
                    food.randomize_position()  # Generate new food position

            if snake.score > highest_score:
                highest_score = snake.score

        draw_textured_background(surface)

        if not game_over:
            snake.render(surface)
            food.render(surface)  # Render the food (cherry image)

        # Display the score
        font = pygame.font.Font(pygame.font.match_font('arial'), 24)
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        high_score_text = font.render(f"High Score: {highest_score}", True, BLACK)
        surface.blit(score_text, (10, 10))
        surface.blit(high_score_text, (10, 40))

        if game_over:
            replay_button = show_game_over(surface, snake.score, highest_score)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
