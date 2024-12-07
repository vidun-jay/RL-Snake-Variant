from q_learning import QLearningAgent
from snake_env import SnakeEnv
import pygame
import time

def test_agent(agent, episodes=10, max_steps_per_episode=1000):
    env = SnakeEnv()
    total_rewards = []
    pygame.init()
    font = pygame.font.SysFont(None, 35)

    for episode in range(episodes):
        state = env.reset()
        state_key = agent.get_state_key(state)
        total_reward = 0

        for step in range(max_steps_per_episode):
            action = agent.choose_action(state_key, env.action_space)
            next_state, reward, done, _, _ = env.step(action)
            state_key = agent.get_state_key(next_state)
            total_reward += reward
            
            # Render the environment
            env.render()

            # Add overlays for state and reward
            screen = env.screen
            reward_text = font.render(f"Reward: {reward}", True, (0, 0, 0))
            total_reward_text = font.render(f"Total Reward: {total_reward}", True, (0, 0, 0))
            step_text = font.render(f"Step: {step + 1}", True, (0, 0, 0))
            episode_text = font.render(f"Episode: {episode + 1}/{episodes}", True, (0, 0, 0))

            # Blit the overlays on the screen
            screen.blit(reward_text, (10, 10))
            screen.blit(total_reward_text, (10, 50))
            screen.blit(step_text, (10, 90))
            screen.blit(episode_text, (10, 130))

            pygame.display.flip()
            time.sleep(0.1)

            if done:
                break

        total_rewards.append(total_reward)
        print(f"Episode {episode + 1}/{episodes} - Total Reward: {total_reward}")

    env.close()
    print(f"Average Reward: {sum(total_rewards) / episodes}")

if __name__ == "__main__":
    agent = QLearningAgent()  # Load your trained agent or use a new one
    test_agent(agent)
