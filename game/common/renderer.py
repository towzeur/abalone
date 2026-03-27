import pygame
import numpy as np
import os
from game.engine.v2 import POSITIONS_2D

class AbaloneRenderer:
    def __init__(self, render_mode, window_size=(160, 160), fps=10):
        self.render_mode = render_mode
        self.window_size = window_size
        self.fps = fps
        self.screen = None
        self.clock = None
        self.assets = {}

    def _load_assets(self):
        # We assume assets are in 'img/' directory relative to project root
        # If we're inside envs/, we might need to adjust, but usually scripts run from root
        asset_dir = "img"
        try:
            self.assets['board'] = pygame.image.load(os.path.join(asset_dir, "board.png")).convert()
            self.assets['marble_black'] = pygame.image.load(os.path.join(asset_dir, "marble_black.png")).convert_alpha()
            self.assets['marble_white'] = pygame.image.load(os.path.join(asset_dir, "marble_white.png")).convert_alpha()
            self.assets['slot'] = pygame.image.load(os.path.join(asset_dir, "slot.png")).convert_alpha()
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Fallback (optional: we could generate them on the fly if missing)

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

        # Draw board background
        if 'board' in self.assets:
            self.screen.blit(self.assets['board'], (0, 0))
        else:
            self.screen.fill((220, 220, 220))

        # Constants for drawing
        center_x, center_y = self.window_size[0] // 2, self.window_size[1] // 2
        # Scale for 160x160. Old scale 13 for 130x130 => 16 for 160x160 roughly
        scale = 16 
        dy = scale * 0.866
        dx = scale

        # Draw board positions and marbles
        for i, (r, c) in enumerate(POSITIONS_2D):
            # Hexagonal coordinate mapping
            # r, c are from 1 to 9. Center is (5, 5).
            y = center_y + (r - 5) * dy
            x = center_x + (c - 5 - (r - 5) / 2.0) * dx
            
            # Center the image on the coordinate
            img_pos = (int(x - 12), int(y - 12)) # 24/2 = 12
            
            val = engine.board[i]
            if val == 0: # Player 0 (Black)
                if 'marble_black' in self.assets:
                    self.screen.blit(self.assets['marble_black'], img_pos)
            elif val == 1: # Player 1 (White)
                if 'marble_white' in self.assets:
                    self.screen.blit(self.assets['marble_white'], img_pos)
            else: # Empty
                if 'slot' in self.assets:
                    self.screen.blit(self.assets['slot'], img_pos)

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
