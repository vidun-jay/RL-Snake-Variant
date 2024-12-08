import argparse
from snake_env import SnakeEnv
import time
import os
import pickle
import random
import numpy as np
from tabulate import tabulate

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--demo", action="store_true", help="run a demonstration episode with epsilon=0 instead of training")
args = parser.parse_args()

def get_direction_index(direction):
    if direction == (0, -1):
        return 0
    elif direction == (0, 1):
        return 1
    elif direction == (-1, 0):
        return 2
    elif direction == (1, 0):
        return 3
    return 0

def state_to_key(env):
    snake_x, snake_y = env.snake.positions[0]
    snake_x_cell = snake_x // env.grid_size
    snake_y_cell = snake_y // env.grid_size
    food_x, food_y = env.food.position
    food_x_cell = food_x // env.grid_size
    food_y_cell = food_y // env.grid_size
    dir_idx = get_direction_index(env.snake.direction)
    return (snake_x_cell, snake_y_cell, food_x_cell, food_y_cell, dir_idx)

def start_table(headers):
    header_table = tabulate([], headers=headers, tablefmt="pretty")
    header_lines = header_table.split("\n")
    global top_border, header_line, bottom_border
    top_border = header_lines[0]
    header_line = header_lines[1]
    bottom_border = header_lines[2]
    print(top_border)
    print(header_line)

def print_table_row(headers, row):
    row_table = tabulate([row], headers=headers, tablefmt="pretty")
    row_lines = row_table.split("\n")
    data_line = row_lines[3]
    print(data_line)

def end_table():
    print(bottom_border)

# load q-table if exists
if os.path.exists("q_table.pkl"):
    with open("q_table.pkl", "rb") as f:
        Q = pickle.load(f)
else:
    Q = {}

# hyperparameters
alpha = 0.5
gamma = 0.99
initial_epsilon = 0.5
min_epsilon = 0.00001
epsilon_decay = 0.995
episodes = 5000

env = SnakeEnv()

if args.demo:
    # if demo flag is given, run a demonstration episode using epsilon=0
    epsilon = 0.0
    obs = env.reset()
    done = False
    while not done:
        state = state_to_key(env)
        if state not in Q:
            Q[state] = np.zeros(env.action_space.n)
        action = np.argmax(Q[state])  # greedy action
        obs, reward, done, truncated, info = env.step(action)
        env.render()
        time.sleep(0.05)
    env.close()
    print("Demonstration complete!")
else:
    # run training
    epsilon = initial_epsilon
    total_steps = 0
    best_total_reward = float('-inf')

    headers = ["Episode", "Total Reward", "Best Reward", "Epsilon"]
    start_table(headers)

    for episode in range(episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        snake_x, snake_y = env.snake.positions[0]
        food_x, food_y = env.food.position
        initial_dist = abs(snake_x - food_x) + abs(snake_y - food_y)

        while not done:
            state = state_to_key(env)
            if state not in Q:
                Q[state] = np.zeros(env.action_space.n)

            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(Q[state])

            old_dist = initial_dist
            next_obs, reward, done, truncated, info = env.step(action)

            snake_x, snake_y = env.snake.positions[0]
            food_x, food_y = env.food.position
            new_dist = abs(snake_x - food_x) + abs(snake_y - food_y)

            if new_dist < old_dist:
                reward += 5.0
            else:
                reward -= 2.0

            initial_dist = new_dist
            total_reward += reward

            next_state = state_to_key(env)
            if next_state not in Q:
                Q[next_state] = np.zeros(env.action_space.n)

            Q[state][action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state][action])

            total_steps += 1
            epsilon = max(min_epsilon, epsilon * epsilon_decay)

        if total_reward > best_total_reward:
            best_total_reward = total_reward

        row = [episode, round(total_reward, 2), round(best_total_reward, 2), round(epsilon, 4)]
        print_table_row(headers, row)

    end_table()

    with open("q_table.pkl", "wb") as f:
        pickle.dump(Q, f)

    env.close()
    print(f"Training complete! Best total reward: {best_total_reward}")
