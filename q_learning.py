import numpy as np
import random
from snake_env import SnakeEnv

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay
        self.epsilon_min = 0.01
        self.q_table = {}

    def get_state_key(self, state):
        """Convert the observation part of the state tuple into a hashable key."""
        # Extract the observation from the tuple (if state is a tuple)
        observation, wall_distances = state
        flattened_obs = tuple(np.array(observation).flatten())
        return flattened_obs + tuple(wall_distances)


    def choose_action(self, state_key, action_space):
        """Choose action using epsilon-greedy policy."""
        if random.random() < self.epsilon:
            return action_space.sample()
        return max(range(action_space.n), key=lambda a: self.q_table.get((state_key, a), 0))

    def update_q_value(self, state_key, action, reward, next_state_key, done):
        """Update the Q-value using the Q-learning formula."""
        old_value = self.q_table.get((state_key, action), 0)
        future_reward = 0 if done else max(self.q_table.get((next_state_key, a), 0) for a in range(4))
        self.q_table[(state_key, action)] = old_value + self.lr * (reward + self.gamma * future_reward - old_value)

    def decay_exploration(self):
        """Decay the exploration rate."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

def train_agent(episodes=1000, max_steps_per_episode=1000):
    env = SnakeEnv()
    agent = train_agent(episodes=10000)

    for episode in range(episodes):
        state = env.reset()
        state_key = agent.get_state_key(state)
        total_reward = 0

        for _ in range(max_steps_per_episode):
            action = agent.choose_action(state_key, env.action_space)
            next_state, reward, done, _, _ = env.step(action)
            next_state_key = agent.get_state_key(next_state)

            agent.update_q_value(state_key, action, reward, next_state_key, done)
            state_key = next_state_key
            total_reward += reward

            if done:
                break

        agent.decay_exploration()
        print(f"Episode {episode + 1}/{episodes} - Total Reward: {total_reward}, Epsilon: {agent.epsilon}")

    env.close()
    return agent

if __name__ == "__main__":
    agent = train_agent()
