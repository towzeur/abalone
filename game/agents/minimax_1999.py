import math
from game.engine.v2 import EngineV2, NEIGHBORS, POSITIONS_2D

# Poids extraits de l'IA 1999
RADIUS_WEIGHTS = {0: 8, 1: 7, 2: 6, 3: 4, 4: 1}

def get_hex_dist(p1_idx, p2_idx):
    """Calcule la distance hexagonale entre deux positions du plateau."""
    r1, c1 = POSITIONS_2D[p1_idx]
    r2, c2 = POSITIONS_2D[p2_idx]
    # Formule de distance pour coordonnées axiales (r, c)
    return (abs(r1 - r2) + abs(r1 + c1 - r2 - c2) + abs(c1 - c2)) // 2

# Précalcul des poids pour les 61 positions (Centre est à 5, 5 dans POSITIONS_2D)
CENTER_IDX = 30  # Dans EngineV2, la position (5,5) correspond à l'index 30
POSITION_WEIGHTS = [RADIUS_WEIGHTS[get_hex_dist(i, CENTER_IDX)] for i in range(61)]

class Minimax1999Agent:
    def __init__(self, depth=2, player_id=0):
        self.depth = depth
        self.player_id = player_id

    def evaluate(self, engine: EngineV2):
        """Fonction d'évaluation exacte extraite du binaire."""
        if engine.winner != -1:
            if engine.winner == self.player_id: return 10000
            else: return -10000

        score = 0
        opp_id = 1 - self.player_id

        for i in range(61):
            val = engine.board[i]
            if val == self.player_id:
                # Matériel (1000) + Position (1-8)
                score += 1000 + POSITION_WEIGHTS[i]
                
                # Bonus de cohésion (proximité alliée)
                for neighbor in NEIGHBORS[i]:
                    if neighbor != -1 and engine.board[neighbor] == self.player_id:
                        score += 2 # Léger bonus pour les billes groupées
                        
            elif val == opp_id:
                score -= (1000 + POSITION_WEIGHTS[i])
                for neighbor in NEIGHBORS[i]:
                    if neighbor != -1 and engine.board[neighbor] == opp_id:
                        score -= 2

        return score

    def select_action(self, engine: EngineV2):
        """Sélectionne la meilleure action en utilisant Alpha-Beta."""
        best_score = -math.inf
        best_action = None
        
        mask = engine.get_action_mask()
        legal_actions = [i for i, val in enumerate(mask) if val]
        
        if not legal_actions:
            return None

        # Tri rudimentaire pour améliorer l'élagage (Poussées d'abord)
        # L'IA 1999 ne triait probablement pas, mais EngineV2 est plus rapide ainsi.
        
        alpha = -math.inf
        beta = math.inf
        
        for action_id in legal_actions:
            new_engine = engine.clone()
            new_engine.apply_action(action_id)
            
            score = self._minimax(new_engine, self.depth - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_action = action_id
            
            alpha = max(alpha, best_score)
            
        return best_action

    def _minimax(self, engine, depth, alpha, beta, maximizing):
        if depth == 0 or engine.winner != -1:
            return self.evaluate(engine)

        mask = engine.get_action_mask()
        legal_actions = [i for i, val in enumerate(mask) if val]
        
        if maximizing:
            max_eval = -math.inf
            for action_id in legal_actions:
                new_engine = engine.clone()
                new_engine.apply_action(action_id)
                eval = self._minimax(new_engine, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for action_id in legal_actions:
                new_engine = engine.clone()
                new_engine.apply_action(action_id)
                eval = self._minimax(new_engine, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
