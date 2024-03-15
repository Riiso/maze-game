import pygame
import sys
from player import Player
from level import Level

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
        self.level = Level()  # Load Level 1
        px, py = self.level.player_start_pos
        self.player = Player(px, py)  # Initialize the player at the start position found in the level

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Quit the game with ESC
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
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.level.draw(self.screen)  # Draw the level
        self.player.draw(self.screen, self.level.offset_x, self.level.offset_y)  # Draw the player
        pygame.display.flip()  # Update the display

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Maintain 60 FPS

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()