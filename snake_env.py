import pygame
import random
import gym
from gym import spaces
import numpy as np

# Constants
GRID_SIZE = 40
WIDTH, HEIGHT = 1280, 960

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 128, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGymEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super(SnakeGymEnv, self).__init__()
        self.GRID_SIZE = GRID_SIZE
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.action_space = spaces.Discrete(4)  # Actions: [0: UP, 1: DOWN, 2: LEFT, 3: RIGHT]
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(self.HEIGHT // self.GRID_SIZE, self.WIDTH // self.GRID_SIZE, 1),
            dtype=np.uint8,
        )

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Gym Environment")
        self.clock = pygame.time.Clock()

        self.snake = None
        self.food = None
        self.terminated = False
        self.score = 0
        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.snake = Snake()
        self.food = Food()
        self.terminated = False
        self.score = 0

        if seed is not None:
            self.seed(seed)

        return self._get_observation(), {}

    def step(self, action):
        directions = [UP, DOWN, LEFT, RIGHT]
        self.snake.change_direction(directions[action])
        self.snake.move()

        reward = 0
        terminated = False
        truncated = False

        if not self.snake.alive:
            self.terminated = True
            reward = -10
        elif self.snake.positions[0] == self.food.position:
            if self.food.decayed:
                reward = -5
                self.snake.length -= 1
            else:
                reward = 10
                self.snake.length += 1
            self.food.reset()

        self.food.update()

        if self.snake.length <= 0:
            self.terminated = True

        return self._get_observation(), reward, self.terminated, truncated, {"score": self.score}

    def render(self, mode="human"):
        if mode == "human":
            self.screen.fill(WHITE)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)

    def close(self):
        pygame.quit()

    def _get_observation(self):
        grid = np.zeros((self.HEIGHT // self.GRID_SIZE, self.WIDTH // self.GRID_SIZE), dtype=np.uint8)
        for pos in self.snake.positions:
            x, y = pos[0] // self.GRID_SIZE, pos[1] // self.GRID_SIZE
            grid[y, x] = 1

        fx, fy = self.food.position[0] // self.GRID_SIZE, self.food.position[1] // self.GRID_SIZE
        grid[fy, fx] = 2
        return grid[:, :, None]  # Add channel dimension


class Snake:
    def __init__(self):
        self.positions = [self.random_start()]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.alive = True

    def random_start(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def move(self):
        if not self.alive:
            return
        cur = self.positions[0]
        x, y = self.direction
        new_x = cur[0] + (x * GRID_SIZE)
        new_y = cur[1] + (y * GRID_SIZE)

        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT or (new_x, new_y) in self.positions[2:]:
            self.alive = False
            return

        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def change_direction(self, direction):
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)


class Food:
    def __init__(self):
        self.position = self.random_position()
        self.spawn_time = pygame.time.get_ticks()
        self.decayed = False

    def random_position(self):
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def update(self):
        if not self.decayed and pygame.time.get_ticks() - self.spawn_time > 5000:
            self.decayed = True

    def reset(self):
        self.position = self.random_position()
        self.spawn_time = pygame.time.get_ticks()
        self.decayed = False

    def draw(self, surface):
        color = (255, 0, 0) if self.decayed else (0, 255, 0)
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, color, rect)


# Gym registration
gym.envs.registration.register(id="SnakeGym-v0", entry_point="__main__:SnakeGymEnv")

if __name__ == "__main__":
    # Standalone test for Gym environment
    env = gym.make("SnakeGym-v0")
    obs, info = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()  # Random action
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        env.render()

    env.close()
