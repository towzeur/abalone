import numpy as np
from gymnasium import spaces

N_POS = 61
N_ACTIONS = N_POS * N_POS  # MVP: action = (pos0, pos1)

# Observation "canonique" commune Gymnasium & PettingZoo
# C=3: [my_marbles, opp_marbles, to_play]
OBS_SHAPE = (3, N_POS)

observation_space = spaces.Dict(
    {
        "observation": spaces.Box(low=0, high=1, shape=OBS_SHAPE, dtype=np.int8),
        "action_mask": spaces.Box(low=0, high=1, shape=(N_ACTIONS,), dtype=np.int8),
    }
)

action_space = spaces.Discrete(N_ACTIONS)
