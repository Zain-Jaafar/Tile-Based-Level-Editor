import pygame
from tile import Tile
from utils import SCREEN
from image_manager import image_manager
import json

class Grid:
    def __init__(self):
        self.tile_size = 48
        self.row_count = 32
        self.column_count = 32
        
        self.grid_tile_list = []
        self.tile_metadata_list = []
        self.create_grid()
        
        self.keys = []
        self.MOVEMENT_SPEED = 16
        
        self.mouse_presses = []
    
    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()
    
    def get_mouse_presses(self):
        self.mouse_presses = pygame.mouse.get_pressed()
    
    def create_grid(self):
        row_count = 0
        for _ in range(self.row_count):
            column_count = 0
            for _ in range(self.column_count):
                image_path = None
                rect = pygame.Rect((self.tile_size * column_count, self.tile_size * row_count), (self.tile_size, self.tile_size))
                tile = Tile(image_path, rect)
                self.grid_tile_list.append(tile)
                
                column_count += 1
            row_count += 1
    
    def reset_grid(self):
        for tile in self.grid_tile_list:
            tile.set_image(None)
    
    def draw_tiles(self):
        for tile in self.grid_tile_list:
            tile.draw()

    def on_clicked(self):
        self.get_mouse_presses()
        mouse_position = pygame.mouse.get_pos()
        
        if self.mouse_presses[0]:
            for tile in self.grid_tile_list:
                if image_manager.selectors_hidden:
                    if tile.rect.collidepoint(mouse_position):
                        image_path = image_manager.get_selected_image_path()
                        if [image_path, tile.get_position()] not in self.tile_metadata_list:
                            if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list:
                                self.tile_metadata_list.remove([tile.get_image_path(), tile.get_position()])
                            self.tile_metadata_list.append([image_path, tile.get_position()])
                    
                        tile.set_image(image_path)
                    
                
                else:
                    if tile.rect.collidepoint(mouse_position) and not tile.rect.colliderect(image_manager.panel_rect):
                        image_path = image_manager.get_selected_image_path()
                        if [image_path, tile.get_position()] not in self.tile_metadata_list:
                            if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list:
                                self.tile_metadata_list.remove([tile.get_image_path(), tile.get_position()])
                            self.tile_metadata_list.append([image_path, tile.get_position()])
                    
                        tile.set_image(image_path)
            
        elif self.mouse_presses[2]:
            for tile in self.grid_tile_list:
                if tile.rect.collidepoint(mouse_position):
                    try:
                        self.tile_metadata_list.remove([tile.get_image_path(), tile.get_position()])
                    except ValueError:
                        pass
                    
                    image_path = None
                    tile.set_image(image_path)
    
    def move_left(self):
        for tile in self.grid_tile_list:
            tile.rect.x += self.MOVEMENT_SPEED
    
    def move_right(self):
        for tile in self.grid_tile_list:
            tile.rect.x -= self.MOVEMENT_SPEED
    
    def move_up(self):
        for tile in self.grid_tile_list:
            tile.rect.y += self.MOVEMENT_SPEED
    
    def move_down(self):
        for tile in self.grid_tile_list:
            tile.rect.y -= self.MOVEMENT_SPEED
    
    def manage_key_presses(self):
        self.get_key_presses()
        if self.keys[pygame.K_UP]:
            self.move_up()
        if self.keys[pygame.K_DOWN]:
            self.move_down()
        if self.keys[pygame.K_LEFT]:
            self.move_left()
        if self.keys[pygame.K_RIGHT]:
            self.move_right()
        
    def save(self):
        with open("Levels/level.json", "w") as f:
            json.dump(self.tile_metadata_list, f)
    
    def load(self, file):
        self.reset_grid()
        self.tile_metadata_list.clear()
        with open(file, "r") as f:
            f = json.load(f)
            for tile_metadata in f:
                for grid_tile in self.grid_tile_list:
                    if tile_metadata[1] == grid_tile.get_position():
                        grid_tile.set_image(tile_metadata[0])
                self.tile_metadata_list.append(tile_metadata)
                

grid = Grid()
