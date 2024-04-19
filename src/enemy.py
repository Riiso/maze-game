import pygame
import random
import time
from utils import astar


class Enemy:
    def __init__(self, x, y, layout, block_size, collectibles, enemy_type):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.center_x = x
        self.center_y = y
        self.layout = layout
        self.block_size = block_size
        self.collectibles_collected = 0
        self.total_collectibles = len(collectibles)
        self.enemy_type = enemy_type
        self.speed = 0.5
        self.path = []
        self.chase_radius = 100
        self.color_map = {
            'gate_defenders': (128, 0, 0),
            'corner_defenders': (0, 255, 255),
            'hallway_defenders': (255, 0, 255),
        }
        self.color = self.color_map[enemy_type]
        self.update_counter = 0  # Initialize update counter
        self.update_frequency = 10  # Move every 10th update call
        self.last_known_player_pos = None   # Store the last known player position
        self.layout_len_x = len(layout)
        self.layout_len_y = len(layout[0])
        self.movement_index = 0
        self.movement_pattern = self.calculate_movement_pattern()
        self.extreme_chase_mode = False

    def calculate_movement_pattern(self):
        # This method should be overridden in specific enemy subclasses
        return []

    def detect_player(self, player_pos):
        # This method should be overridden in specific enemy subclasses
        return

    def update_behavior(self, player_pos, collected_ratio, level_layout, level_num):
        self.update_counter += 1
        if self.update_counter % self.update_frequency == 0:
            self.update_counter = 0  # Reset counter on move

            player_grid_pos = player_pos
            enemy_grid_pos = (int(self.y), int(self.x))
            
            # Detect player movement or path absence to trigger recalculation
            player_moved = self.last_known_player_pos != player_grid_pos
            path_needs_update = not self.path or player_moved
            
            if level_num != 5:
                if collected_ratio >= 0.3 and self.detect_player(player_pos) and path_needs_update:
                    self.last_known_player_pos = player_grid_pos
                    self.path = astar(level_layout, enemy_grid_pos, (player_grid_pos[1], player_grid_pos[0]), time.time())
                    if self.path and player_moved:
                        # If player is moving, immediately start following the new path
                        self.follow_path()
                if collected_ratio >= 0.6:
                    if random.random() < 0.1:   # 10% chance to change movement pattern
                        self.movement_index = random.randint(0, len(self.movement_pattern) - 1)

                if not self.detect_player(player_pos) or collected_ratio < 0.3: # Clear the path if the player is out of the designated chase area
                    self.path = []
                    self.last_known_player_pos = None

                if not self.path:   # If no path, follow the movement pattern
                    next_pos = self.movement_pattern[self.movement_index]
                    self.move_towards(next_pos)
                    if (self.x, self.y) == next_pos:
                        self.movement_index = (self.movement_index + 1) % len(self.movement_pattern)
                else:
                    self.follow_path()
            else:
                if not self.extreme_chase_mode and collected_ratio >= 0.15:
                    self.extreme_chase_mode = self.detect_player(player_pos)
                if collected_ratio >= 0.15 and self.extreme_chase_mode and path_needs_update:
                    self.last_known_player_pos = player_grid_pos
                    self.path = astar(level_layout, enemy_grid_pos, (player_grid_pos[1], player_grid_pos[0]), time.time())
                    if self.path and player_moved:
                        # If player is moving, immediately start following the new path
                        self.follow_path()
                if collected_ratio >= 0.3:
                    if random.random() < 0.1:   # 10% chance to change movement pattern
                        self.movement_index = random.randint(0, len(self.movement_pattern) - 1)
                
                
                if not self.path:   # If no path, follow the movement pattern
                    next_pos = self.movement_pattern[self.movement_index]
                    self.move_towards(next_pos)
                    if (self.x, self.y) == next_pos:
                        self.movement_index = (self.movement_index + 1) % len(self.movement_pattern)
                else:
                    self.follow_path()

    def move_towards(self, target): # Simple movement towards a target (one block per update)
        if self.x < target[0]: self.x += self.speed
        elif self.x > target[0]: self.x -= self.speed
        if self.y < target[1]: self.y += self.speed
        elif self.y > target[1]: self.y -= self.speed

    def follow_path(self):  # Follow the calculated A* path
        if self.path:
            next_step = self.path.pop(0)
            self.y, self.x = next_step[0], next_step[1]  # Adjust for A* returning (y, x)

    def draw(self, screen, offset_x, offset_y, player_screen_x, player_screen_y, view_radius, dev_mode):
        draw_x = self.x * self.block_size + offset_x
        draw_y = self.y * self.block_size + offset_y

        # Calculate distance from the enemy to the player
        distance = ((draw_x + self.block_size // 2 - player_screen_x) ** 2 + (draw_y + self.block_size // 2 - player_screen_y) ** 2) ** 0.5

        # Draw the enemy only if it's within the view radius or in dev mode
        if dev_mode or distance <= view_radius:
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.block_size, self.block_size))

class GateDefender(Enemy):
    def __init__(self, x, y, layout, block_size, collectibles):
        super().__init__(x, y, layout, block_size, collectibles, 'gate_defenders')
        self.center_x = x
        self.center_y = y

    def calculate_movement_pattern(self):   # Movement pattern for the gate defenders
        pattern = [
            (self.center_x, self.center_y),         # Center
            (self.center_x + 2, self.center_y - 2), # Top-Right
            (self.center_x - 2, self.center_y - 2), # Top-Left
            (self.center_x + 2, self.center_y + 2), # Bottom-Right
            (self.center_x - 2, self.center_y + 2), # Bottom-Left
            (self.center_x, self.center_y),         # Center
            (self.center_x + 2, self.center_y + 2), # Bottom-Right
            (self.center_x + 2, self.center_y - 2), # Top-Right
            (self.center_x - 2, self.center_y + 2), # Bottom-Left
            (self.center_x - 2, self.center_y - 2), # Top-Left
        ]
        return pattern
    
    def detect_player(self, player_pos):
        spawn_to_player_dx = abs(player_pos[0] - int(self.original_x))
        spawn_to_player_dy = abs(player_pos[1] - int(self.original_y))

        # Determine if the player is within the chase radius
        within_chase_radius = spawn_to_player_dx <= 2 and spawn_to_player_dy <= 2
    
        return within_chase_radius

class CornerDefender(Enemy):
    def __init__(self, x, y, layout, block_size, collectibles):
        super().__init__(x, y, layout, block_size, collectibles, 'corner_defenders')

    def calculate_movement_pattern(self):   # Movement pattern for the corner defenders

        if self.x == 1 and self.y == 1:
            pattern = [
            (self.x, self.y),         # Start
            (self.x, self.y + 5),     # 1
            (self.x + 5, self.y),     # 2
            (self.x, self.y),         # Start
            (self.x + 2, self.y + 2), # 3
            (self.x, self.y + 4),     # 1
            (self.x + 4, self.y),     # 2
        ]
        elif self.x == 1 and self.y == self.layout_len_x - 2:
            pattern = [
            (self.x, self.y),         # Start
            (self.x, self.y - 5),     # 1
            (self.x + 5, self.y),     # 2
            (self.x, self.y),         # Start
            (self.x + 2, self.y - 2), # 3
            (self.x, self.y - 4),     # 1
            (self.x + 4, self.y),     # 2
        ]
        elif self.x == self.layout_len_y - 2 and self.y == 1:
            pattern = [
            (self.x, self.y),         # Start
            (self.x, self.y + 5),     # 1
            (self.x - 5, self.y),     # 2
            (self.x, self.y),         # Start
            (self.x - 2, self.y + 2), # 3
            (self.x, self.y + 4),     # 1
            (self.x - 4, self.y),     # 2
        ]
        elif self.x == self.layout_len_y - 2 and self.y == self.layout_len_x - 2:
            pattern = [
            (self.x, self.y),         # Start
            (self.x, self.y - 5),     # 1
            (self.x - 5, self.y),     # 2
            (self.x, self.y),         # Start
            (self.x - 2, self.y - 2), # 3
            (self.x, self.y - 4),     # 1
            (self.x - 4, self.y),     # 2
        ]
            
        return pattern
    
    def detect_player(self, player_pos):
        spawn_to_player_dx = abs(player_pos[0] - int(self.original_x))
        spawn_to_player_dy = abs(player_pos[1] - int(self.original_y))

        # Determine if the player is within the chase radius
        within_chase_radius = spawn_to_player_dx <= 4 and spawn_to_player_dy <= 4
    
        return within_chase_radius

class HallwayDefender(Enemy):
    def __init__(self, x, y, layout, block_size, collectibles):
        super().__init__(x, y, layout, block_size, collectibles, 'hallway_defenders')
    
    def calculate_movement_pattern(self):   # Movement pattern for the hallway defenders

        if self.x == self.layout_len_y - 3:
            pattern = [
            (self.x, self.y),          # Start
            (self.x - 1, self.y - 1),  # 1
            (self.x - 17, self.y - 1), # 2
            (self.x - 18, self.y),     # 3
            (self.x - 17, self.y + 1), # 4
            (self.x - 1, self.y + 1),  # 5
        ]
        else:
            pattern = [
            (self.x, self.y),          # Start
            (self.x + 1, self.y + 1),  # 1
            (self.x + 17, self.y + 1), # 2
            (self.x + 18, self.y),     # 3
            (self.x + 17, self.y - 1), # 4
            (self.x + 1, self.y - 1),  # 5
        ]
        
        return pattern

    def detect_player(self, player_pos):
        if self.original_x > 35:
            if player_pos[0] >= int(self.original_x) - 19 and player_pos[0] <= int(self.original_x) + 1 and player_pos[1] >= int(self.original_y) - 1 and player_pos[1] <= int(self.original_y) + 1:
                return True
        else:
            if player_pos[0] <= int(self.original_x) + 19 and player_pos[0] >= int(self.original_x) -1 and player_pos[1] >= int(self.original_y) - 1 and player_pos[1] <= int(self.original_y) + 1:
                return True
        
        return False