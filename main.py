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
background.fill(WHITE)

# Init. Spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        pygame.draw.polygon(self.image, color, [[WIDTH / 2, HEIGHT - height],[WIDTH / 2 - width / 2, HEIGHT],[WIDTH / 2 + width / 2, HEIGHT]])

    def drawShip(self):
        ship_list = pygame.sprite.Group()
        ship_list.add(self)
        ship_list.draw(background)

def main():
    a = Spaceship(BLUE, 100, 100)
    a.drawShip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()

main()