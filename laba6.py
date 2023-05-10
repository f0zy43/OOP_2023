import math
from random import choice
import random
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen1: pygame.Surface, x=40, y=450):
        self.screen = screen1
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = -0.5
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        self.x += self.vx
        self.vx += self.ax
        self.y -= self.vy
        self.vy += self.ay

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hit_test(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (obj.r + self.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen1):
        self.screen = screen1
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.b_type = 0

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event1):
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event1.pos[1] - new_ball.y), (event1.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event1):
        if event1:
            self.an = math.atan((event1.pos[1] - 450) / (event1.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (20, 450),
            (
                20 + self.f2_power * math.cos(self.an),
                450 + self.f2_power * math.sin(self.an)
            ),
            20
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.x = random.randrange(600, 780)
        self.y = random.randrange(300, 550)
        self.r = random.randrange(2, 50)
        self.vx = random.randrange(0, 10)
        self.vy = random.randrange(0, 10)
        self.ax = random.randrange(0, 1)
        self.ay = random.randrange(0, 1)
        self.color = RED
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = random.randrange(600, 780)
        self.y = random.randrange(300, 550)
        self.r = random.randrange(2, 50)
        self.vx = random.randrange(0, 10)
        self.vy = random.randrange(0, 10)
        self.ax = random.randrange(0, 1)
        self.ay = random.randrange(0, 1)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        self.x += self.vx
        self.vx += 0.1 * self.ax
        self.y -= self.vy
        self.vy += 0.1 * self.ay
        if (self.x < self.r) or (self.x > WIDTH - self.r):
            self.vx *= -1
        if (self.y < self.r) or (self.y > HEIGHT - self.r):
            self.vy *= -1

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targeting(event)

    for b in balls:
        b.move()
        if b.hit_test(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hit_test(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
    gun.power_up()

pygame.quit()