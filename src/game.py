import pygame
import sys
from player import Player  # Ensure you have a player.py file with the Player class defined

class Game:
    def __init__(self):
        pygame.init()
        # Get the current screen resolution to set the game to full screen
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        # Set the game to run in full screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        # Initialize the player with an adjusted starting position
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.player_speed = 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to quit the game
                    self.running = False

    def update(self):
        # Update game state based on keypresses
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
        self.screen.fill((0, 0, 0))  # Clear the screen with black
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
