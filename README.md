# RL Snake Variant Project (Decaying Fruits)
![](https://img.shields.io/badge/gym-0.26.2-7F66E5) ![](https://img.shields.io/badge/pygame-2.6.1-AAEEBB)

## Project Description

This repository implements a reinforcement learning project that enhances the classic Snake game by introducing timed fruits with varying decay rates. The game mechanics include:
- Fruits have a limited lifespan before they "go bad."
- Once a fruit spoils, it becomes harmful and reduces the snake's length if consumed.
- Players must strategize to avoid spoiled fruits and adapt quickly to their environment.

The project involves developing a custom OpenAI Gym environment for this problem and implementing reinforcement learning (RL) algorithms to train agents to play the game effectively.

---

## Repository Structure

- `proposal.pdf`: Project proposal outlining the problem statement, milestones, feasibility, and references.
- `environment/`: Contains the custom Gym environment code.
  - `reward_structures.py`: Defines various reward structures for the Snake game.
  - `snake_env.py`: Implements the Snake game environment.
  - `test_snake_env.py`: Facilitates training and testing of the Q-learning agent, including interactive and demo modes.
- `results/`: Stores experiment results and performance evaluations.
- `report.pdf`: Detailed project report including challenges, approaches (Q-learning, DQN), state space, action space, reward structure, and empirical studies on training performance.

---

## Setup Instructions

### Prerequisites

Ensure that you have Python 3.8 or later installed. It is recommended to use a virtual environment to manage dependencies.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vidun-jay/RL-Snake-Variant.git
   cd RL-Snake-Variant
   ```

2. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Train the model interactively:**
   ```
   python3 environment/test_snake_env.py --interactive
   ```
   This command allows you to specify custom values for:
   - **Epsilon:** The exploration-exploitation parameter.
   - **Episode count:** Number of training episodes.
   - **Decay rates:** Controls the rate of exploration decay.

    Upon completion, a `q_table.pkl` file containing the trained model will be generated.

4. **Test the trained model in demo mode:**
   ```
   python3 environment/test_snake_env.py --demo
   ```

This allows you to observe how the agent adapts and avoids spoiled fruits while maximizing its score.
