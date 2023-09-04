import pygame
import os

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MONITOR_WIDTH = 850
MONITOR_HEIGHT = 600
BUTTON_X_OFFSET = 10
BUTTON_TOP_OFFSET = 70
CATEGORY_TOP_OFFSET = 25
CATEGORY_X_OFFSET = 10
FONT = 'Arial Black'

class Computer:
    def __init__(self, screen, menus):
        self.screen = screen
        self.menus = menus
        self.clicked_menus = []
        self.visible_buttons = {}
        self.active_category = list(menus.keys())[0]
        self.button_img = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png'))
        self.monitor_img = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'monitor.png'))
        self.menu_font = pygame.font.SysFont(FONT, 20)
        self.total_font = pygame.font.SysFont(FONT, 25)
        
    def _draw_button_with_text(self, x, y, text, scale_x, scale_y):
        scaled_button = pygame.transform.scale(self.button_img, (scale_x, scale_y))

        # Draw the actual button
        self.screen.blit(scaled_button, (x, y))
        
        # Draw the text
        text_surface = self.menu_font.render(text, False, (0, 0, 0))
        text_x = x + scaled_button.get_width() // 2 - text_surface.get_width() // 2
        text_y = y + scaled_button.get_height() // 2 - text_surface.get_height() // 2
        self.screen.blit(text_surface, (text_x, text_y))

# Make sure to include this updated method in your Computer class.
    def draw_monitor(self):
        scaled_monitor = pygame.transform.scale(self.monitor_img, (MONITOR_WIDTH, MONITOR_HEIGHT))
        self.screen.blit(scaled_monitor, (SCREEN_WIDTH - MONITOR_WIDTH, 0))

    def draw_menu(self):
        x_coord = SCREEN_WIDTH - MONITOR_WIDTH + 20
        for menu in self.menus[self.active_category]:
            self._draw_button_with_text(x_coord, BUTTON_TOP_OFFSET, menu.name, 100, 100)
            x_coord += BUTTON_X_OFFSET + self.button_img.get_width()

    def draw_tabs(self):
        x_coord = SCREEN_WIDTH - MONITOR_WIDTH + 20
        for category in self.menus.keys():
            self._draw_button_with_text(x_coord, CATEGORY_TOP_OFFSET, category, 100, 35)
            self.visible_buttons[category] = (self.button_img, (x_coord, CATEGORY_TOP_OFFSET))
            x_coord += CATEGORY_X_OFFSET + self.button_img.get_width()
            
    def draw_calc_screen(self):
        rect_color = (200, 200, 200)
        rect_x_offset = 4  # Offset from the right side of the screen
        rect_x = SCREEN_WIDTH - MONITOR_WIDTH //2 
        
        rect_height = MONITOR_HEIGHT - 100
        rect_y_offset = 4  # Offset from the top of the screen
        rect_y = 0  
        
        rect_width = MONITOR_WIDTH // 2  # Filling the right half of the screen

        pygame.draw.rect(self.screen, rect_color, (rect_x - rect_x_offset, rect_y + rect_y_offset, rect_width, rect_height))

        # Render the names of clicked menus vertically
        FONT = 'Arial Black'
        menu_font = pygame.font.SysFont(FONT, 20)
        menu_x_offset = rect_x + 10  # A bit of padding from the left of the rectangle
        menu_y_offset = 5  # A bit of padding from the top of the rectangle

        total_price = 0.0  # Initialize

        for menu in self.clicked_menus:
            text_surface = menu_font.render(menu.name, False, (0, 0, 0))
            self.screen.blit(text_surface, (menu_x_offset, menu_y_offset))
            menu_y_offset += text_surface.get_height() + 10  # Move the y-coordinate for the next menu
            
            total_price += menu.price  # Add the price of the menu to the total

        # Display the total price at the bottom of calc_screen
        total_font = pygame.font.SysFont(FONT, 25)
        total_text = f"Total: ${total_price:.2f}"
        total_surface = total_font.render(total_text, False, (0, 0, 0))
        total_y = 450
        self.screen.blit(total_surface, (menu_x_offset, total_y))

    def handle_menu_btn_click(self, x, y):
        button_x = SCREEN_WIDTH - MONITOR_WIDTH + 20
        button_y = BUTTON_TOP_OFFSET
        
        for menu in self.menus[self.active_category]:
            button_width, button_height = self.button_img.get_size()
            if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                self.clicked_menus.append(menu)
                return True  # A button was clicked
                
            button_x += self.button_img.get_width() + 10
        return False  # No button was clicked

    def handle_category_btn_click(self, x, y, CATEGORY_BUTTON_CLICKED):
        for category, (button_surface, coord) in self.visible_buttons.items():
            button_x, button_y = coord
            button_width, button_height = button_surface.get_size()

            if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                self.active_category = category  # Update the active category in the Computer instance
                custom_event = pygame.event.Event(CATEGORY_BUTTON_CLICKED, category=category)
                pygame.event.post(custom_event)
                return True  # A button was clicked
        return False  # No button was clicked
