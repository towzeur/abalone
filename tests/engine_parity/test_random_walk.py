import random
import numpy as np
import game.engine.v2 as v2_mod
from game.engine.v1_legacy import AbaloneGame
from game.engine.v2 import EngineV2Legacy as EngineV2

def test_random_walk(num_steps=100):
    print(f"Starting Random Walk Parity Test ({num_steps} steps)...")
    
    # 1. Init V1
    v1 = AbaloneGame()
    v1.reset(variant_name="classical", random_player=False, player=0)
    
    # --- RUNTIME INJECTION FOR 100% INDEX PARITY ---
    v1_positions = v1.positions # the gold standard
    v2_mod.POSITIONS_2D = v1_positions
    v2_mod._COORD_MAP = {coord: i for i, coord in enumerate(v1_positions)}
    
    new_neighbors = []
    for i, (r, c) in enumerate(v1_positions):
        pos_neighbors = []
        for dr, dc in v2_mod._DIRECTIONS_V1:
            target = (r + dr, c + dc)
            pos_neighbors.append(v2_mod._COORD_MAP.get(target, -1))
        new_neighbors.append(tuple(pos_neighbors))
    v2_mod.NEIGHBORS = new_neighbors
    # -----------------------------------------------

    # 2. Init V2
    v2_board = [-1] * 61
    for pos, (r, c) in enumerate(v1_positions):
        tok = v1.board[r, c]
        if tok >= 0: v2_board[pos] = int(tok)
    v2 = EngineV2(v2_board, to_play=v1.current_player)

    for i in range(num_steps):
        # Compare legal moves
        v1_moves = set(v1.get_possible_moves(v1.current_player))
        v2_moves = set(v2.get_legal_actions())
        
        if v1_moves != v2_moves:
            print(f"STEP {i}: Move mismatch!")
            only_v1 = v1_moves - v2_moves
            only_v2 = v2_moves - v1_moves
            if only_v1:
                print(f"Only in V1 (total {len(only_v1)}):")
                for m in list(only_v1)[:5]:
                    p0, p1 = m
                    print(f"  {m} : {v1_positions[p0]} -> {v1_positions[p1]}")
                    check = v1.validate_move(p0, p1, v1.current_player, return_modif=True)
                    print(f"    V1 validation: {check}")
            if only_v2:
                print(f"Only in V2 (total {len(only_v2)}):")
                for m in list(only_v2)[:5]:
                    p0, p1 = m
                    print(f"  {m} : {v1_positions[p0]} -> {v1_positions[p1]}")
            raise AssertionError("Move sets diverged!")

        if not v1_moves:
            print("No more moves, game over?")
            break
            
        # Pick a random move
        move = random.choice(list(v1_moves))
        pos0, pos1 = move
        
        # Apply on V1
        v1.action_handler(pos0, pos1)
        
        # Apply on V2
        v2.apply(move)
        
        # Compare boards
        for pos, (r, c) in enumerate(v1_positions):
            if v1.board[r, c] != v2.board[pos]:
                print(f"STEP {i}: Board mismatch at index {pos} ({r},{c})!")
                print(f"V1: {v1.board[r, c]}, V2: {v2.board[pos]}")
                raise AssertionError("Boards diverged!")
        
        if v1.game_over != (v2.winner != -1):
            print(f"STEP {i}: Winner mismatch!")
            raise AssertionError("Game Over status diverged!")
            
        if v1.game_over:
            print(f"Game over at step {i}")
            break

    print(f"SUCCESS: {num_steps} steps completed with perfect parity.")

if __name__ == "__main__":
    test_random_walk(500)
