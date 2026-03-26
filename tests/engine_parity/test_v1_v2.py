import numpy as np
from game.engine.v1_legacy import AbaloneGame
import game.engine.v2 as v2_mod
from game.engine.v2 import EngineV2Legacy as EngineV2

def test_parity():
    # 1. Initialize V1
    v1 = AbaloneGame()
    v1.reset(variant_name="classical", random_player=False, player=0)
    print(f"V1 position 45: {v1.positions[45]}")
    print(f"V1 position 48: {v1.positions[48]}")
    print(f"V1 position 44: {v1.positions[44]}")
    print(f"V1 position 40: {v1.positions[40]}")
    
    # FOR PARITY: Inject V1 positions into V2 module
    v1_positions = v1.positions
    v2_mod.POSITIONS_2D = v1_positions
    v2_mod._COORD_MAP = {coord: i for i, coord in enumerate(v1_positions)}
    # Re-compute NEIGHBORS with injected positions
    v2_mod.NEIGHBORS = [[-1] * 6 for _ in range(61)]
    for i, (r, c) in enumerate(v1_positions):
        for d, (dr, dc) in enumerate(v2_mod._DIRECTIONS_V1):
            neighbor_coord = (r + dr, c + dc)
            if neighbor_coord in v2_mod._COORD_MAP:
                v2_mod.NEIGHBORS[i][d] = v2_mod._COORD_MAP[neighbor_coord]

    # 2. Initialize V2 with same state
    v2_board = np.full(61, -1, dtype=np.int8)
    for pos, (r, c) in enumerate(v1_positions):
        tok = v1.board[r, c]
        if tok >= 0:
            v2_board[pos] = tok
            
    v2 = EngineV2(v2_board, to_play=v1.current_player)
    
    # 3. Compare legal moves
    v1_moves = v1.get_possible_moves(v1.current_player)
    v2_moves = v2.get_legal_actions()
    
    print(f"V1 moves count: {len(v1_moves)}")
    print(f"V2 moves count: {len(v2_moves)}")
    
    v1_set = set(v1_moves)
    v2_set = set(v2_moves)
    
    only_v1 = v1_set - v2_set
    only_v2 = v2_set - v1_set
    
    if only_v1:
        print(f"Only in V1 (total {len(only_v1)}):")
        for m in sorted(list(only_v1))[:10]:
            p0, p1 = m
            print(f"  {m} : {v1_positions[p0]} -> {v1_positions[p1]}")
    if only_v2:
        print(f"Only in V2 (total {len(only_v2)}):")
        for m in sorted(list(only_v2))[:10]:
            p0, p1 = m
            print(f"  {m} : {v1_positions[p0]} -> {v1_positions[p1]}")
        
    assert v1_set == v2_set, "Move sets do not match!"
    print("Parity test passed for classical start!")

if __name__ == "__main__":
    try:
        test_parity()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
