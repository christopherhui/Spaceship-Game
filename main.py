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

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.image.set_colorkey(WHITE)

        pygame.draw.rect()


def main():
    x_start = (WIDTH * 0.5) - spaceship_width / 2
    y_start = HEIGHT * 3/4

    x = x_start
    y = y_start

    x_change = 0
    y_change = 0

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_change = spaceship_speed
                elif event.key == pygame.K_LEFT:
                    x_change = -spaceship_speed
                elif event.key == pygame.K_UP:
                    y_change = -spaceship_speed
                elif event.key == pygame.K_DOWN:
                    y_change = spaceship_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change

        background.fill(WHITE)
        changeImg(x, y)

        pygame.display.update()
        clock.tick(FPS)


def changeImg(x, y):
    background.blit(spaceShip, (x, y))

main()


