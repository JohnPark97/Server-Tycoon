import pygame
import os
import random

MAX_NUM_ORDER = 7

class Customer:
    def __init__(self, screen, budget, patience, menus):
        self.screen = screen
        self.image = pygame.image.load(os.path.join('assets', 'customers', 'customer_sample.png'))  # Load the customer image
        self.image = pygame.transform.scale(self.image, (400, 400))  # Scale the image to 100x100 pixels
        self.order_list = self.generate_order(menus)  # Generate a list of orders
        self.budget = budget
        self.patience = patience
        self.happiness = 100  # Starts at 100 and can go down or up based on service
        
        # dialogue
        self.current_dialogue_index = 0
        self.dialogue = ["Hello!", "I would like to order.", "Thank you!"]
        
        self.font = pygame.font.SysFont("Comic Sans MS", 30)  # Font for the text
        self.timer = 0  # Timer to keep track of the time passed since the customer appeared
        
    def generate_order(self, menus):
        all_menus = [menu for sublist in menus.values() for menu in sublist]  # Flatten the dictionary into a list
        num_items = random.randint(1, MAX_NUM_ORDER)  # The number of items the customer wants
        return random.sample(all_menus, num_items)

    def place_order(self, menu_item):
        if self.budget >= menu_item.price:
            self.order_list.append(menu_item)
            self.budget -= menu_item.price
            return True
        else:
            return False
            
    def receive_order(self, menu_item):
        if menu_item in self.order_list:
            self.happiness += 10  # Increase happiness
            self.order_list.remove(menu_item)
        else:
            self.happiness -= 10  # Decrease happiness
            
    def wait(self, time_passed):
        self.patience -= time_passed
        if self.patience < 0:
            self.happiness -= 10  # Decrease happiness if they have to wait too long
        
    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))
        
        # Update the timer
        self.timer += 1  # Increment by 1 for each frame, assuming this function is called once per frame
        
        # Show the text above the customer's head after 2 seconds (assuming 60 FPS)
        if self.timer > 2 * 60:
            
            # Draw order list in a rectangle
            rect_width = 300
            rect_height = 40 * len(self.order_list)  # Assuming each order takes up 30 pixels in height
            rect_x = x
            rect_y = y - rect_height - 10  # Positioned above the customer image

            pygame.draw.rect(self.screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
            
            order_y = rect_y + 5  # Start position for the first order text
            for item in self.order_list:
                order_text_surface = self.font.render(item.name, False, (0, 0, 0))
                self.screen.blit(order_text_surface, (rect_x + 5, order_y))  # 5 is padding inside rectangle
                order_y += 30  # Move down for the next item
