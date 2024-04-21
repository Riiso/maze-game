import pygame
import os
import sys
import ast
from collectible import Collectible
from enemy import GateDefender, CornerDefender, HallwayDefender

class Level:
    def __init__(self, level_num, dev_mode):
        self.level_num = level_num  # Store the current level number
        self.dev_mode = dev_mode  # Store the developer mode setting
        self.layouts = self.load_layouts()  # Load the layouts for the levels
        self.layout = self.layouts.get(level_num, self.layouts[1])
        self.player_start_pos = self.find_player_start()
        self.collectibles = []
        self.exit_positions = []  # To hold all exit block positions
        self.exit_open = False
        self.initialize_level()
        self.block_size = 25
        self.calculate_offsets()
        self.enemies = []
        self.initialize_enemies()

    def load_layouts(self):
        layouts = {}    # Dictionary to store layouts for each level
        current_level = None
        layout = []
        base_path = os.path.dirname(__file__)  # Get the directory where the script is located
        
        if getattr(sys, 'frozen', False):   # The application is running in a bundled form (as an .exe or another bundled application)
            file_path = os.path.join(base_path, 'levels_layouts.txt')  # Path to the layouts file
        else:   # The application is running in a normal Python environment (IDE, command line, etc.)
            file_path = os.path.join(base_path, '..', 'levels', 'levels_layouts.txt')
        
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.isdigit():  # Check if the line is a level number
                    if current_level is not None:
                        layouts[current_level] = layout
                    current_level = int(line)
                    layout = []
                else:
                    layout.append(ast.literal_eval(line))   # Convert the string to a list
            if current_level is not None:   # Store the last layout
                layouts[current_level] = layout
        
        return layouts

    def initialize_enemies(self):   # Initialize enemies based on the layout
        for y, row in enumerate(self.layout):
            for x, block_type in enumerate(row):
                if block_type == 5:
                    self.enemies.append(GateDefender(x, y, self.layout, self.block_size, self.collectibles))
                elif block_type == 6:
                    self.enemies.append(CornerDefender(x, y, self.layout, self.block_size, self.collectibles))
                elif block_type == 7:
                    self.enemies.append(HallwayDefender(x, y, self.layout, self.block_size, self.collectibles))

    def calculate_offsets(self):    # Calculate total maze size and offsets once for reuse
        maze_width = len(self.layout[0]) * self.block_size
        maze_height = len(self.layout) * self.block_size
        self.offset_x = (pygame.display.Info().current_w - maze_width) // 2
        self.offset_y = (pygame.display.Info().current_h - maze_height) // 2
    
    def find_player_start(self):    # Find the player start position in the layout
        for y, row in enumerate(self.layout):
            for x, block in enumerate(row):
                if block == 2:
                    return (x, y)
        return None

    def initialize_level(self): # Initialize collectibles and exit positions
        for y, row in enumerate(self.layout):
            for x, value in enumerate(row):
                if value == 3:
                    self.collectibles.append(Collectible(x, y))
                elif value == 4:
                    self.exit_positions.append((x, y))  # Store each exit block position

    def draw(self, screen, player_position, dev_mode):
        view_radius = 200  # View radius in pixels

        # Convert player position to screen coordinates and adjust for the center of the player sprite
        player_screen_x = player_position[0] * self.block_size + self.offset_x + self.block_size // 2
        player_screen_y = player_position[1] * self.block_size + self.offset_y + self.block_size // 2

        for y, row in enumerate(self.layout):
            for x, block in enumerate(row):
                block_screen_x = x * self.block_size + self.offset_x
                block_screen_y = y * self.block_size + self.offset_y

                # Calculate distance from the center of the player to the center of the block
                distance = ((block_screen_x + self.block_size // 2 - player_screen_x) ** 2 + (block_screen_y + self.block_size // 2 - player_screen_y) ** 2) ** 0.5

                if dev_mode or distance <= view_radius:
                    if block == 1:
                        pygame.draw.rect(screen, (255, 255, 255), (block_screen_x, block_screen_y, self.block_size, self.block_size))
                    elif block == 4:
                        color = (0, 255, 0) if self.exit_open else (255, 0, 0)
                        pygame.draw.rect(screen, color, (block_screen_x, block_screen_y, self.block_size, self.block_size))

        for collectible in self.collectibles:
            collectible_screen_x = collectible.x + self.offset_x
            collectible_screen_y = collectible.y + self.offset_y

            # Calculate distance from the player to the collectible
            distance = ((collectible_screen_x + self.block_size // 2 - player_screen_x) ** 2 + (collectible_screen_y + self.block_size // 2 - player_screen_y) ** 2) ** 0.5

            if dev_mode or distance <= view_radius:
                collectible.draw(screen, self.offset_x, self.offset_y)
        
        for enemy in self.enemies:
            enemy.draw(screen, self.offset_x, self.offset_y, player_screen_x, player_screen_y, view_radius, dev_mode)
    
    def check_collision(self, proposed_x, proposed_y):    # Calculate the grid coordinates for all corners of the player's proposed position
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