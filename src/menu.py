import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.items = ["Level 1", "Level 2", "Level 3", "Level 4", "Quit Game"]
        self.font = pygame.font.Font(None, 36)
        self.selected = 0  # Index of the selected item

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        # Draw the heading
        heading = self.font.render("Maze Game", True, (255, 255, 255))
        self.screen.blit(heading, (self.screen.get_width() / 2 - heading.get_width() / 2, 50))

        # Draw the menu items
        for index, item in enumerate(self.items):
            if index == self.selected:
                label = self.font.render(item, True, (255, 0, 0))  # Highlight selected item
            else:
                label = self.font.render(item, True, (255, 255, 255))
            self.screen.blit(label, (self.screen.get_width() / 2 - label.get_width() / 2,
                                     150 + index * 50))  # Adjust position based on item index

        pygame.display.flip()

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
        return None  # Return None if the loop ends without a selection