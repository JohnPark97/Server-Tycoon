import pygame

class Menu():
    def __init__(self, name: str, price: int, image: pygame.Surface):
        self.name = name
        self.price = price
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)