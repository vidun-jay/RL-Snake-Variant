from snake_env import SnakeEnv
import time

from snake_env import SnakeEnv
import time

env = SnakeEnv()
obs = env.reset()
done = False
total_reward = 0

while not done:
    # find the direction to the food
    food_x, food_y = env.food.position
    snake_x, snake_y = env.snake.positions[0]

    if food_x < snake_x:
        action = 2  # LEFT
    elif food_x > snake_x:
        action = 3  # RIGHT
    elif food_y < snake_y:
        action = 0  # UP
    elif food_y > snake_y:
        action = 1  # DOWN
    else:
        action = env.action_space.sample()  # fallback to random

    obs, reward, done, truncated, info = env.step(action)
    total_reward += reward
    env.render()
    time.sleep(0.1)

print(f"Game over! Total reward: {total_reward}")
env.close()
