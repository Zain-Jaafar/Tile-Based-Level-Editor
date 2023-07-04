import pygame
from utils import SCREEN

class Tile():
    def __init__(self, image_path: str, rect: pygame.Rect):
        self.image = None
        self.image_path = image_path
        self.set_image(image_path)
        self.rect = rect
        self.position = [rect.x, rect.y]
    
    def set_image(self, image_path):
        if image_path is None:
            self.image_path = None
            self.image = None 
        else:
            self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (48, 48))
            self.image_path = image_path
    
    def get_image_path(self):
        return self.image_path

    def get_position(self):
        return self.position
    
    def draw(self):
        if self.image is None:
            pygame.draw.rect(SCREEN, (40, 40, 40), self.rect, 1)
        else:
            SCREEN.blit(self.image, self.rect)
        
        