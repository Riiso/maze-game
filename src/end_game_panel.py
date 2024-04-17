import pygame
import sys

class EndGamePanel:
    def __init__(self, screen, flag):
        self.screen = screen
        self.running = True
        if flag == 0:
            self.title = "Congratulations for completing the game"
        else:
            self.title = "Congratulations for completing EXTREME CHALLENGE"
        self.title_font = pygame.font.SysFont(None, 48)
        self.items = ["Restart Level", "Main Menu"]
        self.font = pygame.font.SysFont(None, 36)
        self.selected = 0  # Index of the selected item

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_label = self.title_font.render(self.title, True, (255, 255, 255)) # Render title
        title_position = (self.screen.get_width() / 2 - title_label.get_width() / 2, self.screen.get_height() / 2 - 100)    # Position title
        self.screen.blit(title_label, title_position)

        for index, item in enumerate(self.items):   # Draw menu items
            color = (255, 0, 0) if index == self.selected else (255, 255, 255)
            label = self.font.render(item, True, color)
            item_position = (self.screen.get_width() / 2 - label.get_width() / 2, self.screen.get_height() / 2 - 30 + index * 40)
            self.screen.blit(label, item_position)
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
                        return self.selected  # Return the selected option index
            self.draw()
        return None