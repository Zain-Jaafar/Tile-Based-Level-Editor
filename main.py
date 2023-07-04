import pygame
from utils import clock, FPS, SCREEN
from grid import grid
from events import handle_events
from image_manager import image_manager

while True:
    SCREEN.fill((0, 0, 0))
    handle_events(pygame.event.get())
    
    grid.draw_tiles()
    grid.manage_key_presses()
    grid.on_clicked()
    if image_manager.selectors_hidden is False:
        image_manager.draw_selectors()
    
    pygame.display.update()
    clock.tick(FPS)