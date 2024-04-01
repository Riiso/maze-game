import pygame
import sys

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.title = "Paused"
        self.title_font = pygame.font.SysFont(None, 48)
        self.items = ["Resume", "Restart Level", "Main Menu"]
        self.font = pygame.font.Font(None, 36)
        self.selected = 0  # Index of the selected item

    def draw(self):
        self.screen.fill((0, 0, 0))

        title_label = self.title_font.render(self.title, True, (255, 255, 255))  # Render title
        self.screen.blit(title_label, (self.screen.get_width() / 2 - title_label.get_width() / 2, self.screen.get_height() / 2 - 100))  # Position title

        for index, item in enumerate(self.items):
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
                        self.running = False
                        return self.selected  # Return the index of the selected item
        return None