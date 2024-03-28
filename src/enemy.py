import pygame
import random
from utils import astar

class Enemy:
    def __init__(self, x, y, layout, block_size, collectibles, enemy_type):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.center_x = x  # Set the center position to the initial position
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
            'gate_defenders': (255, 0, 0),
            'corner_defenders': (0, 255, 0),
            'hallway_defenders': (255, 0, 255),
        }
        self.color = self.color_map[enemy_type]
        self.movement_pattern = self.calculate_movement_pattern()
        self.update_counter = 0  # Initialize update counter
        self.update_frequency = 10  # Move every 10th update call

    def calculate_movement_pattern(self):
        # Placeholder for calculating movement pattern
        # This method should be overridden in specific enemy subclasses
        return []

    def update_behavior(self, player_pos, collected_ratio):
        collected_ratio = self.collectibles_collected / self.total_collectibles

        if collected_ratio >= 0.6:
            self.speed = 0.8  # Speed up for stage 3
            # Random direction change logic to be implemented
        elif collected_ratio >= 0.6:
            self.speed = 0.6  # Speed up for stage 2
            # Chase player if within radius
            if self.detect_player_in_radius(player_pos):
                self.path = astar(self.layout, (self.y, self.x), (player_pos[1], player_pos[0]))
        else:
            self.speed = 0.5  # Default speed for stage 1

    def detect_player_in_radius(self, player_pos):
        # Calculate distance to player from original spawn position
        dist_x = abs(self.original_x - player_pos[0])
        dist_y = abs(self.original_y - player_pos[1])
        distance = ((dist_x ** 2) + (dist_y ** 2)) ** 0.5
        return distance <= self.chase_radius

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
        self.movement_index = 0
        self.direction_change_chance = 0.1  # 10% chance to change direction in stage 3

    def calculate_movement_pattern(self):
        # Define the 7x7 square waypoints centered around the spawn position
        pattern = [
            (self.center_x, self.center_y),         # Center
            (self.center_x + 2, self.center_y - 2), # Top-Right
            (self.center_x, self.center_y),         # Center
            (self.center_x - 2, self.center_y - 2), # Top-Left
            (self.center_x, self.center_y),         # Center
            (self.center_x - 2, self.center_y + 2), # Bottom-Left
            (self.center_x, self.center_y),         # Center
            (self.center_x + 2, self.center_y + 2), # Bottom-Right
        ]
        return pattern

    def update_behavior(self, player_pos, collected_ratio, level_layout):
        super().update_behavior(player_pos, collected_ratio)
        self.update_counter += 1
        if self.update_counter % self.update_frequency == 0:
            self.update_counter = 0  # Reset counter on move

            player_grid_pos = player_pos  # Assuming player_pos is already in grid coordinates
            enemy_grid_pos = (int(self.y), int(self.x))

            spawn_to_player_dx = abs(player_grid_pos[0] - int(self.original_x))
            spawn_to_player_dy = abs(player_grid_pos[1] - int(self.original_y))

            if spawn_to_player_dx <= 2 and spawn_to_player_dy <= 2:
                if collected_ratio >= 0.3:
                    # If the player has moved or if no path exists, recalculate the path
                    if not self.path or (self.last_known_player_pos != player_grid_pos):
                        self.last_known_player_pos = player_grid_pos
                        self.path = astar(level_layout, enemy_grid_pos, (player_grid_pos[1], player_grid_pos[0]))
                        print('Chasing player:', self.path)
            else:
                # Clear the path if the player is out of the designated chase area
                self.path = []
                self.last_known_player_pos = None

            if not self.path:
                next_pos = self.movement_pattern[self.movement_index]
                self.move_towards(next_pos)
                if (self.x, self.y) == next_pos:
                    self.movement_index = (self.movement_index + 1) % len(self.movement_pattern)
            else:
                self.follow_path()

    def move_towards(self, target):
        # Simple movement towards a target (one block per update)
        if self.x < target[0]: self.x += self.speed
        elif self.x > target[0]: self.x -= self.speed
        if self.y < target[1]: self.y += self.speed
        elif self.y > target[1]: self.y -= self.speed

    def follow_path(self):
        # Follow the calculated A* path
        if self.path:
            next_step = self.path.pop(0)
            self.y, self.x = next_step[0], next_step[1]  # Adjust for A* returning (y, x)

class CornerDefender(Enemy):
    def calculate_movement_pattern(self):
        # Placeholder for corner defenders' movement pattern
        print("Corner defender movement pattern to be implemented.")

class HallwayDefender(Enemy):
    def calculate_movement_pattern(self):
        # Placeholder for hallway defenders' movement pattern
        print("Hallway defender movement pattern to be implemented.")
