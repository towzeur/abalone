# Action Codec - Compact Representation (AlphaZero style)
# Total actions: 61 positions * 6 directions * 7 types = 2562

MOVES_TYPES = [
    "inline_1", "inline_2", "inline_3", 
    "sidestep_2_axis1", "sidestep_2_axis2", 
    "sidestep_3_axis1", "sidestep_3_axis2"
]

def encode_action(pos: int, direction: int, type_idx: int) -> int:
    """
    Encodes an action into a single integer.
    pos: 0-60
    direction: 0-5
    type_idx: 0-6
    """
    return pos * 42 + (direction * 7) + type_idx

def decode_action(action_id: int) -> tuple[int, int, int]:
    """
    Decodes an action_id into (pos, direction, type_idx).
    """
    pos, rem = divmod(action_id, 42)
    direction, type_idx = divmod(rem, 7)
    return pos, direction, type_idx
