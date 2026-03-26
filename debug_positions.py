from game.engine.v1_legacy import AbaloneGame
from game.engine.v2 import POSITIONS_2D

v1 = AbaloneGame()
v1.reset(variant_name="classical", random_player=False, player=0)

print("V1 POSITIONS (first 10):", v1.positions[:10])
print("V2 POSITIONS (first 10):", POSITIONS_2D[:10])

mismatches = []
for i in range(min(len(v1.positions), len(POSITIONS_2D))):
    if v1.positions[i] != POSITIONS_2D[i]:
        mismatches.append((i, v1.positions[i], POSITIONS_2D[i]))

if mismatches:
    print(f"Mismatches found: {len(mismatches)}")
    for m in mismatches[:5]:
        print(f"Index {m[0]}: V1={m[1]}, V2={m[2]}")
else:
    print("Positions match perfectly!")
