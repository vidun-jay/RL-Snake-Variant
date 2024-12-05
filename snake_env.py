import pygame
import sys
import random
from reward_structures import *

pygame.init()
pygame.display.set_caption("Snake Game")

# screen dimensions
GRID_SIZE = 40
WIDTH, HEIGHT = 1280, 960

# colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 128, 0)

# directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# create a font for rendering text
font = pygame.font.SysFont(None, 35)

class Snake:
    def __init__(self):
        self.positions = [self.random_start()]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.alive = True
        self.multiplier = 1
        self.fresh_fruit_combo = 0

    def random_start(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def move(self):
        if not self.alive:
            return
        if self.length <= 0 or len(self.positions) == 0:
            self.alive = False
            return
        
        cur = self.positions[0]
        x, y = self.direction
        new_x = cur[0] + (x * GRID_SIZE)
        new_y = cur[1] + (y * GRID_SIZE)

        # check for collision with edges
        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            self.alive = False
            return

        new_pos = (new_x, new_y)

        # check for collision with self
        if new_pos in self.positions[2:]:
            self.alive = False
            return

        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.__init__()

    def change_direction(self, dir):
        opposite = (self.direction[0] * -1, self.direction[1] * -1)
        if dir != opposite:
            self.direction = dir

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

class Food:
    def __init__(self):
        self.position = self.random_position()
        # load the fruit images
        self.fresh_image = pygame.image.load("assets/fruit.png").convert_alpha()
        self.fresh_image = pygame.transform.scale(self.fresh_image, (GRID_SIZE, GRID_SIZE))
        self.decayed_image = pygame.image.load("assets/decayed_fruit.png").convert_alpha()
        self.decayed_image = pygame.transform.scale(self.decayed_image, (GRID_SIZE, GRID_SIZE))
        self.image = self.fresh_image
        self.spawn_time = pygame.time.get_ticks()
        self.decayed = False        
        self.penalty = 0

    def random_position(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def update(self, decay_rate=5000):
        current_time = pygame.time.get_ticks()
        time_passed = current_time - self.spawn_time

        if time_passed >= decay_rate:
            self.decayed = True
            self.image = self.decayed_image
            
    def reset(self):
        self.position = self.random_position()
        self.spawn_time = pygame.time.get_ticks()
        self.decayed = False
        self.penalty = 0
        self.image = self.fresh_image

    def draw(self, surface):
        # blit the image at the fruit's position
        surface.blit(self.image, self.position)

def main():
    snake = Snake()
    food = Food()
    running = True
    game_over = False

    while running:
        clock.tick(10)

        if not game_over:

            # check if the snake is alive
            if not snake.alive or snake.length <= 0:
                game_over = True

            else:
                snake.move()
                
                # reward structure
                time_sensitive_rewards(snake, food)

                # update the food state after each iteration
                food.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_r and game_over:
                    # restart the game when 'R' is pressed
                    snake = Snake()
                    food = Food()
                    game_over = False

        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)

        # render the length counter
        length_text = font.render(f"Length: {snake.length}", True, BLACK)
        screen.blit(length_text, (10, 10))  # display at the top-left corner

        if game_over:
            # display game over message
            font_game_over = pygame.font.SysFont(None, 75)
            text = font_game_over.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

            # display restart instruction
            instruction = font_game_over.render("Press 'R' to Restart", True, BLACK)
            instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            screen.blit(instruction, instruction_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
