import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game.engine.v2 import EngineV2
from game.adapters.obs_codec import encode_observation, legal_action_mask

REWARDS = {
    'winner': 12,
    'ejected': 2,
    'inline_push': 0.5,
    'sidestep_move': -0.1,
    'inline_move': -0.1
}

class AbaloneGymEnv(gym.Env):
    metadata = {"render_modes": ["human", "ansi"], "render_fps": 4}

    def __init__(self, render_mode=None, variant="classical", max_steps=200):
        super().__init__()
        self.render_mode = render_mode
        self.variant = variant
        self.max_steps = max_steps
        self.current_step = 0
        
        self.action_space = spaces.Discrete(2562)
        self.observation_space = spaces.Dict({
            "observation": spaces.Box(low=0, high=1, shape=(3, 61), dtype=np.int8),
            "action_mask": spaces.Box(low=0, high=1, shape=(2562,), dtype=np.int8)
        })
        
        self.engine = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        
        from game.engine.consts import VARIANTS
        data = VARIANTS.get(self.variant, VARIANTS["classical"])
        board = [-1] * 61
        for p, p_set in enumerate(data["players_sets"]):
            for pos in p_set: board[pos] = p
        
        self.engine = EngineV2(board=board, to_play=0)
        
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self.render()
            
        return observation, info

    def step(self, action):
        self.current_step += 1
        self.engine, move_type = self.engine.apply_action(int(action))
        
        observation = self._get_obs()
        reward = float(REWARDS.get(move_type, 0.0))
        terminated = self.engine.winner != -1
        truncated = self.current_step >= self.max_steps
        info = self._get_info()
        
        if self.render_mode == "human":
            self.render()
            
        return observation, reward, terminated, truncated, info

    def _get_obs(self):
        return {
            "observation": encode_observation(self.engine),
            "action_mask": legal_action_mask(self.engine)
        }

    def _get_info(self):
        return {
            "to_play": self.engine.to_play,
            "damages": self.engine.damages,
            "step": self.current_step
        }

    def render(self):
        board_str = self.engine.render_text()
        if self.render_mode == "ansi":
            return board_str
        elif self.render_mode == "human":
            print(f"\nStep: {self.current_step} | Turn: {self.engine.to_play} | Score: {self.engine.damages}")
            print(board_str)
            print("-" * 20)

    def close(self):
        pass
