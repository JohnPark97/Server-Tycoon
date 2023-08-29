import pygame
import os
import json

from menu import Menu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 550

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BACKGROUND = (224, 207, 158)

# Define the custom event type
CATEGORY_BUTTON_CLICKED = pygame.USEREVENT + 1

# Global variable to store all the visible buttons and their coordinates
visible_buttons = {}
active_category = None  # Variable to store the currently active category

clicked_menus = []


def load_prices():
    with open('assets/menu/price.json') as file:
        return json.load(file)

def load_menu():
    # e.x. { "sashimi": [], "nigiri": [] ...}
    menu_map = {}
    base_path = 'assets/menu'
    prices = load_prices()
    
    for dirpath, dirnames, filenames in os.walk(base_path):
        for filename in filenames:
            if filename.endswith('.png'):
                # Extract name without extension
                name = os.path.splitext(filename)[0]
                
                # Get the parent directory of the PNG
                category = os.path.basename(dirpath)
                
                # Add the PNG to the map
                if category not in menu_map:
                    menu_map[category] = []

                image = pygame.image.load(os.path.join(dirpath, filename))
                price = prices[category][name]
                menu = Menu(name, price, image)

                menu_map[category].append(menu)

    return menu_map


def draw_tabs(screen: pygame.Surface, menus: dict, button: pygame.Surface, CATEGORY_X_OFFSET: int):
    global active_category  # Declare global to modify it

    FONT = 'Arial Black'
    menu_font = pygame.font.SysFont(FONT, 20)
    CATEGORY_TOP_OFFSET = 25

    # Set the first category as the default active category
    if active_category is None:
        active_category = list(menus.keys())[0]

    for category in menus.keys():
        category_coord = (CATEGORY_X_OFFSET, CATEGORY_TOP_OFFSET)
        category_button = pygame.transform.scale(button, (button.get_width(), button.get_height() // 3))

        screen.blit(category_button, category_coord)
        
        category_surface = menu_font.render(category, False, (0, 0, 0))
        cat_text_x = category_coord[0] + category_button.get_width() // 2 - category_surface.get_width() // 2
        cat_text_y = category_coord[1] + category_button.get_height() // 2 - category_surface.get_height() // 2
        screen.blit(category_surface, (cat_text_x, cat_text_y))

        # Save to the global visible_buttons map
        visible_buttons[category] = (category_button, category_coord)

        CATEGORY_X_OFFSET += category_button.get_width() + 10

def draw_menu(screen: pygame.Surface, menus: dict, active_category: str):
    BUTTON_X_OFFSET = 35
    BUTTON_TOP_OFFSET = 70
    button = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png'))
    FONT = 'Arial Black'
    menu_font = pygame.font.SysFont(FONT, 20)

    for menu in menus[active_category]:
        coord = (BUTTON_X_OFFSET, BUTTON_TOP_OFFSET)
        screen.blit(button, coord)
        
        text_surface = menu_font.render(menu.name, False, (0, 0, 0))
        text_x = coord[0] + button.get_width() // 2 - text_surface.get_width() // 2
        text_y = coord[1] + button.get_height() // 2 - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))
        
        BUTTON_X_OFFSET += button.get_width() + 10

def draw_calc_screen(screen: pygame.Surface, clicked_menus):
    # Draw the rectangle on the right side
    rect_color = (200, 200, 200)  # Grey color
    rect_x = SCREEN_WIDTH // 2  # Starting at the midpoint of the screen width
    
    rect_height = SCREEN_HEIGHT // 1.5  # 1/4 of the screen height
    rect_y = (SCREEN_HEIGHT - rect_height) // 2  # Centering vertically
    
    rect_width = SCREEN_WIDTH // 2  # Filling the right half of the screen

    pygame.draw.rect(screen, rect_color, (rect_x - 26, rect_y - 68, rect_width, rect_height))

    # Render the names of clicked menus vertically
    FONT = 'Arial Black'
    menu_font = pygame.font.SysFont(FONT, 15)
    menu_x_offset = rect_x + 10  # A bit of padding from the left of the rectangle
    menu_y_offset = 35  # A bit of padding from the top of the rectangle

    total_price = 0.0  # Initialize the total price

    for menu in clicked_menus:
        text_surface = menu_font.render(menu.name, False, (0, 0, 0))
        screen.blit(text_surface, (menu_x_offset, menu_y_offset))
        menu_y_offset += text_surface.get_height() + 10  # Move the y-coordinate for the next menu
        
        total_price += menu.price  # Add the price of the menu to the total

    # Display the total price at the bottom of calc_screen
    total_font = pygame.font.SysFont(FONT, 20)
    total_text = f"Total: ${total_price:.2f}"
    total_surface = total_font.render(total_text, False, (0, 0, 0))
    total_y = 360
    screen.blit(total_surface, (menu_x_offset, total_y))
                

def draw_monitor(screen: pygame.Surface):
    monitor = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'monitor.png'))
    monitor = pygame.transform.scale(monitor, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(monitor, (0, 0))

def draw_background(screen: pygame.Surface):
    screen.fill(BACKGROUND)


def update_screen(screen: pygame.Surface, menus: dict, active_category: str):
    draw_background(screen)
    draw_monitor(screen)
    draw_calc_screen(screen, clicked_menus)  # Pass clicked_menus
    draw_tabs(screen, menus, pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png')), 35)
    draw_menu(screen, menus, active_category)

    pygame.display.flip()

def main():
    global active_category  # Declare global to modify it
    global clicked_menus  # Declare global to modify it

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Server Tycoon")

    run = True
    menus = load_menu()

    # Set the first category as the default active category
    active_category = list(menus.keys())[0]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check for category button clicks
                for category, (button_surface, coord) in visible_buttons.items():
                    button_x, button_y = coord
                    button_width, button_height = button_surface.get_size()

                    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                        active_category = category  # Update the active category
                        custom_event = pygame.event.Event(CATEGORY_BUTTON_CLICKED, category=category)
                        pygame.event.post(custom_event)
                
                # Check for menu button clicks
                BUTTON_X_OFFSET = 35
                BUTTON_TOP_OFFSET = 70
                button = pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png'))
                for menu in menus[active_category]:
                    button_x, button_y = BUTTON_X_OFFSET, BUTTON_TOP_OFFSET
                    button_width, button_height = button.get_size()
                    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                        clicked_menus.append(menu)
                    BUTTON_X_OFFSET += button.get_width() + 10

                print(clicked_menus)  # For debugging

            elif event.type == CATEGORY_BUTTON_CLICKED:
                print(f"Category button clicked for category: {event.category}")

        update_screen(screen, menus, active_category)  # Pass the active category

    pygame.quit()

if __name__ == "__main__":
    main()