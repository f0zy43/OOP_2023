import pygame
from pygame.draw import ellipse, circle

pygame.init()


class Hare:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.body_width = self.width // 2
        self.body_height = self.height // 2
        self.body_y = self.y + self.body_height // 2

        self.head_size = self.height // 4

        self.ear_height = self.height // 3
        self.ear_x_offset = self.head_size // 4

        self.leg_height = self.height // 16
        self.leg_x_offset = self.width // 4
        self.leg_y_offset = self.height // 2 - self.leg_height // 2

    def draw_body(self, surface):
        ellipse(surface, self.color,
                (self.x - self.body_width // 2, self.body_y - self.body_height // 2, self.body_width, self.body_height))

    def draw_head(self, surface):
        circle(surface, self.color, (self.x, self.y - self.head_size // 2), self.head_size // 2)

    def draw_ear(self, surface, x_offset):
        ear_x = self.x + x_offset
        ear_y = self.y - self.height // 2 + self.ear_height // 2
        ellipse(surface, self.color,
                (ear_x - self.width // 8 // 2, ear_y - self.ear_height // 2, self.width // 8, self.ear_height))

    def draw_leg(self, surface, x_offset):
        leg_x = self.x + x_offset
        leg_y = self.y + self.leg_y_offset
        ellipse(surface, self.color,
                (leg_x - self.width // 4 // 2, leg_y - self.leg_height // 2, self.width // 4, self.leg_height))

    def draw(self, surface):
        self.draw_body(surface)
        self.draw_head(surface)
        self.draw_ear(surface, -self.ear_x_offset)
        self.draw_ear(surface, self.ear_x_offset)
        self.draw_leg(surface, -self.leg_x_offset)
        self.draw_leg(surface, self.leg_x_offset)


pygame.init()

FPS = 30
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
finished = False

hare = Hare(200, 200, 100, 200, pygame.Color('white'))
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    hare.draw(screen)
    pygame.display.update()

pygame.quit()