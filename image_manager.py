import pygame
import os
from utils import SCREEN, SCREEN_HEIGHT, draw_text
from image_selector import ImageSelector

class ImageManager():
    def __init__(self):
        self.images = {}
        for path in os.listdir("Images/Tiles"):
            if "." not in path:
                self.images[f"{path}"] = []
                for file_name in os.listdir(f"Images/Tiles/{path}"):
                    self.images[f"{path}"].append(f"Images/Tiles/{path}/{file_name}")

        self.panel_background = pygame.Surface((300, SCREEN_HEIGHT))
        self.panel_background.fill((20,20,30))
        self.panel_rect = pygame.Rect((0, 0), (300, SCREEN_HEIGHT))
        
        self.selectors = []
        self.selector_titles = []
        
        self.create_selectors()
        
        self.selected_image_path = None
        
        self.selectors_hidden = False
    
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
    
    def draw_selectors(self):
        self.panel_background = pygame.Surface((300, SCREEN.get_height()))
        self.panel_background.fill((20,20,30))
        self.panel_rect = pygame.Rect((0, 0), (300, SCREEN.get_height()))
        SCREEN.blit(self.panel_background, (0,0))
        
        for selector in self.selectors:
            selector.draw()
        
        for selector_title in self.selector_titles:
            draw_text("white", selector_title[0], selector_title[1].topleft, 32)
    
    def get_selected_image_path(self):
        return self.selected_image_path

    def set_selected_image_path(self, new_path: str):
        self.selected_image_path = new_path
        
    def onclicked(self, mouse_button, mouse_position):
        if mouse_button == 1:
            for selector in self.selectors:
                if selector.rect.collidepoint(mouse_position) and self.selectors_hidden is False:
                    self.selected_image_path = selector.get_image_path()


image_manager = ImageManager()
