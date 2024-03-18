import pygame
from collectible import Collectible

class Level:
    def __init__(self, level_num):
        self.level_num = level_num  # Store the current level number
        self.layouts = {
            1: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [4, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
                [1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
        }
        self.layout = self.layouts.get(level_num, self.layouts[1])
        self.player_start_pos = self.find_player_start()
        self.collectibles = []
        self.exit_position = None
        self.exit_open = False
        self.initialize_level()
        self.block_size = 25
        self.calculate_offsets()

    # Calculate total maze size and offsets once for reuse
    def calculate_offsets(self):
        maze_width = len(self.layout[0]) * self.block_size
        maze_height = len(self.layout) * self.block_size
        self.offset_x = (pygame.display.Info().current_w - maze_width) // 2
        self.offset_y = (pygame.display.Info().current_h - maze_height) // 2
    
    def find_player_start(self):
        for y, row in enumerate(self.layout):
            for x, block in enumerate(row):
                if block == 2:  # Player start position marked by '2'
                    return (x, y)
        return None

    def initialize_level(self):
        for y, row in enumerate(self.layout):
            for x, value in enumerate(row):
                if value == 3:
                    self.collectibles.append(Collectible(x, y))
                elif value == 4:
                    self.exit_position = (x, y)

    def draw(self, screen):
        for y, row in enumerate(self.layout):
            for x, block in enumerate(row):
                if block == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (x * self.block_size + self.offset_x, y * self.block_size + self.offset_y, self.block_size, self.block_size))
                elif block == 4:
                    if self.exit_open:
                        pygame.draw.rect(screen, (0, 255, 0), (x * self.block_size + self.offset_x, y * self.block_size + self.offset_y, self.block_size, self.block_size))
                    else:
                        pygame.draw.rect(screen, (255, 0, 0), (x * self.block_size + self.offset_x, y * self.block_size + self.offset_y, self.block_size, self.block_size))
        for collectible in self.collectibles:
            collectible.draw(screen, self.offset_x, self.offset_y)
    
    def check_collision(self, proposed_x, proposed_y):
        # Calculate the grid coordinates for all corners of the player's proposed position
        grid_coords = [
            ((proposed_x - self.offset_x) // self.block_size, (proposed_y - self.offset_y) // self.block_size),  # Top-left
            ((proposed_x + self.block_size - 1 - self.offset_x) // self.block_size, (proposed_y - self.offset_y) // self.block_size),  # Top-right
            ((proposed_x - self.offset_x) // self.block_size, (proposed_y + self.block_size - 1 - self.offset_y) // self.block_size),  # Bottom-left
            ((proposed_x + self.block_size - 1 - self.offset_x) // self.block_size, (proposed_y + self.block_size - 1 - self.offset_y) // self.block_size)  # Bottom-right
        ]

        for x, y in grid_coords:
            if x < 0 or y < 0 or y >= len(self.layout) or x >= len(self.layout[0]) or self.layout[y][x] == 1:
                return True  # Collision detected

        return False  # No collision