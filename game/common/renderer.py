import pygame
import numpy as np
from game.engine.v2 import POSITIONS_2D
from pathlib import Path

def load_image(name, asset_dir="img"):
    path = Path(asset_dir) / name
    if not path.exists():
        raise FileNotFoundError(f"Asset not found: {path}")
    return pygame.image.load(str(path))

class AbaloneRenderer:
    CELL_SIZE = 16
    # Pixel-perfect calibration knobs for 160x160 board alignment.
    # Increase GRID_SCALE to spread the grid, decrease to tighten it.
    # GRID_X_OFFSET / GRID_Y_OFFSET shift all pieces in pixels.
    GRID_SCALE = 1.0
    GRID_X_OFFSET = 0.0
    GRID_Y_OFFSET = 0.0

    def __init__(self, render_mode, window_size=(160, 160), fps=10):
        self.render_mode = render_mode
        self.window_size = window_size
        self.fps = fps
        self.screen = None
        self.clock = None
        self.assets = {}

    def _load_assets(self):
        # Load assets from 'img/' directory
        asset_dir = Path(__file__).resolve().parents[2] / "img"
        try:
            board_img = load_image("board.png", asset_dir)
            marble_black_img = load_image("marble_black.png", asset_dir)
            marble_white_img = load_image("marble_white.png", asset_dir)
            slot_img = load_image("slot.png", asset_dir)
            
            # Convert to display format for better performance (only if display surface exists)
            if pygame.display.get_surface():
                self.assets['board'] = board_img.convert()
                self.assets['marble_black'] = marble_black_img.convert_alpha()
                self.assets['marble_white'] = marble_white_img.convert_alpha()
                self.assets['slot'] = slot_img.convert_alpha()
            else:
                # Fallback if no display yet
                self.assets['board'] = board_img
                self.assets['marble_black'] = marble_black_img
                self.assets['marble_white'] = marble_white_img
                self.assets['slot'] = slot_img
        except Exception as e:
            print(f"Error loading assets: {e}")

    def render(self, engine):
        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.set_caption("Abalone")
                self.screen = pygame.display.set_mode(self.window_size)
            elif self.render_mode == "rgb_array":
                self.screen = pygame.Surface(self.window_size)
            self.clock = pygame.time.Clock()
            self._load_assets()

        # Draw board texture in the full frame (tight 160x160 by default).
        if 'board' in self.assets:
            board_img = self.assets['board']
            if board_img.get_size() != self.window_size:
                board_img = pygame.transform.smoothscale(board_img, self.window_size)
            self.screen.blit(board_img, (0, 0))
        else:
            self.screen.fill((220, 220, 220))

        marble_surface = self.assets.get('marble_black') or self.assets.get('slot')
        marble_w = marble_surface.get_width() if marble_surface else self.CELL_SIZE
        marble_h = marble_surface.get_height() if marble_surface else self.CELL_SIZE
        half_w = marble_w / 2.0
        half_h = marble_h / 2.0

        # Compute a hex step that fits a 9x9 Abalone projection inside the frame.
        # Horizontal span is 8 steps between centers; vertical is 8 * (step * 0.866).
        max_step_x = (self.window_size[0] - marble_w) / 8.0
        max_step_y = (self.window_size[1] - marble_h) / (8.0 * 0.866)
        base_step = min(max_step_x, max_step_y)
        step = base_step * self.GRID_SCALE
        dy = step * 0.866

        # Group coordinates by row to center each row independently.
        row_cols = {}
        for r, c in POSITIONS_2D:
            row_cols.setdefault(r, []).append(c)
        row_bounds = {r: (min(cols), max(cols)) for r, cols in row_cols.items()}

        board_used_h = marble_h + 8.0 * dy
        top_margin = (self.window_size[1] - board_used_h) / 2.0

        # Draw board positions and marbles
        for i, (r, c) in enumerate(POSITIONS_2D):
            c_min, c_max = row_bounds[r]
            row_count = c_max - c_min + 1
            row_used_w = marble_w + (row_count - 1) * step
            row_left = (self.window_size[0] - row_used_w) / 2.0

            x = row_left + half_w + (c - c_min) * step + self.GRID_X_OFFSET
            y = top_margin + half_h + (r - 1) * dy + self.GRID_Y_OFFSET
            img_pos = (int(round(x - half_w)), int(round(y - half_h)))
            
            val = engine.board[i]
            if val == 0: # Player 0 (Black)
                marble_black = self.assets.get('marble_black')
                if marble_black is not None:
                    self.screen.blit(marble_black, img_pos)
            elif val == 1: # Player 1 (White)
                marble_white = self.assets.get('marble_white')
                if marble_white is not None:
                    self.screen.blit(marble_white, img_pos)
            else: # Empty slot
                slot = self.assets.get('slot')
                if slot is not None:
                    self.screen.blit(slot, img_pos)

        if self.render_mode == "human":
            pygame.display.update()
            self.clock.tick(self.fps)
        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None
