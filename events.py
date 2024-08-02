import pygame
import sys
from grid import grid
from image_manager import image_manager

# Handles all events like keypresses, mouse clicks, and file drops
def handle_events(events: pygame.event.Event):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # If a mouse button is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            image_manager.onclicked(event.button, event.pos)

            

            if grid.current_tool == "select":
                grid.select_box_starting_position = event.pos
        
        # If a mouse button is released
        elif event.type == pygame.MOUSEBUTTONUP:
            if grid.current_tool == "select":
                grid.select_box_ending_position = event.pos
                grid.create_select_box()

        # If a key is pressed 
        elif event.type == pygame.KEYDOWN:
            
            # If CTRL + S is pressed
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                grid.save()
            
            # Hides and shows the side panel
            elif event.key == pygame.K_h:
                if image_manager.selectors_hidden:
                    image_manager.selectors_hidden = False
                else:
                    image_manager.selectors_hidden = True
        
            elif event.key == pygame.K_n:
                grid.new_layer()
            
            elif event.key == pygame.K_o:
                grid.next_layer()
            
            elif event.key == pygame.K_i:
                grid.previous_layer()
            
            elif event.key == pygame.K_f:
                grid.fill_selected_tiles()
            
            elif event.key == pygame.K_d:
                grid.delete_selected_tiles()
            
            elif event.key == pygame.K_a:
                grid.autotile_selected_tiles()
            
            elif event.key == pygame.K_1:
                grid.current_tool = "brush"
            
            elif event.key == pygame.K_2:
                grid.current_tool = "select"
        
        # This event is triggered when a file is dragged and dropped onto the program window.
        elif event.type == pygame.DROPFILE:
                grid.load(event.file)
