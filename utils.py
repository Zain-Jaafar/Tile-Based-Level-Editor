import pygame

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Level Editor")

FPS = 60
clock = pygame.time.Clock()


def draw_text(colour, text, position, text_size=32):
    font = pygame.font.Font('Fonts/Pixeltype.ttf', text_size)
    text_surf = font.render(text, False, colour)
    text_rect = pygame.Rect((0, 0), (text_surf.get_size()))
    text_rect.topleft = position
    SCREEN.blit(text_surf, text_rect)
