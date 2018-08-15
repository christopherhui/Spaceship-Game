import pygame, sys, time, random

pygame.init()
clock = pygame.time.Clock()

# Colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
LIGHTBLUE = (190, 210, 252)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
GRAY = (128, 128, 128)
PURPLE = (170, 45, 220)

# Map dimensions and properties
WIDTH = 600
HEIGHT = 600
FPS = 70
pygame.display.set_caption('Spaceship Game')

assert WIDTH >= 600, 'Map width must be greater than 600'

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# Spaceship dimensions and properties
spaceship_width = 100
spaceship_height = 100
spaceship_speed = 7

loadSpaceShip = pygame.image.load('spaceship.png')
spaceShip = pygame.transform.scale(loadSpaceShip, (spaceship_width, spaceship_height))

# hearts dimensions
heart_width = 35
heart_height = 35

# text positions
health_msg_width = 70
level_msg_width = WIDTH - 90
score_msg_width = level_msg_width - 63

# class for background image
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

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
        self.image.fill(WHITE)

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

    # start misc stuff
    lives = 5
    level = 1
    score = 0
    score_threshold = 4
    score_threshold_incr = score_threshold
    game_over = False

    # creation for blocks
    wait_time = 5
    fall_speed = 2
    block_sprites = pygame.sprite.Group()
    gen_blocks(block_sprites, fall_speed, level)

    # bullet properties:
    bullet_speed = 7
    bullet_sprites = pygame.sprite.Group()

    # creation for hearts
    heart_sprites = pygame.sprite.Group()
    gen_hearts(heart_sprites, lives)

    # create background
    BackGround = Background('outerspace.jpg', [0,0])

    while True:
        # background creation
        screen.fill(WHITE)
        screen.blit(BackGround.image, BackGround.rect)

        # event types for controlling spaceship
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
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

            if event.type == pygame.KEYUP and not game_over:
                if event.key == pygame.K_RIGHT:
                    x_change += -spaceship_speed
                elif event.key == pygame.K_LEFT:
                    x_change += spaceship_speed
                elif event.key == pygame.K_UP:
                    y_change += spaceship_speed
                elif event.key == pygame.K_DOWN:
                    y_change += -spaceship_speed

            if event.type == pygame.KEYUP and game_over:
                if event.key == pygame.K_r:
                    main()

        if game_over:
            x_change = 0
            y_change = 0

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

        # bullet properties - 1. out of bounds check 2. collision logic on block
        for bullet in bullet_sprites:
            if bullet.rect.y < 0:
                bullet_sprites.remove(bullet)

            block_hit_list = pygame.sprite.spritecollide(bullet, block_sprites, False)
            for block in block_hit_list:
                bullet_sprites.remove(bullet)
                block.respawn_blo()
                score += 1

        # update level and their respective properties
        if score >= score_threshold:
            level += 1
            score_threshold += score_threshold_incr * level
            if fall_speed < 5:
                fall_speed += 0.25
            if level % 3 == 0:
                gen_blocks(block_sprites, fall_speed, level)

        # bullet updates on screen:
        bullet_sprites.draw(screen)
        bullet_sprites.update()

        # block updates on screen:
        block_sprites.draw(screen)
        block_sprites.update()

        # block property changes
        for block in block_sprites:
            if block.rect.y > HEIGHT:
                block.init_pos()
                reduce_life(lives, heart_sprites)
                lives -= 1
            block.speed = fall_speed

        # heart sprites for lives:
        for heart in heart_sprites:
            pygame.Surface.blit(screen, heart.image, (heart.x, heart.y))

        # changes player spaceship location
        change_img(x, y)

        # text display
        health_msg(lives)
        level_msg(level)
        score_msg(score)
        if lives <= 0:
            game_over = True
            game_over_init(block_sprites)

        pygame.display.update()
        clock.tick(FPS)

def change_img(x, y):
    screen.blit(spaceShip, (x, y))

def gen_blocks(block_sprites, fall_speed, level):
    if level == 1:
        for i in range(3):
            aBlock = Block(LIGHTBLUE, 50, 50, fall_speed)
            block_sprites.add(aBlock)
            aBlock.init_pos()
    else:
        aBlock = Block(LIGHTBLUE, 50, 50, fall_speed)
        block_sprites.add(aBlock)
        aBlock.init_pos()

def spawn_bullet(bullet_sprites, x, y, bullet_speed):
    bullet = Bullet(bullet_speed, x, y)
    bullet_sprites.add(bullet)

def gen_hearts(heart_sprites, lives):
    for i in range(lives):
        if i == 0:
            heart = Heart(health_msg_width * 2, 20, i + 1)
        else:
            heart = Heart(health_msg_width * 2 + (i * heart_width * 6/5), 20, i + 1)
        heart_sprites.add(heart)

def reduce_life(lives, heart_sprites):
    for heart in heart_sprites:
        if heart.life == lives:
            heart_sprites.remove(heart)

# text messages for main()
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def health_msg(lives):
    healthText = pygame.font.Font('freesansbold.ttf', heart_height)
    if lives <= 0:
        TextSurface, TextRect = text_objects("No lives left", healthText, RED)
        TextRect.center = (health_msg_width + 50, 40)
    else:
        TextSurface, TextRect = text_objects("Lives:", healthText, RED)
        TextRect.center = (health_msg_width, 40)
    screen.blit(TextSurface, TextRect)

def level_msg(level):
    levelText = pygame.font.Font('freesansbold.ttf', heart_height)
    TextSurface, TextRect = text_objects("Level: " + str(level), levelText, GREEN)
    TextRect.center = (level_msg_width, 40)
    screen.blit(TextSurface, TextRect)

def score_msg(score):
    scoreText = pygame.font.Font('freesansbold.ttf', int(heart_height * 0.5))
    TextSurface, TextRect = text_objects("Score: " + str(score), scoreText, PURPLE)
    TextRect.left = score_msg_width
    TextRect.bottom = 80
    screen.blit(TextSurface, TextRect)

def game_over_init(block_sprites):
    game_over_msg()
    play_again_msg()
    for block in block_sprites:
        block_sprites.remove(block)

def game_over_msg():
    gameText = pygame.font.Font('freesansbold.ttf', int(WIDTH / 8))
    TextSurface, TextRect = text_objects("Game Over", gameText, BLUE)
    TextRect.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(TextSurface, TextRect)

def play_again_msg():
    playText = pygame.font.Font('freesansbold.ttf', int(WIDTH / 24))
    TextSurface, TextRect = text_objects("Press r to play again", playText, LIGHTBLUE)
    TextRect.center = (WIDTH / 2, HEIGHT / 2 + int(WIDTH / 16) + 30)
    screen.blit(TextSurface, TextRect)

if __name__ == '__main__':
    main()


