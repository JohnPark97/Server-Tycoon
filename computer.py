import pygame
import os
from button import Button  # Make sure you've defined this class properly


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
        self.active_category = list(menus.keys())[0]
        self.button_img = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png'))
        self.monitor_img = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'monitor.png'))
        self.menu_font = pygame.font.SysFont(FONT, 17)
        self.total_font = pygame.font.SysFont(FONT, 25)
        self.util_font = pygame.font.SysFont(FONT, 15)

        self.all_buttons = []  # A list to hold all types of buttons
        self._load_all_buttons()

    def _load_all_buttons(self):
        self._load_tabs()
        self._load_utility_buttons()

    def _load_tabs(self):
        x_coord = SCREEN_WIDTH - MONITOR_WIDTH + 20
        for category in self.menus.keys():
            self.all_buttons.append(Button(x_coord, CATEGORY_TOP_OFFSET, 100, 35, category, self.menu_font, 'category'))
            x_coord += CATEGORY_X_OFFSET + 100  # Button width is 100
            
            self._load_menus(category)

    def _load_menus(self, category):
        calc_screen_x = SCREEN_WIDTH - MONITOR_WIDTH // 2
        button_width = 100
        button_height = 100
        button_x = SCREEN_WIDTH - MONITOR_WIDTH + 20
        button_y = BUTTON_TOP_OFFSET
            
        for menu in self.menus[category]:
            # Check if the next button will overflow the calc_screen
            if button_x + button_width > calc_screen_x:
                # Reset button_x and update button_y to move to the next line
                button_x = SCREEN_WIDTH - MONITOR_WIDTH + 20
                button_y += button_height + BUTTON_X_OFFSET  # Adjust this as needed
            
            self.all_buttons.append(Button(button_x, button_y, button_width, button_height, menu.name, self.menu_font, 'menu', category))
            button_x += BUTTON_X_OFFSET + button_width

    def _load_utility_buttons(self):
        # Create utility buttons
        save_order_button = Button(SCREEN_WIDTH - MONITOR_WIDTH //2 , 460, 100, 75, "Save Order", self.menu_font, 'utility')
        print_bill_button = Button(SCREEN_WIDTH - MONITOR_WIDTH //2 + save_order_button.width, 460, 100, 75, "Print Bill", self.menu_font, 'utility')
        self.all_buttons.append(save_order_button)
        self.all_buttons.append(print_bill_button)

    def draw_monitor(self):
        scaled_monitor = pygame.transform.scale(self.monitor_img, (MONITOR_WIDTH, MONITOR_HEIGHT))
        self.screen.blit(scaled_monitor, (SCREEN_WIDTH - MONITOR_WIDTH, 0))

    def draw_menu(self):
        # Loop through and draw only the 'menu' buttons that belong to the active category
        for button in self.all_buttons:
            if button.type == 'menu' and button.category == self.active_category:
                button.draw(self.screen)

    def draw_tabs(self):
        # Loop through and draw only the 'category' buttons
        for button in self.all_buttons:
            if button.type == 'category':
                button.draw(self.screen)
            
    def draw_calc_screen(self):
        rect_color = (200, 200, 200)
        rect_x_offset = 4  # Offset from the right side of the screen
        rect_x = SCREEN_WIDTH - MONITOR_WIDTH //2 
        
        rect_height = MONITOR_HEIGHT - 150
        rect_y_offset = 4  # Offset from the top of the screen
        rect_y = 0  
        
        rect_width = MONITOR_WIDTH // 2  # Filling the right half of the screen

        pygame.draw.rect(self.screen, rect_color, (rect_x - rect_x_offset, rect_y + rect_y_offset, rect_width, rect_height))

        menu_font = self.menu_font
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
        total_y = 400
        self.screen.blit(total_surface, (menu_x_offset, total_y))

    def draw_buttons(self):
        for button in self.all_buttons:
            if button.type == 'menu' and button.category == self.active_category:
                button.draw(self.screen)
            elif button.type == 'category' or button.type == 'utility':
                button.draw(self.screen)

    def handle_button_click(self, x, y, customer, CUSTOMER_ORDER_CONFIRM_EVENT):
        for button in self.all_buttons:
            if button.is_clicked(x, y):
                if button.type == 'utility':
                    if button.text == "Save Order":
                        self.handle_order_save(customer, CUSTOMER_ORDER_CONFIRM_EVENT)
                    elif button.text == "Print Bill":
                        print("Printing Bill...")
                    return True
                elif button.type == 'category':
                    self.active_category = button.text
                elif button.type == 'menu':
                    if button.category == self.active_category:
                        clicked_menu = next(menu for menu in self.menus[button.category] if menu.name == button.text)
                        self.clicked_menus.append(clicked_menu)

    def check_order(self, customer):
        # Check if clicked_menus matches the order_list in the Customer instance
        return sorted(self.clicked_menus, key=lambda x: x.name) == sorted(customer.order_list, key=lambda x: x.name)
    
    def handle_order_save(self, customer, CUSTOMER_ORDER_CONFIRM_EVENT):
        pygame.event.post(pygame.event.Event(CUSTOMER_ORDER_CONFIRM_EVENT, got_order_right=self.check_order(customer)))

    def draw(self):
        self.draw_monitor()
        self.draw_calc_screen()

        self.draw_buttons()