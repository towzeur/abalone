# Engine V2 - Pure Python (High Performance)
# Optimized for Surgical Apply and Training (MaskablePPO)
# No NumPy dependency in core logic.

def _get_v1_positions():
    """Returns the same positions list as Engine V1."""
    n = 11
    board = [[-1] * n for _ in range(n)]
    for i in range(n):
        board[0][i] = board[n-1][i] = board[i][0] = board[i][n-1] = -2
    for i in range(4):
        for j in range(1, 4 - i + 1):
            board[1 + i][j] = -2
            board[n - 2 - i][6 + i + j - 1] = -2
    positions = []
    for r in range(n):
        for c in range(n):
            if board[r][c] == -1: positions.append((r, c))
    return positions

POSITIONS_2D = _get_v1_positions()
_COORD_MAP = {coord: i for i, coord in enumerate(POSITIONS_2D)}
_DIRECTIONS_V1 = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
OPPOSITE = (3, 4, 5, 0, 1, 2)

# Precompute NEIGHBORS[61][6]
NEIGHBORS = []
for i, (r, c) in enumerate(POSITIONS_2D):
    pos_neighbors = []
    for dr, dc in _DIRECTIONS_V1:
        target = (r + dr, c + dc)
        pos_neighbors.append(_COORD_MAP.get(target, -1))
    NEIGHBORS.append(tuple(pos_neighbors))

class EngineV2:
    """High-performance core engine using compact action space (2562)."""
    __slots__ = ['board', 'to_play', 'damages', 'winner']

    def __init__(self, board=None, to_play=0, damages=None, winner=-1):
        self.board = list(board) if board is not None else [-1] * 61
        self.to_play = to_play
        self.damages = list(damages) if damages else [0, 0]
        self.winner = winner

    def clone(self):
        return EngineV2(self.board, self.to_play, self.damages, self.winner)

    def get_action_mask(self):
        """Returns a list of 2562 bits for RL training."""
        mask = bytearray(2562)
        my_marbles = [i for i, v in enumerate(self.board) if v == self.to_play]
        for p0 in my_marbles:
            for d in range(6):
                for t in range(7):
                    if self.is_legal(p0, d, t):
                        mask[p0 * 42 + d * 7 + t] = 1
        return mask

    def is_legal(self, p0, d, t):
        # 1. Inline (1, 2, 3)
        if t < 3:
            size = t + 1
            group = [p0]
            for _ in range(size - 1):
                next_node = NEIGHBORS[group[-1]][d]
                if next_node == -1 or self.board[next_node] != self.to_play: return False
                group.append(next_node)
            dest = NEIGHBORS[group[-1]][d]
            if dest == -1: return False
            if self.board[dest] == -1: return True
            return bool(self._check_push(group, d))
        # 2. Sidestep (2, 3)
        else:
            axis = (d + 1) % 6 if t in (3, 5) else (d + 2) % 6
            size = 2 if t in (3, 4) else 3
            group = [p0]
            for _ in range(size - 1):
                next_node = NEIGHBORS[group[-1]][axis]
                if next_node == -1 or self.board[next_node] != self.to_play: return False
                group.append(next_node)
            for m in group:
                dest = NEIGHBORS[m][d]
                if dest == -1 or self.board[dest] != -1: return False
            return True

    def _check_push(self, allies, d):
        head = allies[-1]
        opp = 1 - self.to_play
        enemies = []
        curr = NEIGHBORS[head][d]
        while curr != -1 and self.board[curr] == opp:
            enemies.append(curr)
            curr = NEIGHBORS[curr][d]
        if 0 < len(enemies) < len(allies) and len(allies) < 4:
            if curr == -1 or self.board[curr] == -1:
                return (tuple(allies), tuple(enemies), d)
        return None

    def apply_action(self, action_id):
        """Standard method for RL training."""
        pos, rem = divmod(action_id, 42)
        direction, type_idx = divmod(rem, 7)
        move_type = "invalid"
        
        if type_idx < 3: # Inline/Push
            size = type_idx + 1
            group = [pos]
            for _ in range(size - 1): group.append(NEIGHBORS[group[-1]][direction])
            dest = NEIGHBORS[group[-1]][direction]
            if dest != -1 and self.board[dest] == -1:
                for m in group[::-1]: self.board[NEIGHBORS[m][direction]] = self.to_play
                self.board[pos] = -1
                move_type = "inline_move"
            else:
                push_info = self._check_push(group, direction)
                if push_info:
                    allies, enemies, d = push_info
                    opp = 1 - self.to_play
                    last_enemy = enemies[-1]
                    target_p = NEIGHBORS[last_enemy][d]
                    if target_p == -1:
                        self.damages[opp] += 1
                        move_type = "ejected"
                        if self.damages[opp] == 6: 
                            self.winner = self.to_play
                            move_type = "winner"
                    else:
                        self.board[target_p] = opp
                        move_type = "inline_push"
                    for m in allies[::-1]: self.board[NEIGHBORS[m][d]] = self.to_play
                    self.board[pos] = -1
        else: # Sidestep
            axis = (direction + 1) % 6 if type_idx in (3, 5) else (direction + 2) % 6
            size = 2 if type_idx in (3, 4) else 3
            group = [pos]
            for _ in range(size - 1): group.append(NEIGHBORS[group[-1]][axis])
            for m in group:
                self.board[NEIGHBORS[m][direction]] = self.to_play
                self.board[m] = -1
            move_type = "sidestep_move"
        
        self.to_play = 1 - self.to_play
        return self, move_type

    def render_text(self):
        """Returns a string representation of the board in a hexagonal ASCII grid."""
        # 2D buffer for the 11x11 grid
        grid = [[' ' for _ in range(11)] for _ in range(11)]
        for i, (r, c) in enumerate(POSITIONS_2D):
            val = self.board[i]
            char = '.'
            if val == 0: char = 'X'
            if val == 1: char = 'O'
            grid[r][c] = char
        
        output = []
        for r in range(1, 10):
            row_content = []
            # Calculate indentation for hexagonal look
            indent = abs(5 - r)
            line = " " * indent
            for c in range(11):
                if grid[r][c] != ' ':
                    row_content.append(grid[r][c])
            line += " ".join(row_content)
            output.append(line)
        return "\n".join(output)

class EngineV2Legacy(EngineV2):
    """Subclass containing all parity testing and legacy compatibility methods."""
    
    def get_legal_actions(self):
        """Returns the EXACT same set of (pos0, pos1) as V1 for parity tests."""
        actions = []
        for p0 in range(61):
            if self.board[p0] != self.to_play: continue
            for d in range(6):
                for t in range(3):
                    if self.is_legal(p0, d, t):
                        size = t + 1
                        curr = p0
                        for _ in range(size): curr = NEIGHBORS[curr][d]
                        actions.append((p0, curr))
                for t in (3, 4, 5, 6):
                    if self.is_legal(p0, d, t):
                        axis = (d + 1) % 6 if t in (3, 5) else (d + 2) % 6
                        size = 2 if t in (3, 4) else 3
                        curr = p0
                        for _ in range(size):
                            actions.append((curr, NEIGHBORS[curr][d]))
                            curr = NEIGHBORS[curr][axis]
        return actions

    def validate_move(self, p0, p1):
        """Legacy validation for (pos0, p1). Used in debug scripts."""
        for d in range(6):
            curr = p0
            for step in range(1, 5):
                curr = NEIGHBORS[curr][d]
                if curr == p1:
                    if self.is_legal(p0, d, step-1): return True
                    break
        for t in (3, 4, 5, 6):
            for d in range(6):
                if self.is_legal(p0, d, t):
                    axis = (d + 1) % 6 if t in (3, 5) else (d + 2) % 6
                    size = 2 if t in (3, 4) else 3
                    group = [p0]
                    for _ in range(size - 1): group.append(NEIGHBORS[group[-1]][axis])
                    if any(NEIGHBORS[m][d] == p1 for m in group): return True
        return False

    def apply(self, action):
        """Maps (pos0, pos1) back to the unique physical action_id and applies it."""
        p0, p1 = action
        # Logic to find the best action_id for this (pos0, pos1)
        for d in range(6):
            curr = p0
            for step in range(1, 5):
                curr = NEIGHBORS[curr][d]
                if curr == p1:
                    if self.is_legal(p0, d, step-1):
                        return self.apply_action(p0 * 42 + d * 7 + (step-1))
                    break
        for t in (3, 4, 5, 6):
            for d in range(6):
                if self.is_legal(p0, d, t):
                    axis = (d + 1) % 6 if t in (3, 5) else (d + 2) % 6
                    size = 2 if t in (3, 4) else 3
                    group = [p0]
                    for _ in range(size - 1): group.append(NEIGHBORS[group[-1]][axis])
                    for m in group:
                        if NEIGHBORS[m][d] == p1:
                            return self.apply_action(p0 * 42 + d * 7 + t)
        return self
