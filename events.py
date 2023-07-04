import pygame
import sys
from grid import grid
from image_manager import image_manager


def handle_events(events: pygame.event.Event):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            image_manager.onclicked(event.button, event.pos)
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                grid.save()
            
            if event.key == pygame.K_h:
                if image_manager.selectors_hidden:
                    image_manager.selectors_hidden = False
                else:
                    image_manager.selectors_hidden = True
        
        elif event.type == pygame.DROPFILE:
                grid.load(event.file)