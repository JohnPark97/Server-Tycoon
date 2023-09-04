import pygame

class GameClock:
    def __init__(self, screen, total_time):
        self.screen = screen
        self.total_time = total_time  # The total time for a round in seconds
        self.time_left = self.total_time  # The time left in the current round
        self.font = pygame.font.SysFont("Comic Sans MS", 40)
        
        # Record the start time
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        # Calculate how many seconds have passed
        self.seconds_passed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        # Calculate the time left in the round
        self.time_left = self.total_time - self.seconds_passed

    def draw(self):
        # Create a text surface
        time_surface = self.font.render(f"Time Left: {self.time_left}s", False, (0, 0, 0))
        
        # Calculate the x-coordinate based on the screen's width and the width of the text surface
        x = self.screen.get_width() - time_surface.get_width() - 10  # 10 pixels padding from the right
        
        # Calculate the y-coordinate based on the screen's height and the height of the text surface
        y = self.screen.get_height() - time_surface.get_height() - 10  # 10 pixels padding from the bottom
    
        # Draw the text surface
        self.screen.blit(time_surface, (x, y))

    def has_time_left(self):
        return self.time_left > 0
    
    