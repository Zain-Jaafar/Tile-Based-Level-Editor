import pygame
from utils import clock, FPS, SCREEN
from grid import grid
from events import handle_events
from image_manager import image_manager

while True:
    SCREEN.fill((0, 0, 0))
    handle_events(pygame.event.get())
    
    # Draws grid and handles key and mouse presses
    grid.draw_tiles()
    grid.manage_key_presses()
    grid.on_clicked()
    
    if image_manager.selectors_hidden is False:
        image_manager.draw_selectors()
    
    # Displays current layer and tool on the screen
    grid.display_current_layer()
    grid.display_current_tool()
    
    pygame.display.update() # Draws the current frame to the screen after all processing has been done
    clock.tick(FPS) # Controlls the FPS of the program to reduce screen stuttering.