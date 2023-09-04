import pygame
import os
import json

from menu import Menu
from computer import Computer
from clock import GameClock
from customer import Customer

FPS = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MONITOR_WIDTH = 850
MONITOR_HEIGHT = 600

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BACKGROUND = (224, 207, 158)

# Define the custom event type
CATEGORY_BUTTON_CLICKED = pygame.USEREVENT + 1
TIME_UP_EVENT = CATEGORY_BUTTON_CLICKED + 1

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

def draw_background(screen: pygame.Surface):
    screen.fill(BACKGROUND)

def update_screen(screen: pygame.Surface, computer: Computer, customer: Customer, game_clock: GameClock):
    draw_background(screen)
    game_clock.draw()
    computer.draw_monitor()
    computer.draw_calc_screen()
    computer.draw_tabs()
    computer.draw_menu()
    # Draw the customer at position (50, 50)
    customer.draw(screen, 30, 300)

    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Server Tycoon")

    run = True

    time_up_event_posted = False  # Add this flag

    clock = pygame.time.Clock()
    game_clock = GameClock(screen, 60)
    menus = load_menu()

    computer = Computer(screen, menus)
    # Create a new customer with a budget of 100 and patience of 60 seconds
    customer = Customer(100, 60)
    
    while run:
        clock.tick(FPS)

        if game_clock.has_time_left():
            # Update the game clock
            game_clock.update()
            time_up_event_posted = False  # Reset the flag when there's time left
        else:
            if not time_up_event_posted:  # Check the flag
                pygame.event.post(pygame.event.Event(TIME_UP_EVENT))
                time_up_event_posted = True  # Set the flag to True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Try menu buttons first
                if not computer.handle_menu_btn_click(x, y):
                    # If no menu button was clicked, try category buttons
                    computer.handle_category_btn_click(x, y, CATEGORY_BUTTON_CLICKED)
            elif event.type == CATEGORY_BUTTON_CLICKED:
                pass
            elif event.type == TIME_UP_EVENT:
                print("Time's up!")

        update_screen(screen, computer, customer, game_clock)
    pygame.quit()

if __name__ == "__main__":
    main()