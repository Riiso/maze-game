import pygame

class Player:
    def __init__(self, x, y, block_size=25):
        self.x = x * block_size  # Convert grid position to pixel position
        self.y = y * block_size
        self.block_size = block_size
        self.speed = 5

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(screen, (0, 128, 255),
                         (self.x + offset_x, self.y + offset_y,
                          self.block_size, self.block_size))
