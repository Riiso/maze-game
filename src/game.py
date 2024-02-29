import pygame
import sys
from player import Player  # Make sure to have a player.py file with the Player class

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        # Initialize the player with starting position
        self.player = Player(400, 300)
        self.player_speed = 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Update game state
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        # Draw the player (replace with player's draw method if available)
        pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(self.player.x, self.player.y, 50, 50))
        pygame.display.flip()  # Update the screen

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Cap the game at 60 frames per second

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()