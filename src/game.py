import pygame
import sys
import threading
import utils
from player import Player
from level import Level
from menu import Menu
from pause_menu import PauseMenu
from end_level_panel import EndLevelPanel
from game_over_panel import GameOverPanel
from end_game_panel import EndGamePanel

class Game:
    def __init__(self):
        pygame.init()
        self.setup_screen() # Set up the game screen
        self.clock = pygame.time.Clock()    # Initialize the clock for controlling the frame rate
        self.state = "MAIN_MENU"  # Initial state
        self.dev_mode = False  # Set to True to enable developer mode for easier testing
        self.hint_path = []
        self.show_hint = False
        self.hint_start_time = 0
        self.hint_color = (0, 0, 0)

    def setup_screen(self):
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)   # Set the game to run in full screen

    def show_main_menu(self):
        menu = Menu(self.screen)
        selected_level = menu.run()
        if selected_level is None:  # If "Quit Game" is selected or the window is closed
            self.exit_game()
        else:
            self.start_level(selected_level + 1)  # Transition to starting the selected level

    def start_level(self, level_num):   # Start the game at the specified level
        self.level = Level(level_num, self.dev_mode)
        px, py = self.level.player_start_pos
        self.player = Player(px, py)
        self.state = "RUNNING"

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def pause_game(self):
        pause_menu = PauseMenu(self.screen)
        while self.state == "PAUSED":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        pause_menu.selected = (pause_menu.selected + 1) % len(pause_menu.items)
                    elif event.key == pygame.K_UP:
                        pause_menu.selected = (pause_menu.selected - 1) % len(pause_menu.items)
                    elif event.key == pygame.K_RETURN:
                        selected_option = pause_menu.selected
                        if selected_option == 0:  # Resume
                            self.state = "RUNNING"
                        elif selected_option == 1:  # Restart Level
                            self.start_level(self.level.level_num)
                            self.state = "RUNNING"
                        elif selected_option == 2:  # Main Menu
                            self.state = "MAIN_MENU"
                            self.show_main_menu()
                        break
            pause_menu.draw()
            pygame.display.flip()   # Update the display

    def show_game_over_panel(self):
        game_over_panel = GameOverPanel(self.screen)
        while self.state == "GAME_OVER":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        game_over_panel.selected = (game_over_panel.selected + 1) % len(game_over_panel.items)
                    elif event.key == pygame.K_UP:
                        game_over_panel.selected = (game_over_panel.selected - 1) % len(game_over_panel.items)
                    elif event.key == pygame.K_RETURN:
                        selected_option = game_over_panel.selected
                        if selected_option == 0:  # Restart Level
                            self.start_level(self.level.level_num)
                            self.state = "RUNNING"
                        elif selected_option == 1:  # Main Menu
                            self.state = "MAIN_MENU"
                            self.show_main_menu()
                        break
            game_over_panel.draw()
            pygame.display.flip()   # Update the display

    def show_end_level_panel(self):
        end_level_panel = EndLevelPanel(self.screen)
        while self.state == "END_LEVEL":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        end_level_panel.selected = (end_level_panel.selected + 1) % len(end_level_panel.items)
                    elif event.key == pygame.K_UP:
                        end_level_panel.selected = (end_level_panel.selected - 1) % len(end_level_panel.items)
                    elif event.key == pygame.K_RETURN:
                        selected_option = end_level_panel.selected
                        if selected_option == 0:  # Next Level
                            self.start_level(self.level.level_num + 1)
                            self.state = "RUNNING"
                        elif selected_option == 1:  # Main Menu
                            self.state = "MAIN_MENU"
                            self.show_main_menu()
                        break
            end_level_panel.draw()
            pygame.display.flip()   # Update the display

    def show_end_game_panel(self):
        end_game_panel = EndGamePanel(self.screen)
        while self.state == "END_GAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        end_game_panel.selected = (end_game_panel.selected + 1) % len(end_game_panel.items)
                    elif event.key == pygame.K_UP:
                        end_game_panel.selected = (end_game_panel.selected - 1) % len(end_game_panel.items)
                    elif event.key == pygame.K_RETURN:
                        selected_option = end_game_panel.selected
                        if selected_option == 0:  # Restart Level
                            self.start_level(self.level.level_num)
                            self.state = "RUNNING"
                        elif selected_option == 1:  # Main Menu
                            self.state = "MAIN_MENU"
                            self.show_main_menu()
                        break
            end_game_panel.draw()
            pygame.display.flip()   # Update the display

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self.state == "RUNNING":  # Pause game if 'P' is pressed
                    self.state = "PAUSED"
                elif event.key == pygame.K_d:  # Toggle developer mode with 'D'
                    self.dev_mode = not self.dev_mode
                elif event.key == pygame.K_a:   # A* pathfinding
                    self.calculate_hint_path(method="astar")
                elif event.key == pygame.K_b:   # Dijkstra pathfinding
                    self.calculate_hint_path(method="dijkstra")

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1

        # Calculate the player's proposed position based on movement direction
        proposed_x, proposed_y = self.player.propose_move(dx, dy)

        # Adjust check to consider the whole player area
        if not self.level.check_collision(proposed_x + self.level.offset_x, proposed_y + self.level.offset_y):
            self.player.x = proposed_x
            self.player.y = proposed_y

        self.check_enemy_collisions()   # Check for enemy collisions
        self.check_collectible_collision()  # Check for collectible collisions
        
        if self.show_hint and (pygame.time.get_ticks() - self.hint_start_time > 3000):  # Show hint for 3 seconds
            self.show_hint = False

        # Update enemies
        player_grid_pos = (self.player.x // self.level.block_size, self.player.y // self.level.block_size)
        collected_ratio = len([c for c in self.level.collectibles if c.collected]) / len(self.level.collectibles)
        for enemy in self.level.enemies:
            enemy.update_behavior(player_grid_pos, collected_ratio, self.level.layout)
    
    def calculate_hint_path(self, method):
        # Reset the hint_path before starting the new calculation
        self.hint_path = []
        self.show_hint = False  # Temporarily disable showing the hint until the new path is calculated
        
        # Convert player's and collectibles current positions to grid coordinates
        player_grid_pos = (self.player.y // self.level.block_size, self.player.x // self.level.block_size)
        collectibles_grid_pos = [(collectible.y // self.level.block_size, collectible.x // self.level.block_size) for collectible in self.level.collectibles if not collectible.collected]
        
        middle_exit_pos = self.level.exit_positions[len(self.level.exit_positions) // 2]
        exit_grid_pos = (middle_exit_pos[1], middle_exit_pos[0])
        
        def handle_path_result(path):   # Callback function to handle the path result
            self.hint_path = path
            if path:
                self.show_hint = True
            self.hint_start_time = pygame.time.get_ticks()

        if method == "astar":
            # Start a new thread for A* pathfinding
            thread = threading.Thread(target = utils.astar_threaded, args=(self.level.layout, player_grid_pos, collectibles_grid_pos, exit_grid_pos, handle_path_result))
            thread.start()
            self.hint_color = (128, 0, 128)
        elif method == "dijkstra":
            # Start a new thread for Dijkstra pathfinding
            thread = threading.Thread(target = utils.dijkstra_threaded, args=(self.level.layout, player_grid_pos, collectibles_grid_pos, exit_grid_pos, handle_path_result))
            thread.start()
            self.hint_color = (0, 128, 128)

    def check_enemy_collisions(self):   # Check for collisions between the player and enemies
        player_rect = pygame.Rect(self.player.x, self.player.y, self.level.block_size, self.level.block_size)
        for enemy in self.level.enemies:
            enemy_rect = pygame.Rect(enemy.x * self.level.block_size, enemy.y * self.level.block_size, self.level.block_size, self.level.block_size)
            if player_rect.colliderect(enemy_rect):
                self.state = "GAME_OVER"
                break

    def check_collectible_collision(self):  # Check for collisions between the player and collectibles
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.block_size, self.player.block_size)
        for collectible in self.level.collectibles:
            collectible_rect = pygame.Rect(collectible.x, collectible.y, collectible.block_size, collectible.block_size)
            if not collectible.collected and player_rect.colliderect(collectible_rect):
                collectible.collected = True
                break
        if all(collectible.collected for collectible in self.level.collectibles):   # Open the exit if all collectibles are collected
            self.level.exit_open = True

        if self.level.exit_open:
            for exit_x, exit_y in self.level.exit_positions:
                exit_rect = pygame.Rect(exit_x * self.level.block_size, exit_y * self.level.block_size, self.level.block_size, self.level.block_size)
                if player_rect.colliderect(exit_rect):
                    if self.level.level_num == 4:   # Check if this is the last level
                        self.state = "END_GAME"
                    else:
                        self.state = "END_LEVEL"
                    break

    def draw(self): # Draw the game elements on the screen
        player_position = (self.player.x / self.level.block_size, self.player.y / self.level.block_size)
        self.screen.fill((0, 0, 0))
        
        font = pygame.font.SysFont("Arial", 24)
        collected_count = len([c for c in self.level.collectibles if c.collected])
        total_count = len(self.level.collectibles)
        text_surface = font.render(f"Collectibles: {collected_count}/{total_count}", True, (255, 255, 255))
        self.screen.blit(text_surface, (20, 20))

        legend = [
            "P - Pause game",
            "A - Show hint (A*)",
            "B - Show hint (Dijkstra)"
        ]
        y_offset = self.screen_height - (len(legend) * 30)  # Position the legend at the bottom of the screen
        for i, line in enumerate(legend):
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, y_offset + (i * 30)))
        
        if self.show_hint and self.hint_path:
            path_rect_width = self.level.block_size // 4  # Make the path width 1/4th of the block size for a thinner rectangle
            path_rect_height = self.level.block_size // 4
            
            # Get player's screen position
            player_screen_x = player_position[0] * self.level.block_size + self.level.offset_x
            player_screen_y = player_position[1] * self.level.block_size + self.level.offset_y
            view_radius = 200  # View radius in pixels

            for row, column in self.hint_path:
                hint_point_screen_x = column * self.level.block_size + self.level.offset_x + (self.level.block_size - path_rect_width) // 2 # Center the hint path point
                hint_point_screen_y = row * self.level.block_size + self.level.offset_y + (self.level.block_size - path_rect_height) // 2
                
                # Calculate distance from the player to this point of the hint path
                distance = ((hint_point_screen_x - player_screen_x) ** 2 + (hint_point_screen_y - player_screen_y) ** 2) ** 0.5

                # Draw the hint path point if within view radius or if in developer mode
                if self.dev_mode or distance <= view_radius:
                    pygame.draw.rect(self.screen, self.hint_color, (hint_point_screen_x, hint_point_screen_y, path_rect_width, path_rect_height))   # Draw the hint path point

        self.level.draw(self.screen, player_position, self.dev_mode)  # Draw the level
        self.player.draw(self.screen, self.level.offset_x, self.level.offset_y)  # Draw the player

        pygame.display.flip()  # Update the display
    
    def run(self):
        while True:
            if self.state == "MAIN_MENU":
                self.show_main_menu()
            elif self.state == "RUNNING":
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)  # Maintain 60 FPS
            elif self.state == "PAUSED":
                self.pause_game()
            elif self.state == "GAME_OVER":
                self.show_game_over_panel()
            elif self.state == "END_LEVEL":
                self.show_end_level_panel()
            elif self.state == "END_GAME":
                self.show_end_game_panel()

if __name__ == "__main__":
    game = Game()
    game.run()