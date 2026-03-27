import pygame
import os

def generate_assets(img_dir="img", board_size=160, marble_size=16):
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    pygame.init()
    
    # 1. Generate board background
    board = pygame.Surface((board_size, board_size))
    board.fill((220, 220, 220))
    
    # We could draw the slots on the board PNG directly, 
    # but usually it's better to have a clean board and draw slots in the renderer.
    # For now, let's just make a simple colored board.
    pygame.image.save(board, os.path.join(img_dir, "board.png"))
    
    # 2. Generate black marble (Player 0)
    black_marble = pygame.Surface((marble_size, marble_size), pygame.SRCALPHA)
    pygame.draw.circle(black_marble, (20, 20, 20), (marble_size // 2, marble_size // 2), marble_size // 2 - 1)
    pygame.draw.circle(black_marble, (60, 60, 60), (marble_size // 3, marble_size // 3), marble_size // 6)
    pygame.image.save(black_marble, os.path.join(img_dir, "marble_black.png"))
    
    # 3. Generate white marble (Player 1)
    white_marble = pygame.Surface((marble_size, marble_size), pygame.SRCALPHA)
    pygame.draw.circle(white_marble, (250, 250, 250), (marble_size // 2, marble_size // 2), marble_size // 2 - 1)
    pygame.draw.circle(white_marble, (20, 20, 20), (marble_size // 2, marble_size // 2), marble_size // 2 - 1, 1)
    pygame.draw.circle(white_marble, (255, 255, 255), (marble_size // 3, marble_size // 3), marble_size // 6)
    pygame.image.save(white_marble, os.path.join(img_dir, "marble_white.png"))
    
    # 4. Generate slot (Empty position)
    slot = pygame.Surface((marble_size, marble_size), pygame.SRCALPHA)
    slot_radius = max(2, marble_size // 6)
    pygame.draw.circle(slot, (170, 170, 170), (marble_size // 2, marble_size // 2), slot_radius)
    pygame.image.save(slot, os.path.join(img_dir, "slot.png"))

    pygame.quit()

if __name__ == "__main__":
    generate_assets()
    print("Assets generated in img/ (board: 160x160, marbles/slots: 16x16)")
