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

        self.current_tool = "brush"

        self.select_box_starting_position = (0, 0)
        self.select_box_ending_position = (0, 0)
        self.select_box = pygame.Rect(0, 0, 0, 0)
        self.selected_tiles = []

        self.selected_image_tiles = []
    
    def next_layer(self):
        self.current_layer += 1
    
    def previous_layer(self):
        self.current_layer -= 1
    
    def new_layer(self):
        self.create_grid()
        self.current_layer = len(self.grid_tile_lists) - 1
    
    def display_current_tool(self):
        draw_text("white", f"Tool:  {self.current_tool}", (175, SCREEN.get_height() - 25), 28)

    def display_current_layer(self):
        draw_text("white", f"Layer:  {self.current_layer}", (10, SCREEN.get_height() - 25), 28)
        
    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()
    
    def get_mouse_presses(self):
        self.mouse_presses = pygame.mouse.get_pressed()
    
    def create_grid(self):
        self.grid_tile_lists.append([])
        self.tile_metadata_list.append([])

        layer_number = len(self.grid_tile_lists)

        row_count = 0
        for _ in range(self.row_count):
            column_count = 0
            for _ in range(self.column_count):
                image_path = None
                rect = pygame.Rect((self.grid_starting_position[0] + self.tile_size * column_count, self.grid_starting_position[1] + self.tile_size * row_count), (self.tile_size, self.tile_size))
                position = [self.tile_size * column_count, self.tile_size * row_count]
                tile = Tile(image_path, rect, position, layer_number)
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

    def create_select_box(self):
        self.select_box = pygame.Rect(0, 0, 0, 0)
        x1, y1 = min(self.select_box_starting_position[0], self.select_box_ending_position[0]), min(self.select_box_starting_position[1], self.select_box_ending_position[1])
        x2, y2 = max(self.select_box_starting_position[0], self.select_box_ending_position[0]), max(self.select_box_starting_position[1], self.select_box_ending_position[1])
        
        self.select_box = pygame.Rect(x1, y1, x2-x1, y2-y1)
        self.set_selected_tiles()
        

    def draw_select_box(self):
        pygame.draw.rect(SCREEN, "white", self.select_box, 2)

    def set_selected_tiles(self):
        self.selected_tiles.clear()
        self.selected_image_tiles.clear()
        for tile in self.grid_tile_lists[self.current_layer]:
            if self.select_box.colliderect(tile.rect):
                self.selected_tiles.append(tile)
                if tile.image is not None:
                    self.selected_image_tiles.append(tile)

    def fill_selected_tiles(self):
        for tile in self.selected_tiles:
            tile.set_image(image_manager.selected_image_path)
    
    def delete_selected_tiles(self):
        for tile in self.selected_tiles:
            tile.set_image(None)

    def autotile_selected_tiles(self):
        if self.selected_image_tiles == []:
            return
        
        for tile in self.selected_image_tiles:
            surrounding_tiles = []
            for grid_tile in self.selected_tiles:
                if tile.autotiling_rect.colliderect(grid_tile):
                    if grid_tile != tile:
                        surrounding_tiles.append(grid_tile)
            
            if surrounding_tiles[1].image is None and surrounding_tiles[3].image is not None and surrounding_tiles[4].image is not None:
                tile.set_image(f"Images/Tiles/{image_manager.selected_image_folder}/top_middle.png")

            elif surrounding_tiles[1].image is None and surrounding_tiles[3].image is None and surrounding_tiles[4].image is not None:
                tile.set_image(f"Images/Tiles/{image_manager.selected_image_folder}/top_left.png")
            
            elif surrounding_tiles[1].image is None and surrounding_tiles[3].image is not None and surrounding_tiles[4].image is None:
                tile.set_image(f"Images/Tiles/{image_manager.selected_image_folder}/top_right.png")
            
            elif surrounding_tiles[3].image is None and surrounding_tiles[4].image is not None:
                tile.set_image(f"Images/Tiles/{image_manager.selected_image_folder}/middle_left.png")
            
            elif surrounding_tiles[3].image is not None and surrounding_tiles[4].image is None:
                tile.set_image(f"Images/Tiles/{image_manager.selected_image_folder}/middle_right.png")
            
            else:
                tile.set_image(f"Images/Tiles/{image_manager.selected_image_folder}/filler.png")
            

    def on_clicked(self):
        self.get_mouse_presses()
        mouse_position = pygame.mouse.get_pos()
        
        if self.current_tool == "brush":
            if self.mouse_presses[0]:
                for tile in self.grid_tile_lists[self.current_layer]:
                    if image_manager.selectors_hidden:
                        if tile.rect.collidepoint(mouse_position):
                            image_path = image_manager.get_selected_image_path()
                            if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                                if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                                    self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                                self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
                        
                            tile.set_image(image_path)
                        
                    
                    else:
                        if tile.rect.collidepoint(mouse_position) and not tile.rect.colliderect(image_manager.panel_rect):
                            image_path = image_manager.get_selected_image_path()
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
        
        elif self.current_tool == "select":
            self.draw_select_box()
            
    
    def move_left(self):
        self.grid_starting_position[0] += self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.x += self.MOVEMENT_SPEED
                tile.autotiling_rect.x += self.MOVEMENT_SPEED
                
    
    def move_right(self):
        self.grid_starting_position[0] -= self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.x -= self.MOVEMENT_SPEED
                tile.autotiling_rect.x -= self.MOVEMENT_SPEED
                
    
    def move_up(self):
        self.grid_starting_position[1] += self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.y += self.MOVEMENT_SPEED
                tile.autotiling_rect.y += self.MOVEMENT_SPEED
                
    
    def move_down(self):
        self.grid_starting_position[1] -= self.MOVEMENT_SPEED
        for grid in self.grid_tile_lists:
            for tile in grid:
                tile.rect.y -= self.MOVEMENT_SPEED
                tile.autotiling_rect.y -= self.MOVEMENT_SPEED
                
    
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
