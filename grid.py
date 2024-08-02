import pygame
import json
from tile import Tile
from utils import SCREEN, draw_text
from image_manager import image_manager

class Grid:
    def __init__(self):
        # Grid size variables
        self.tile_size = 48
        self.row_count = 100
        self.column_count = 100
        self.grid_starting_position = [0, 0]
        
        # Grid metadata
        self.grid_tile_lists = []
        self.tile_metadata_list = []
        
        # Generate the grid
        self.create_grid()
        
        self.current_layer = 0
        
        self.keys = [] # Stores all current keypresses
        self.MOVEMENT_SPEED = 16 # Movement speed of camera
        
        self.mouse_presses = [] # Stores all current mouse presses

        self.current_tool = "brush" # Keeps track of current tool selected

        # Variables for selecting multiple tiles
        self.select_box_starting_position = (0, 0)
        self.select_box_ending_position = (0, 0)
        self.select_box = pygame.Rect(0, 0, 0, 0)
        self.selected_tiles = []

        self.selected_image_tiles = []
    
    # Increments current layer by 1
    def next_layer(self):
        self.current_layer += 1
    
    # Decrements current layer by 1
    def previous_layer(self):
        self.current_layer -= 1
    
    # Creates a new layer
    def new_layer(self):
        self.create_grid()
        self.current_layer = len(self.grid_tile_lists) - 1
    
    # Displays current tool on the screen
    def display_current_tool(self):
        draw_text("white", f"Tool:  {self.current_tool}", (175, SCREEN.get_height() - 25), 28)

    # Displays current layer on the screen 
    def display_current_layer(self):
        draw_text("white", f"Layer:  {self.current_layer}", (10, SCREEN.get_height() - 25), 28)
    
    # Get all keypresses for current frame
    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()
    
    # Get all mouse presses for current frame
    def get_mouse_presses(self):
        self.mouse_presses = pygame.mouse.get_pressed()
    
    # Generate the grid 
    def create_grid(self):
        self.grid_tile_lists.append([])
        self.tile_metadata_list.append([])

        layer_number = len(self.grid_tile_lists)

        row_count = 0
        for _ in range(self.row_count): # Make Rows which are made up of columns
            column_count = 0
            for _ in range(self.column_count): # Make Columns
                image_path = None
                rect = pygame.Rect((self.grid_starting_position[0] + self.tile_size * column_count, self.grid_starting_position[1] + self.tile_size * row_count), (self.tile_size, self.tile_size))
                position = [self.tile_size * column_count, self.tile_size * row_count]
                tile = Tile(image_path, rect, position, layer_number)
                self.grid_tile_lists[len(self.grid_tile_lists) - 1].append(tile)

                column_count += 1
            row_count += 1
    
    # Deletes all grids and makes a new one
    def reset_grid(self):
        self.grid_tile_lists = []
        self.create_grid()
    
    # Draws the user-placed tiles
    def draw_tiles(self):
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.draw()

    # Creates the select box to select multiple tiles
    def create_select_box(self):
        self.select_box = pygame.Rect(0, 0, 0, 0)
        x1, y1 = min(self.select_box_starting_position[0], self.select_box_ending_position[0]), min(self.select_box_starting_position[1], self.select_box_ending_position[1])
        x2, y2 = max(self.select_box_starting_position[0], self.select_box_ending_position[0]), max(self.select_box_starting_position[1], self.select_box_ending_position[1])
        
        self.select_box = pygame.Rect(x1, y1, x2-x1, y2-y1)
        self.set_selected_tiles()
        

    # Draws a rectangle representing the area which is selected
    def draw_select_box(self):
        pygame.draw.rect(SCREEN, "white", self.select_box, 2)

    # Appends the selected tiles to self.selected_image_tiles
    def set_selected_tiles(self):
        self.selected_tiles.clear()
        self.selected_image_tiles.clear()
        for tile in self.grid_tile_lists[self.current_layer]:
            if self.select_box.colliderect(tile.rect):
                self.selected_tiles.append(tile)
                if tile.image is not None:
                    self.selected_image_tiles.append(tile)

    # Fills the selected tiles with the most recently selected tile image
    def fill_selected_tiles(self):
        for tile in self.selected_tiles:
            image_path = image_manager.selected_image_path
            if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                    self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
        
            tile.set_image(image_path)
    
    # Deletes all Tiles within the selected region
    def delete_selected_tiles(self):
        for tile in self.selected_tiles:
            try:
                self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
            except ValueError:
                pass
            
            image_path = None
            tile.set_image(image_path)

    # This function automatically tiles selects the images for the tiles in a 
    # selection depending on which tiles are surrounding it
    def autotile_selected_tiles(self):
        # Exit the function if there are no tiles selected
        if self.selected_image_tiles == []:
            return
        
        # Figure out if there are tiles surrounding each tile
        for tile in self.selected_image_tiles:
            surrounding_tiles = []
            for grid_tile in self.selected_tiles:
                if tile.autotiling_rect.colliderect(grid_tile):
                    if grid_tile != tile:
                        surrounding_tiles.append(grid_tile)
            
            # If there is a tile to the left and right, but not on top, use the "top middle" tile image
            if surrounding_tiles[1].image is None and surrounding_tiles[3].image is not None and surrounding_tiles[4].image is not None:
                image_path = f"Images/Tiles/{image_manager.selected_image_folder}/top_middle.png"
                if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                    if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
            
                tile.set_image(image_path)

            # If there is a tile to the right, but not on top or to the left, use the "top left" tile image
            elif surrounding_tiles[1].image is None and surrounding_tiles[3].image is None and surrounding_tiles[4].image is not None:
                image_path = f"Images/Tiles/{image_manager.selected_image_folder}/top_left.png"
                if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                    if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
            
                tile.set_image(image_path)
            
            # If there is a tile to the left, but not on top or to the right, use the "top right" tile image
            elif surrounding_tiles[1].image is None and surrounding_tiles[3].image is not None and surrounding_tiles[4].image is None:
                image_path = f"Images/Tiles/{image_manager.selected_image_folder}/top_right.png"
                if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                    if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
            
                tile.set_image(image_path)
            
            # If there is a tile on top, bottom, and to the right, but not to the left, use the "middle left" tile image
            elif surrounding_tiles[3].image is None and surrounding_tiles[4].image is not None:
                image_path = f"Images/Tiles/{image_manager.selected_image_folder}/middle_left.png"
                if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                    if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
            
                tile.set_image(image_path)
            
            # If there is a tile on top, bottom, and to the right, but not to the left, use the "middle right" tile image
            elif surrounding_tiles[3].image is not None and surrounding_tiles[4].image is None:
                image_path = f"Images/Tiles/{image_manager.selected_image_folder}/middle_right.png"
                if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                    if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
            
                tile.set_image(image_path)
            
            # If there are tiles all around, use the "filler" tile image
            else:
                image_path = f"Images/Tiles/{image_manager.selected_image_folder}/filler.png"
                if [image_path, tile.get_position()] not in self.tile_metadata_list[self.current_layer]:
                    if [tile.get_image_path(), tile.get_position()] in self.tile_metadata_list[self.current_layer]:
                        self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                    self.tile_metadata_list[self.current_layer].append([image_path, tile.get_position()])
            
                tile.set_image(image_path)

    # Handles mouse presses
    def on_clicked(self):
        self.get_mouse_presses()
        mouse_position = pygame.mouse.get_pos()
        
        if self.current_tool == "brush":
            '''
            This code can be read like this:
            If the left mouse button is pressed:
                if side panel is hidden:
                    if the mouse pointer is on a tile:
                        set the tile's image to the current selected image
                else (the side panel is being shown):
                    if the mouse pointer is on the side panel then ignore the button press
            '''
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
            
            # This code can be read like this:
            # If the right mouse button is pressed:
            #     if the mouse pointer is on a tile:
            #         try to remove/delete/erase the tile
            #         if the tile has no data, don't do anything
            elif self.mouse_presses[2]:
                for tile in self.grid_tile_lists[self.current_layer]:
                    if tile.rect.collidepoint(mouse_position):
                        try:
                            self.tile_metadata_list[self.current_layer].remove([tile.get_image_path(), tile.get_position()])
                        except ValueError:
                            pass
                        
                        image_path = None
                        tile.set_image(image_path)
        
        # Draws the select box when left mouse button is clicked and dragged
        elif self.current_tool == "select":
            self.draw_select_box()
            
    # Moves all tiles and grids to the right, making it look like the camera is moving left
    def move_left(self):
        self.grid_starting_position[0] += self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.x += self.MOVEMENT_SPEED
                tile.autotiling_rect.x += self.MOVEMENT_SPEED
                
    # Moves all tiles and grids to the left, making it look like the camera is moving right
    def move_right(self):
        self.grid_starting_position[0] -= self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.x -= self.MOVEMENT_SPEED
                tile.autotiling_rect.x -= self.MOVEMENT_SPEED
                
    # Moves all tiles and grids down, making it look like the camera is moving up
    def move_up(self):
        self.grid_starting_position[1] += self.MOVEMENT_SPEED
        for layer in self.grid_tile_lists:
            for tile in layer:
                tile.rect.y += self.MOVEMENT_SPEED
                tile.autotiling_rect.y += self.MOVEMENT_SPEED
                
    # Moves all tiles and grids to the up, making it look like the camera is moving down
    def move_down(self):
        self.grid_starting_position[1] -= self.MOVEMENT_SPEED
        for grid in self.grid_tile_lists:
            for tile in grid:
                tile.rect.y -= self.MOVEMENT_SPEED
                tile.autotiling_rect.y -= self.MOVEMENT_SPEED
                
    # Decides how to move the camera based on what key is pressed
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
    
    # Exports the level to a json file where it can then be parsed for any tile-based game
    def save(self):
        with open("Levels/level.json", "w") as f:
            json.dump(self.tile_metadata_list, f)
    
    # Loads a previously saved level so it can be further edited
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
