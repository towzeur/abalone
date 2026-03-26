import json
from game.engine.v2 import EngineV2

def test_all_variants():
    with open("game/engine/variants.json", "r") as f:
        variants = json.load(f)
    
    print(f"Testing {len(variants)} variants...")
    for name, data in variants.items():
        try:
            # Create board from variant data
            board = [-1] * 61
            for p, p_set in enumerate(data["players_sets"]):
                for pos in p_set:
                    board[pos] = p
            
            engine = EngineV2(board=board, to_play=0)
            mask = engine.get_action_mask()
            num_legal = sum(mask)
            
            print(f"  [OK] {name}: {num_legal} legal actions")
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            raise e

if __name__ == "__main__":
    test_all_variants()
