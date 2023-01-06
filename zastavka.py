import os
from random import randint, random
import sys
import pygame
import random


pygame.init()
fontUI = pygame.font.Font(None, 30)


def load_image(name, colorkey='black'):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ИГРА НА ДВОИХ",
                  "Правила игры",
                  "Чемпионат",
                  "Играть Пинг-Понг",
                  "Играть Танки"]

    fon = pygame.transform.scale(load_image('чеснок.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    coord = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'), (0, 50, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        coord.append(intro_rect)
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                for rect in coord:
                    if rect.collidepoint(event.pos):
                        kuda = coord.index(rect)
                        if kuda == 4:
                            tanki()
                        if kuda == 3:
                            ping()
        pygame.display.flip()
        clock.tick(FPS)


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(screen, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                screen.blit(text, rect)
                i += 1


class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE - 3, TILE - 3)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        keys = pygame.key.get_pressed()
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(screen, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        screen.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)


def tanki():
    for _ in range(50):
        while True:
            x = randint(0, WIDTH // TILE - 1) * TILE
            y = randint(0, HEIGHT // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            fined = False
            for obj in objects:
                if rect.colliderect(obj.rect): fined = True

            if not fined: break

        Block(x, y, TILE)
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        for bullet in bullets: bullet.update()
        for obj in objects: obj.update()
        ui.update()
        screen.fill('black')
        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()
        ui.draw()
        pygame.display.update()
        clock.tick(FPS)


def ping():

    racket_w = 15  # width
    racket_h = 100  # height
    racket_speed = 8

    point_left = point_right = 0
    font = pygame.font.Font(None, 50)

    ball_r = 10
    ball_d = 2 * ball_r
    ball_speed = 4
    ball_start_x = WIDTH / 2
    ball_start_y = HEIGHT / 2
    dx = 1
    dy = -1

    screen = pygame.display.set_mode(size)

    racket_right = pygame.Rect(WIDTH - racket_w - 5, int(HEIGHT / 2 - racket_h / 2), racket_w, racket_h)
    racket_left = pygame.Rect(5, int(HEIGHT / 2 - racket_h / 2), racket_w, racket_h)
    ball = pygame.Rect(ball_start_x, ball_start_y, ball_d, ball_d)

    green = (87, 166, 57)  # Тёмный жёлто-зелёный
    racket_color = (187, 0, 10)
    clock = pygame.time.Clock()

    # pygame.display.set_caption('Ping-Pong')
    sound = pygame.mixer.Sound('data/ball_sound.mp3.mp3')
    pause = False
    game = True
    while True:
        screen.fill(green)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and racket_right.top > 0:
            racket_right.top -= racket_speed
        elif key[pygame.K_DOWN] and racket_right.bottom < HEIGHT:
            racket_right.bottom += racket_speed
        elif key[pygame.K_w] and racket_left.top > 0:
            racket_left.top -= racket_speed
        elif key[pygame.K_s] and racket_left.bottom < HEIGHT:
            racket_left.bottom += racket_speed

        pygame.draw.rect(screen, racket_color, racket_right)
        pygame.draw.rect(screen, racket_color, racket_left)
        pygame.draw.circle(screen, (255, 255, 255), ball.center, ball_r)
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

        if ball.centery < ball_r or ball.centery > HEIGHT:
            dy = -dy
            pygame.mixer.Sound.play(sound)
        elif ball.colliderect(racket_left) or ball.colliderect(racket_right):
            if ball.colliderect(racket_left):
                ball_speed += 1
            pygame.mixer.Sound.play(sound)
            dx = -dx

        if ball.centerx > WIDTH:
            point_right += 1
            ball.x = ball_start_x
            ball.y = ball_start_y

            dx = dy = 0
            goal_time = pygame.time.get_ticks()
            pause = True

        if ball.centerx < 0:
            point_left += 1
            ball.x = ball_start_x
            ball.y = ball_start_y

            dx = dy = 0
            goal_time = pygame.time.get_ticks()
            pause = True
        if pause:
            ball_speed = 4
            time = pygame.time.get_ticks()
            if time - goal_time > 2500:
                dx = random.choice((1, -1))
                dy = random.choice((1, -1))
                pause = False

        right_text = font.render(f"{point_left}", True, pygame.Color("White"))
        screen.blit(right_text, (WIDTH - 40, 20))

        left_text = font.render(f"{point_right}", True, pygame.Color("White"))
        screen.blit(left_text, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)


FPS = 50
STEP = 5
TILE = 32
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
objects = []
bullets = []
imageblock = load_image('box.png')
imgBrick = pygame.transform.scale(imageblock, (TILE, TILE))

tile_width = tile_height = 50
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
ui = UI()

start_screen()

pygame.quit()
terminate()

# додумать



