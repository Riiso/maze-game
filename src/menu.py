import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.heading = "Maze Game"
        self.heading_font = pygame.font.SysFont(None, 60)
        self.items = ["Level 1", "Level 2", "Level 3", "Level 4", "Quit Game"]
        self.font = pygame.font.Font(None, 36)
        self.selected = 0  # Index of the selected item

    def draw(self):
        self.screen.fill((0, 0, 0))

        heading = self.heading_font.render(self.heading, True, (255, 255, 255)) # Render heading
        self.screen.blit(heading, (self.screen.get_width() / 2 - heading.get_width() / 2, 250))  # Position heading

        for index, item in enumerate(self.items):   # Draw menu items
            color = (255, 0, 0) if index == self.selected else (255, 255, 255)
            label = self.font.render(item, True, color)
            self.screen.blit(label, (self.screen.get_width() / 2 - label.get_width() / 2,
                                     self.screen.get_height() / 2 - 30 + index * 40))
        pygame.display.flip()   # Update the display

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == pygame.K_RETURN:
                        if self.items[self.selected] == "Quit Game":
                            pygame.quit()
                            sys.exit()
                        else:
                            self.running = False
                            return self.selected  # Return the selected level index
            self.draw()
        return None