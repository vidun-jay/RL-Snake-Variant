from snake_env import SnakeEnv 
import time

from snake_env import SnakeEnv
import time

env = SnakeEnv()
obs = env.reset()
done = False
total_reward = 0

while not done:
    action = env.action_space.sample()  # random action
    obs, reward, done, truncated, info = env.step(action)
    total_reward += reward
    env.render()
    time.sleep(0.1)

print(f"Game over! Total reward: {total_reward}")
env.close()
