import pygame
from utils import SCREEN

class Tile():
    def __init__(self, image_path: str, rect: pygame.Rect, position: list[int, int], layer_number: int):
        # Initialises variables for each tile
        
        self.image = None
        self.image_path = image_path
        self.set_image(image_path)
        self.rect = rect
        self.position = position
        self.layer_number = layer_number
        
        # Secondary rect used for the autotiling function
        self.autotiling_rect = pygame.Rect(rect.x - 5, rect.y - 5, rect.width + 10, rect.height + 10)
    
    # Sets the image for tile, this is called when the tile is clicked
    def set_image(self, image_path):
        if image_path is None:
            self.image_path = None
            self.image = None 
        else:
            self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (48, 48))
            self.image_path = image_path
    
    # Get filepath of the tile
    def get_image_path(self):
        return self.image_path

    # Get position of the tile
    def get_position(self):
        return self.position
    
    # Draws the image of the tile, if it has no image then a grey outline will be used instead
    def draw(self):
        if self.image is None:
            if self.layer_number == 1:
                pygame.draw.rect(SCREEN, (40, 40, 40), self.rect, 1)
        else:
            SCREEN.blit(self.image, self.rect)
        
        