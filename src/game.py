import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Fill the screen with black
            # Update game state and draw everything
            pygame.display.flip()  # Update the full display Surface to the screen

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()