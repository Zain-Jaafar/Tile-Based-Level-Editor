import pygame
import json
from tile import Tile
from utils import SCREEN, draw_text
from image_manager import image_manager

class Grid:
    def __init__(self):
        self.tile_size = 48
        self.row_count = 32
        self.column_count = 32
        self.grid_starting_position = [0, 0]
        
        self.grid_tile_lists = []
        self.tile_metadata_list = []
        self.create_grid()
        
        self.current_layer = 0
        
        self.keys = []
        self.MOVEMENT_SPEED = 16
        
        self.mouse_presses = []
    
    
    def next_layer(self):
        self.current_layer += 1
    
    def previous_layer(self):
        self.current_layer -= 1
    
    def new_layer(self):
        self.create_grid()
        self.current_layer = len(self.grid_tile_lists) - 1
    
    def display_current_layer(self):
        draw_text("white", f"Layer: {self.current_layer}", (10, SCREEN.get_height() - 25), 28)
        
    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()
    
    def get_mouse_presses(self):
        self.mouse_presses = pygame.mouse.get_pressed()
    
    def create_grid(self):
        self.grid_tile_lists.append([])
        self.tile_metadata_list.append([])
        row_count = 0
        for _ in range(self.row_count):
            column_count = 0
            for _ in range(self.column_count):
                image_path = None
                rect = pygame.Rect((self.grid_starting_position[0] + self.tile_size * column_count, self.grid_starting_position[1] + self.tile_size * row_count), (self.tile_size, self.tile_size))
                position = [self.tile_size * column_count, self.tile_size * row_count]
                tile = Tile(image_path, rect, position)
                self.grid_tile_lists[len(self.grid_tile_lists) - 1].append(tile)

                column_count += 1
            row_count += 1
    
    def reset_grid(self):
        self.grid_tile_lists = []
        self.create_grid()
    
    def draw_tiles(self):
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.draw()

    def on_clicked(self):
        self.get_mouse_presses()
        mouse_position = pygame.mouse.get_pos()
        
        if self.mouse_presses[0]:
            for tile in self.grid_tile_lists[self.current_layer]:
                if image_manager.selectors_hidden:
                    if tile.rect.collidepoint(mouse_position):
                        print(tile.get_position())
                        image_path = image_manager.get_selected_image_path()
                        if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                            if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                                self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                            self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
                    
                        tile.set_image(image_path)
                    
                
                else:
                    if tile.rect.collidepoint(mouse_position) and not tile.rect.colliderect(image_manager.panel_rect):
                        image_path = image_manager.get_selected_image_path()
                        print(tile.get_position())
                        if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                            if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                                self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                            self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
                    
                        tile.set_image(image_path)
            
        elif self.mouse_presses[2]:
            for tile in self.grid_tile_lists[self.current_layer]:
                if tile.rect.collidepoint(mouse_position):
                    try:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    except ValueError:
                        pass
                    
                    image_path = None
                    tile.set_image(image_path)
    
    def move_left(self):
        self.grid_starting_position[0] += self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.x += self.MOVEMENT_SPEED
                
    
    def move_right(self):
        self.grid_starting_position[0] -= self.MOVEMENT_SPEED # CHANGE EVERYTHING LIKE THIS
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.x -= self.MOVEMENT_SPEED
                
    
    def move_up(self):
        self.grid_starting_position[1] += self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.y += self.MOVEMENT_SPEED
                
    
    def move_down(self):
        self.grid_starting_position[1] -= self.MOVEMENT_SPEED
        for grid in self.grid_tile_lists:
            for tile in grid:
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
        layer_count = 0
        with open(file, "r") as f:
            f = json.load(f)
            while len(self.grid_tile_lists) != len(f):
                self.create_grid()
            for layer in f:
                for tile in layer:
                    for grid_tile in self.grid_tile_lists[layer_count]:
                        if tile[1] == grid_tile.get_position():
                            grid_tile.set_image(tile[0])
                self.tile_metadata_list.append(layer)
                layer_count += 1
                

grid = Grid()
