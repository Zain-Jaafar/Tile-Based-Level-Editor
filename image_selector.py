import pygame
import os
from utils import SCREEN

class ImageSelector():
    # Initialises the image selector
    def __init__(self, rect: pygame.Rect, image_path: str):
        self.image_path = image_path
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path)), (48, 48))
        self.rect = rect
    
    # Returns the file path that the image selector links to
    def get_image_path(self):
        return self.image_path
    
    # Displays the image selector on the screen
    def draw(self):
        SCREEN.blit(self.image, self.rect)