import pygame
import os

class Customer:
    def __init__(self, budget, patience):
        self.image = pygame.image.load(os.path.join('assets', 'customers', 'customer_sample.png'))  # Load the customer image
        self.image = pygame.transform.scale(self.image, (400, 400))  # Scale the image to 100x100 pixels
        self.order_list = []
        self.budget = budget
        self.patience = patience
        self.happiness = 100  # Starts at 100 and can go down or up based on service
        
        # dialogue
        self.current_dialogue_index = 0
        self.dialogue = ["Hello!", "I would like to order.", "Thank you!"]
        
        self.font = pygame.font.SysFont("Comic Sans MS", 30)  # Font for the text
        self.timer = 0  # Timer to keep track of the time passed since the customer appeared
        
    def place_order(self, menu_item):
        if self.budget >= menu_item.price:
            self.order_list.append(menu_item)
            self.budget -= menu_item.price
            return True
        else:
            print("Not enough budget to place this order.")
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
            

        
    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
        
        # Update the timer
        self.timer += 1  # Increment by 1 for each frame, assuming this function is called once per frame
        
        # Show the text above the customer's head after 2 seconds (assuming 60 FPS)
        if self.timer > 2 * 60:
            text_surface = self.font.render("I'm waiting!", False, (0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), (x, y - 40, text_surface.get_width(), text_surface.get_height()))
            screen.blit(text_surface, (x, y - 40))
