import pygame

class Collectible:
    def __init__(self, x, y, block_size=25):
        self.x = x * block_size
        self.y = y * block_size
        self.block_size = block_size
        self.collected = False

    def draw(self, screen, offset_x, offset_y):
        if not self.collected:
            pygame.draw.rect(screen, (255, 215, 0), (self.x + offset_x, self.y + offset_y, self.block_size, self.block_size))