import pygame, sys, time, random

pygame.init()
clock = pygame.time.Clock()

# Colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
GRAY = (128, 128, 128)

# Map dimensions and properties
WIDTH = 600
HEIGHT = 600
FPS = 60
pygame.display.set_caption('Spaceship Game')

background = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
background_colour = WHITE

# Spaceship dimensions and properties
spaceship_width = 50
spaceship_height = 50
spaceship_speed = 5

loadSpaceShip = pygame.image.load('spaceshiptriangle.png')
spaceShip = pygame.transform.scale(loadSpaceShip, (spaceship_width, spaceship_height))

# hearts dimensions
heart_width = 40
heart_height = 40

# initialize class for blocks:
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, fall_speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.speed = fall_speed

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def init_pos(self):
        self.rect.x = random.randrange(WIDTH - self.width)
        self.rect.y = - HEIGHT * 1/4

    def reset_pos(self):
        self.rect.x = random.randrange(WIDTH - self.width)
        self.rect.y = -self.height

    def respawn_blo(self):
        self.rect.x = random.randrange(WIDTH - self.width)
        self.rect.y = - HEIGHT * 0.5

    def update(self):
        self.rect.y += self.speed

# initialize class for bullets:
class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed

        self.image = pygame.Surface([5, 10])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        self.rect.x = x + spaceship_width / 2 - 2
        self.rect.y = y

    def update(self):
        self.rect.y -= self.speed

# init. for Heart -- used for tracking health
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, life):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.life = life
        self.width = heart_width
        self.height = heart_height

        self.image = pygame.image.load('heart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

def main():
    # get x and y values of spaceship
    x_start = (WIDTH * 0.5) - spaceship_width / 2
    y_start = HEIGHT * 3/4

    x = x_start
    y = y_start
    x_change = 0
    y_change = 0
    lives = 5

    # creation for blocks
    wait_time = 5
    fall_speed = 3
    block_sprites = pygame.sprite.Group()
    gen_blocks(block_sprites, fall_speed)

    # bullet properties:
    bullet_speed = 5
    bullet_sprites = pygame.sprite.Group()

    # creation for hearts
    heart_sprites = pygame.sprite.Group()
    gen_hearts(heart_sprites, lives)

    while True:

        # background creation and text display
        background.fill(background_colour)
        health_msg()

        # event types for controlling spaceship
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_change += spaceship_speed
                elif event.key == pygame.K_LEFT:
                    x_change += -spaceship_speed
                elif event.key == pygame.K_UP:
                    y_change += -spaceship_speed
                elif event.key == pygame.K_DOWN:
                    y_change += spaceship_speed
                elif event.key == pygame.K_SPACE:
                    spawn_bullet(bullet_sprites, x, y, bullet_speed)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    x_change += -spaceship_speed
                elif event.key == pygame.K_LEFT:
                    x_change += spaceship_speed
                elif event.key == pygame.K_UP:
                    y_change += spaceship_speed
                elif event.key == pygame.K_DOWN:
                    y_change += -spaceship_speed

        x += x_change
        y += y_change

        # takes the boundaries of each of the game's WIDTH and HEIGHT
        if x + spaceship_width < 0:
            x = WIDTH + spaceship_width

        if x > WIDTH + spaceship_width:
            x = -spaceship_width

        if y + spaceship_height < 0:
            y = HEIGHT

        if y > HEIGHT:
            y = -spaceship_height

        # changes player spaceship location
        change_img(x, y)

        # bullet properties - 1. out of bounds check 2. collision logic on block
        for bullet in bullet_sprites:
            if bullet.rect.y < 0:
                bullet_sprites.remove(bullet)

            block_hit_list = pygame.sprite.spritecollide(bullet, block_sprites, False)
            for block in block_hit_list:
                bullet_sprites.remove(bullet)
                block.respawn_blo()

        # bullet updates on screen:
        bullet_sprites.draw(background)
        bullet_sprites.update()

        # block updates on screen:
        block_sprites.draw(background)
        block_sprites.update()

        for block in block_sprites:
            if block.rect.y > HEIGHT:
                block.init_pos()
                reduce_life(lives, heart_sprites)
                lives -= 1
            # TODO add a "game over" option when lives == 0

        # heart sprites for lives:
        for heart in heart_sprites:
            pygame.Surface.blit(background, heart.image, (heart.x, heart.y))

        pygame.display.update()
        clock.tick(FPS)

def get_background():
    backgroundImg = pygame.image.load('clouds.jpg')
    rect = backgroundImg.get_rect()
    rect.left, rect.top = (0, 0)
    background.blit(backgroundImg, rect)

def change_img(x, y):
    background.blit(spaceShip, (x, y))

def gen_blocks(block_sprites, fall_speed):
    for i in range(5):
        aBlock = Block(BLUE, 50, 50, fall_speed)
        block_sprites.add(aBlock)
        aBlock.init_pos()

def spawn_bullet(bullet_sprites, x, y, bullet_speed):
    bullet = Bullet(bullet_speed, x, y)
    bullet_sprites.add(bullet)

def gen_hearts(heart_sprites, lives):
    for i in range(lives):
        if i == 0:
            heart = Heart(150, 20, i + 1)
        else:
            heart = Heart(150 + (i * heart_width * 6/5), 20, i + 1)
        heart_sprites.add(heart)

def reduce_life(lives, heart_sprites):
    for heart in heart_sprites:
        if heart.life == lives:
            heart_sprites.remove(heart)

def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def health_msg():
    healthText = pygame.font.Font('freesansbold.ttf', heart_height)
    TextSurface, TextRect = text_objects("Lives:", healthText)
    TextRect.center = (70, 40)
    background.blit(TextSurface, TextRect)

if __name__ == '__main__':
    main()


