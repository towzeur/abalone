import numpy as np
from .codec import encode_action


def encode_observation(game):
    # game.current_player, game.players (=2), game.positions, game.board
    obs = np.zeros((3, 61), dtype=np.int8)
    cp = game.current_player
    op = (cp + 1) % game.players

    for pos, (r, c) in enumerate(game.positions):
        tok = game.board[r, c]
        if tok == cp:
            obs[0, pos] = 1
        elif tok == op:
            obs[1, pos] = 1

    obs[2, :] = cp  # plane constant (0/1)
    return obs


def legal_action_mask(game):
    mask = np.zeros((61 * 61,), dtype=np.int8)
    for pos0, pos1 in game.get_possible_moves(game.current_player):
        mask[encode_action(pos0, pos1)] = 1
    return mask
