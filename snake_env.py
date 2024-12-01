import pygame
import sys
import random

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

class Snake:
    def __init__(self):
        self.positions = [self.random_start()]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1

    def random_start(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new_pos = ((cur[0] + (x * GRID_SIZE)) % WIDTH, (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if new_pos in self.positions[2:]:
            self.reset()
        else:
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
        # load the fruit image
        self.image = pygame.image.load("assets/fruit.png").convert_alpha()
        # scale image to fit the grid size
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))

    def random_position(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def draw(self, surface):
        # blit the image at the fruit's position
        surface.blit(self.image, self.position)

def main():
    snake = Snake()
    food = Food()
    running = True

    while running:
        clock.tick(10)
        snake.move()

        if snake.positions[0] == food.position:
            snake.length += 1
            food.position = food.random_position()

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

        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
