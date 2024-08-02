import pygame
import os
from utils import SCREEN, SCREEN_HEIGHT, draw_text
from image_selector import ImageSelector

class ImageManager():
    def __init__(self):
        # Initialise variables for the image manager, which allows you to select images when using the app
        
        # Get all image groups and images from the Images folder
        self.images = {}
        for path in os.listdir("Images/Tiles"):
            if "." not in path:
                self.images[f"{path}"] = []
                for file_name in os.listdir(f"Images/Tiles/{path}"):
                    self.images[f"{path}"].append(f"Images/Tiles/{path}/{file_name}")

        # Variables for the side panel
        self.panel_background = pygame.Surface((300, SCREEN_HEIGHT))
        self.panel_background.fill((20,20,30))
        self.panel_rect = pygame.Rect((0, 0), (300, SCREEN_HEIGHT))
        
        # Image Selectors, which allow you to pick which image to use
        self.selectors = []
        self.selector_titles = []
        
        self.create_selectors()
        
        # Keep track of the current image being used
        self.selected_image_path = None
        self.selected_image_folder = None
        
        # Allows us to toggle if the panel is shown or hidden
        self.selectors_hidden = False
    
    # Creates the image selectors
    def create_selectors(self):
        row_count = -1
        for dictionary in self.images:
            column_count = 0
            row_count += 1
            self.selector_titles.append([dictionary, pygame.Rect((10, row_count * 58 + 10), (300, 32))])
            for image_path in self.images[dictionary]:
                if column_count > 4:
                    column_count = 0
                    row_count += 1
                
                rect = pygame.Rect((column_count * 58 + 10, row_count * 58 + 35),(48, 48))
                
                selector = ImageSelector(rect, image_path)
                self.selectors.append(selector)
                column_count += 1
            row_count += 1
    
    # Display the panel and image selectors on the screen
    def draw_selectors(self):
        self.panel_background = pygame.Surface((300, SCREEN.get_height()))
        self.panel_background.fill((20,20,30))
        self.panel_rect = pygame.Rect((0, 0), (300, SCREEN.get_height()))
        SCREEN.blit(self.panel_background, (0,0))
        
        # Draw all selectors
        for selector in self.selectors:
            selector.draw()
        
        # Draw text to group the selectors into categories like "Grass Tiles" or "Desert Tiles"
        for selector_title in self.selector_titles:
            draw_text("white", selector_title[0], selector_title[1].topleft, 32)
    
    def get_selected_image_path(self):
        return self.selected_image_path
    
    # if the selector is clicked with the left mouse button, set the selected image to that of the selector
    def onclicked(self, mouse_button, mouse_position):
        if mouse_button == 1:
            for selector in self.selectors:
                if selector.rect.collidepoint(mouse_position) and self.selectors_hidden is False:
                    self.selected_image_path = selector.get_image_path()
                    temp_string = selector.get_image_path()[13:]
                    self.selected_image_folder = temp_string[:temp_string.index("/")]


image_manager = ImageManager()
