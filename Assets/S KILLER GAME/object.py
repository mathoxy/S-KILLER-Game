from os import listdir
from os.path import join, isfile
import pygame

def load_block(size):
    path = join("Terrain", "Terrain.png")
    try:
        image = pygame.image.load(path)
    except pygame.error as e:
            print("Error loading image:", e)
    rect = pygame.Rect(96, 0, size, size)
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface) 


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = load_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


