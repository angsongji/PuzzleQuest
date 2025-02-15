import pygame
from .setting import *

pygame.font.init()

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color):
        super().__init__()
        self.image = pygame.Surface((puzzle_size, puzzle_size))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("Arial", 50)
        self.color = color

        if self.text != "0":
            font_surface = self.font.render(self.text, True, rgbBackground_light)
            self.image.fill(self.color)
            self.font_size = self.font.size(self.text)
            draw_x = (puzzle_size / 2) - (self.font_size[0] / 2)
            draw_y = (puzzle_size / 2) - (self.font_size[1] / 2)
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(rgbBackground_light)  # Màu ô trống

    def update(self, offset_x, offset_y):
        self.rect.x = offset_x + self.x * puzzle_size
        self.rect.y = offset_y + self.y * puzzle_size

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    