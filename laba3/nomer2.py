import pygame
import math as m
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1300, 550))
rect(screen, (255, 255, 255), [(0, 0), (1300, 600)])

bodily = (228,199,178)
green = (55, 125, 34)
orange = (237, 110, 45)
yellow = (249, 212, 83)
purple= (195, 69, 246)
light_green = (160, 250, 88)
black = (0, 0, 0)


def rukav(color, vertex_count, radius, position, k):
    "Функция, рисующая рукав"
    "k нужен для ориентации - правой или левой - он 1 или -1 "
    n, r = vertex_count, radius
    x, y = position
    polygon(screen, color, [
        (x + r * m.cos(2 * m.pi * i / n + k * m.pi), y + r * m.sin(2 * m.pi * i / n + k * m.pi))
        for i in range(n)
    ])
    polygon(screen, (0, 0, 0), [
        (x + r * m.cos(2 * m.pi * i / n + k * m.pi), y + r * m.sin(2 * m.pi * i / n + k * m.pi))
        for i in range(n)
    ], 1)


def volos(a, x, y, color):
    "Функция, рисующая волос"
    # а - угол через который расположены треугольники волос ~10deg
    a = a / 360 * 2 * m.pi
    polygon(screen, color, [(x + 150 * m.sin(a) - 25 * m.cos(a), y - 150 * m.cos(a) - 25 * m.sin(a)),
                            (x + 150 * m.sin(a) + 25 * m.cos(a), y - 150 * m.cos(a) + 25 * m.sin(a)),
                            (x + (150 + 35) * m.sin(a), y - (150 + 35) * m.cos(a))])
    # отрисовка границы
    polygon(screen, (0, 0, 0), [[x + 150 * m.sin(a) - 25 * m.cos(a), y - 150 * m.cos(a) - 25 * m.sin(a)],
                                (x + 150 * m.sin(a) + 25 * m.cos(a), y - 150 * m.cos(a) + 25 * m.sin(a)),
                                (x + (150 + 35) * m.sin(a), y - (150 + 35) * m.cos(a))], 1)

def face(color, x,y,R):
    #Функция, рисующая лицо
    circle(screen, color , (x, y), R )

def body(color, x,y,R):
    #функция, рисующая тело
    circle(screen, color, (x, y ), R, draw_top_left=True, draw_top_right=True)
    
def eye(color, x , y, R):
    #рисует глаз
    circle(screen, color , (x, y) , R)
    circle(screen, (0, 0, 0), (x ,y), 8/27 *R)

def palm(color, x, y, R):
    #рисует ладонь
    circle(screen, color, (x, y ), R, draw_bottom_left=True, draw_bottom_right=True)

    
def hand(color, x1, y1, x2, y2, size):
    #рисует руку
    line(screen, color, (x1,y1), (x2,y2), size)
    

    

def human(x, y, heir, eyes, shirt):

    body (shirt, x, y+200,180)
    #тело
    
    face(bodily, x, y-60, 150)
    #лицо
    
    eye(eyes, x+40, y-100, 27)
    eye(eyes, x-40, y-100, 27)
    #глаза

    polygon(screen, (113, 70, 40), [(x, y - 50), (x + 10, y - 70), (x - 10, y - 70)])  # нос
    polygon(screen, (235, 66, 56), [(x, y + 20), (x - 80, y - 40), (x + 80, y - 40)])  # рот
    
    hand(bodily, x-150, y+100, x-300, y-260, 25)
    hand(bodily, x+150, y+100, x+300, y-260, 25)
    #руки
    
    palm(bodily, x-300, y-260,33)
    palm(bodily, x+300, y-260,33)
    #ладони
    
    rukav(shirt, 5, 74, (x - 150, y + 100), 0)
    rukav(shirt, 5, 74, (x + 150, y + 100), 1)
    #рукава
    
    for i in range(-90, 105, 15):
        volos(i, x, y - 60, heir)
    #волосы
    return 0

def article(color1, color2, x,y, string):
    #рисует надпись
    rect(screen, color1, [(0, 0), (x, y)])
    rect(screen, color2, [(0, 0), (x, y)], 1)
    text = pygame.font.SysFont('pingfang', 65, True)
    follow = text.render(string , True, (0, 0, 0))
    return(follow)

def draw_all():
    #Функция рисует всю картинку
    human(550, 360, purple, (133, 178, 240), orange)
    screen.blit(article(light_green,black,1300,100, "PYTHON is REALLY AMAZING!"), (250, 7))
    




pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    draw_all()
    pygame.display.update()
pygame.quit()