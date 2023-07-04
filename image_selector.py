import pygame
import os
from utils import SCREEN

class ImageSelector():
    def __init__(self, rect: pygame.Rect, image_path: str):
        self.image_path = image_path
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path)), (48, 48))
        self.rect = rect
    
    def get_image_path(self):
        return self.image_path
    
    def draw(self):
        SCREEN.blit(self.image, self.rect)