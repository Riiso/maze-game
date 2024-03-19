import pygame
import sys

class EndLevelPanel:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.items = ["Next Level", "Main Menu"]
        self.font = pygame.font.Font(None, 36)
        self.selected = 0  # Index of the selected item

    def draw(self):
        self.screen.fill((0, 0, 0))
        for index, item in enumerate(self.items):
            color = (255, 0, 0) if index == self.selected else (255, 255, 255)
            label = self.font.render(item, True, color)
            self.screen.blit(label, (self.screen.get_width() / 2 - label.get_width() / 2,
                                     self.screen.get_height() / 2 - 30 + index * 40))

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
                        self.running = False
                        return self.selected  # Return the selected option index
        return None