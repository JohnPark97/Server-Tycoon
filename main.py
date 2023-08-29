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


def draw_background(screen: pygame.Surface):
    screen.fill(BACKGROUND)

def update_screen(screen: pygame.Surface, menus: dict, active_category: str):
    draw_background(screen)
    draw_tabs(screen, menus, pygame.image.load(os.path.join('assets', 'decors', 'computer', 'button.png')), 35)
    draw_menu(screen, menus, active_category)

    pygame.display.flip()

def main():
    global active_category  # Declare global to modify it

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

                for category, (button_surface, coord) in visible_buttons.items():
                    button_x, button_y = coord
                    button_width, button_height = button_surface.get_size()

                    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                        active_category = category  # Update the active category
                        custom_event = pygame.event.Event(CATEGORY_BUTTON_CLICKED, category=category)
                        pygame.event.post(custom_event)

            elif event.type == CATEGORY_BUTTON_CLICKED:
                print(f"Category button clicked for category: {event.category}")

        update_screen(screen, menus, active_category)  # Pass the active category

    pygame.quit()

if __name__ == "__main__":
    main()
