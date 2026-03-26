import numpy as np
from game.engine.v2 import EngineV2

def encode_observation(engine: EngineV2):
    """
    Returns (3, 61) observation.
    Plane 0: My marbles
    Plane 1: Opponent marbles
    Plane 2: Constant plane for current player index (0 or 1)
    """
    obs = np.zeros((3, 61), dtype=np.int8)
    cp = engine.to_play
    opp = 1 - cp
    
    # Efficient indexing for list-based board
    for i, val in enumerate(engine.board):
        if val == cp:
            obs[0, i] = 1
        elif val == opp:
            obs[1, i] = 1
            
    obs[2, :] = cp
    return obs

def legal_action_mask(engine: EngineV2):
    """
    Returns (2562,) action mask for MaskablePPO.
    """
    # EngineV2.get_action_mask() returns a bytearray(2562)
    return np.frombuffer(engine.get_action_mask(), dtype=np.int8)
