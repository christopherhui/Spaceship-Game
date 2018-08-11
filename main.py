import pygame, sys

pygame.init()
clock = pygame.time.Clock()

# Colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)


WIDTH = 1000
HEIGHT = 600
FPS = 60
pygame.display.set_caption('Spaceship Game')

background = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# Init. Spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.Sprite.sprite.__init__(self)

        self.image
