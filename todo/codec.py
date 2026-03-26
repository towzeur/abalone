N_POS = 61


def encode_action(pos0: int, pos1: int) -> int:
    return pos0 * N_POS + pos1


def decode_action(action_id: int) -> tuple[int, int]:
    return divmod(action_id, N_POS)
