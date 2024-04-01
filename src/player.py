import pygame

class Player:
    def __init__(self, x, y, block_size=25):
        self.x = x * block_size  # Convert grid position to pixel position
        self.y = y * block_size
        self.block_size = block_size
        self.speed = 5

    def propose_move(self, dx, dy): # Propose a new position based on movement direction and speed
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        return new_x, new_y

    def draw(self, screen, offset_x, offset_y): # Draw the player
        pygame.draw.rect(screen, (0, 128, 255), (self.x + offset_x, self.y + offset_y, self.block_size, self.block_size))
