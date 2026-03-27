import functools
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game.engine.v2 import EngineV2
from game.adapters.obs_codec import encode_observation, legal_action_mask
from game.common.renderer import AbaloneRenderer
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

def env(render_mode=None, variant="classical", max_steps=200):
    """
    Standard PettingZoo creator with recommended wrappers.
    """
    env = raw_env(render_mode=render_mode, variant=variant, max_steps=max_steps)
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

class raw_env(AECEnv):
    metadata = {
        "render_modes": ["human", "ansi", "rgb_array"],
        "name": "abalone_v2",
        "is_parallelizable": False,
        "render_fps": 10,
    }

    def __init__(self, render_mode=None, variant="classical", max_steps=200):
        super().__init__()
        self.render_mode = render_mode
        self.variant = variant
        self.max_steps = max_steps
        
        self.agents = ["player_0", "player_1"]
        self.possible_agents = self.agents[:]
        self._agent_selector = agent_selector(self.agents)
        
        self.engine = None
        self.current_step = 0
        self.renderer = None
        if self.render_mode in {"human", "rgb_array"}:
            self.renderer = AbaloneRenderer(render_mode, window_size=(160, 160), fps=self.metadata["render_fps"])

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return spaces.Dict({
            "observation": spaces.Box(low=0, high=1, shape=(3, 61), dtype=np.int8),
            "action_mask": spaces.Box(low=0, high=1, shape=(2562,), dtype=np.int8)
        })

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return spaces.Discrete(2562)

    def render(self):
        if self.render_mode == "ansi":
            return self.engine.render_text()
        elif self.renderer:
            return self.renderer.render(self.engine)

    def observe(self, agent):
        return {
            "observation": encode_observation(self.engine),
            "action_mask": legal_action_mask(self.engine) if agent == self.agent_selection else np.zeros(2562, dtype=np.int8)
        }

    def reset(self, seed=None, options=None):
        self.current_step = 0
        from game.engine.consts import VARIANTS
        data = VARIANTS.get(self.variant, VARIANTS["classical"])
        board = [-1] * 61
        for p, p_set in enumerate(data["players_sets"]):
            for pos in p_set: board[pos] = p
        
        self.engine = EngineV2(board=board, to_play=0)
        
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0.0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0.0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        
        self._agent_selector.reinit(self.agents)
        self.agent_selection = self._agent_selector.next()
        
        if self.render_mode == "human":
            self.render()

    def step(self, action):
        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step(action)
            return

        agent = self.agent_selection
        self.current_step += 1
        
        # Apply action
        self.engine, move_type = self.engine.apply_action(int(action))
        
        # In AEC, we update rewards for the CURRENT agent based on the result
        # If someone wins, we terminate all agents.
        if self.engine.winner != -1:
            for a in self.agents:
                self.terminations[a] = True
                self.rewards[a] = 1.0 if a == f"player_{self.engine.winner}" else -1.0
        
        # Check truncation (limit reached for both players)
        if self.current_step >= self.max_steps * 2:
            for a in self.agents:
                self.truncations[a] = True
        
        # Accumulate and cycle
        self._accumulate_rewards()
        self.agent_selection = self._agent_selector.next()
        
        if self.render_mode == "human":
            self.render()

    def close(self):
        if self.renderer:
            self.renderer.close()
            self.renderer = None
