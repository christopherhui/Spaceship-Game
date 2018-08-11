import pygame, sys

pygame.init()
clock = pygame.time.Clock()

# Colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)

# Background parameters:
WIDTH = 1000
HEIGHT = 600
FPS = 60
pygame.display.set_caption('Spaceship Game')

background = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
background.fill(WHITE)

# Spaceship parameters:
width = 40
height = 40

# Init. Boxes
class Boxes(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

def main():
    # draws initial pos. of spaceship
    top_corner = [WIDTH / 2, HEIGHT - height - 10]
    left_corner = [WIDTH / 2 - width / 2, HEIGHT - 10]
    right_corner = [WIDTH / 2 + width / 2, HEIGHT - 10]
    pygame.draw.polygon(background, BLACK, [top_corner, left_corner, right_corner])

    # initializes sprite list
    sprite_list = pygame.sprite.Group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        sprite_list.draw(background)
        pygame.display.update()

main()