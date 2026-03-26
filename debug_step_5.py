import random
import numpy as np
import game.engine.v2 as v2_mod
from game.engine.v1_legacy import AbaloneGame
from game.engine.v2 import EngineV2

def debug():
    # Setup exactly like the random walk test
    random.seed(42) # Try to reproduce step 5
    v1 = AbaloneGame()
    v1.reset(variant_name="classical", random_player=False, player=0)
    
    v1_positions = v1.positions
    v2_mod.POSITIONS_2D = v1_positions
    v2_mod._COORD_MAP = {coord: i for i, coord in enumerate(v1_positions)}
    v2_mod.NEIGHBORS = [[-1]*6 for _ in range(61)]
    for i, (r, c) in enumerate(v1_positions):
        for d, (dr, dc) in enumerate(v2_mod._DIRECTIONS_V1):
            neighbor_coord = (r+dr, c+dc)
            if neighbor_coord in v2_mod._COORD_MAP:
                v2_mod.NEIGHBORS[i][d] = v2_mod._COORD_MAP[neighbor_coord]

    v2_board = [-1] * 61
    for pos, (r, c) in enumerate(v1_positions):
        tok = v1.board[r, c]
        if tok >= 0: v2_board[pos] = int(tok)
    v2 = EngineV2(v2_board, to_play=v1.current_player)

    for i in range(10):
        v1_moves = set(v1.get_possible_moves(v1.current_player))
        v2_moves = set(v2.get_legal_actions())
        
        print(f"STEP {i}: Player {v1.current_player}, V1 moves: {len(v1_moves)}, V2 moves: {len(v2_moves)}")
        
        if v1_moves != v2_moves:
            diff = v1_moves - v2_moves
            print(f"!!! Mismatch at step {i}")
            for m in diff:
                p0, p1 = m
                r0, c0 = v1_positions[p0]
                r1, c1 = v1_positions[p1]
                print(f"Move {m}: {r0,c0} -> {r1,c1}")
                # Analyze why V1 likes it
                check = v1.validate_move(p0, p1, v1.current_player, return_modif=True)
                print(f"V1 validate_move: {check}")
            break
            
        move = random.choice(list(v1_moves))
        v1.action_handler(*move)
        v2.apply(move)

if __name__ == "__main__":
    debug()
