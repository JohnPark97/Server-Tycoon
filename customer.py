import pygame
import os
import random

from common import wrap_text

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
        self.dialogue_box_active = False  # Whether the dialogue box is active or not
        self.dialogue_map = {
            "order": self._order_to_txt(),
            "positive": "Thank you!",
            "negative": "What is this!?",
        }

        self.current_dialogue = self.dialogue_map["order"]
        
        self.font = pygame.font.SysFont("Comic Sans MS", 30)  # Font for the text
        self.timer = 0  # Timer to keep track of the time passed since the customer appeared

    def _order_to_txt(self):
        return ', '.join([order.name for order in self.order_list])    

    def generate_order(self, menus):
        all_menus = [menu for sublist in menus.values() for menu in sublist]  # Flatten the dictionary into a list
        num_items = random.randint(1, MAX_NUM_ORDER)  # Th
        return random.sample(all_menus, num_items)

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
        
    def react_to_order(self, got_order_right: bool):
        if got_order_right:
            self.current_dialogue = self.dialogue_map["positive"]
        else:
            self.current_dialogue = self.dialogue_map["negative"]

    def draw_dialogue_box(self):
        # Draw the dialogue box
        pygame.draw.rect(self.screen, (255, 255, 255), (25, 25, 375, 250))
        
        # Draw the dialogue text
        dialogue_text = self.current_dialogue
        max_width = 350  # Max width inside the rectangle
        
        lines = wrap_text(dialogue_text, self.font, max_width)
        y_offset = 30  # Starting y position
        for line in lines:
            dialogue_surface = self.font.render(line.strip(), False, (0, 0, 0))
            self.screen.blit(dialogue_surface, (30, y_offset))
            y_offset += self.font.get_height()  # Move down for the next line


    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))
        self.draw_dialogue_box()
        
        # Update the timer
        # self.timer += 1  # Increment by 1 for each frame, assuming this function is called once per frame
        
        # if self.timer > 2 * 60:
