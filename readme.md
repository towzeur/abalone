# Abalone V2 (High Performance)

Abalone is a strategic board game for two players, played on a hexagonal board with 61 positions. This repository provides a high-performance, pure Python implementation optimized for Reinforcement Learning (RL).

| Feature            | Value                               |
|--------------------|-------------------------------------|
| Import (Gym)       | `from envs.abalone_env import AbaloneGymEnv` |
| Import (PettingZoo)| `from envs.abalone_pettingzoo import env` |
| Actions            | Discrete(2562)                      |
| Agents             | 2 (player_0, player_1)              |
| Observation Shape  | (3, 61)                             |
| Observation Values | [0, 1]                              |

## Engine V2 Features
- **Pure Python**: No heavy dependencies (zero NumPy in the core logic) for maximum portability and speed in small-scale simulations.
- **Compact Action Space**: Reduced redundancy from 3721 (61x61) to 2562 unique physical moves.
- **Surgical Apply**: Board updates are performed via direct indexing using precomputed neighbor tables.
- **Variant Support**: Supports 60+ starting configurations (Classical, Belgian Daisy, German Daisy, etc.).

## Action Space
The action space is a discrete set of **2562** possible moves. Each action ID is a single integer encoded as:
`action_id = pos * 42 + direction * 7 + type`

- **pos (0-60)**: The pivot marble index (the "tail" of the moving group).
- **direction (0-5)**: Hexagonal directions (E, SE, SW, W, NW, NE).
- **type (0-6)**:
    - `0, 1, 2`: **In-line** move or push (1, 2, or 3 marbles).
    - `3, 4`: **Sidestep** of 2 marbles (aligned on axis 1 or 2).
    - `5, 6`: **Sidestep** of 3 marbles (aligned on axis 1 or 2).

## Observation Space
The observation is a dictionary containing:
- `observation`: A `(3, 61)` bitmask array.
    - **Plane 0**: Current player's marbles.
    - **Plane 1**: Opponent's marbles.
    - **Plane 2**: Current player index (all 0s or all 1s).
- `action_mask`: A `(2562,)` binary vector where `1` represents a legal move.

## Usage

### Gymnasium (Single Agent / Training)
```python
import gymnasium as gym
import envs # Registers the environment

env = gym.make("abalone-v2", render_mode="human")
obs, info = env.reset()

for _ in range(100):
    # Use action_mask for MaskablePPO
    mask = obs["action_mask"]
    action = env.action_space.sample(mask=mask) 
    
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
env.close()
```

### PettingZoo (Multi-Agent AEC)
```python
from envs.abalone_pettingzoo import env

parallel_env = env(render_mode="human")
parallel_env.reset()

for agent in parallel_env.agent_iter():
    observation, reward, termination, truncation, info = parallel_env.last()
    
    if termination or truncation:
        action = None
    else:
        mask = observation["action_mask"]
        action = parallel_env.action_space(agent).sample(mask=mask)
        
    parallel_env.step(action)
```

## Rewards
The default Gymnasium environment uses the following reward structure:
- **Winner**: +12
- **Ejected Marble**: +2
- **Inline Push**: +0.5
- **Movement (In-line/Sidestep)**: -0.1 (to encourage engagement)

In PettingZoo, standard zero-sum rewards are used (+1 for win, -1 for loss).

## Rendering
The environment supports a high-quality ASCII hexagonal renderer:
- `X`: Player 0
- `O`: Player 1
- `.`: Empty position

```text
     O O O O O
    O O O O O O
   . . O O O . .
  . . . . . . . .
 . . . . . . . . .
  . . . . . . . .
   . . X X X . .
    X X X X X X
     X X X X X
```
