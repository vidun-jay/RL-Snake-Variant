# RL Snake Variant Project (Decaying Fruits)

## Project Description

This repository contains the implementation for our reinforcement learning project where we enhance the classic Snake game by introducing timed fruits with varying decay rates. The game includes the following mechanics:
- Fruits have a limited lifespan before they "go bad."
- Once a fruit goes bad, it becomes harmful and reduces the snake's length if consumed.
- Players must strategize to avoid spoiled fruits and adapt quickly to their environment.

The project involves developing a custom OpenAI Gym environment for this problem and implementing reinforcement learning (RL) algorithms to train agents to play the game effectively.

---

## Repository Structure

- `proposal.pdf`: Project proposal with the problem statement, milestones, feasibility, and references.
- `environment/`: Code for the custom Gym environment.
  - `snake_env.py`: Implementation of the Snake game environment.
  - `README.md`: Details on the environment's state space, action space, reward structure, and environment interactions.
- `rl_algorithms/`: Implementations of various RL algorithms.
  - `dqn.py`: Deep Q-Learning implementation.
  - `ppo.py`: Proximal Policy Optimization implementation.
  - `random_agent.py`: Baseline random agent.
- `results/`: Results from experiments and performance evaluations.
  - `plots/`: Graphs and visualizations of algorithm performance.
  - `logs/`: Training logs and metrics.
- `report/`: Final project report following the NeurIPS style.

---

## Setup Instructions
TODO

### Prerequisites
TODO

### Installation
TODO
