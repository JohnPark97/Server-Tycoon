import pygame
import os
from common import wrap_text

class Button:
    def __init__(self, x, y, width, height, text, font, button_type, category=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.type = button_type  # 'menu', 'category', 'utility', etc.
        self.category = category if button_type == 'menu' else None  # Only set if type is 'menu'
        self.image = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png'))
        self.image = pygame.transform.scale(self.image, (width, height))

    def is_clicked(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        lines = wrap_text(self.text, self.font, self.width)  # Assume wrap_text is available

        # Calculate the total height of all lines
        total_height = 0
        for line in lines:
            text_surface = self.font.render(line.strip(), False, (0, 0, 0))
            total_height += text_surface.get_height()

        # Calculate the starting y-coordinate for the text to be centered
        text_y_start = self.y + (self.height - total_height) // 2

        total_line_height = 0
        for line in lines:
            text_surface = self.font.render(line.strip(), False, (0, 0, 0))
            text_x = self.x + self.width // 2 - text_surface.get_width() // 2
            text_y = text_y_start + total_line_height
            screen.blit(text_surface, (text_x, text_y))
            total_line_height += text_surface.get_height()


