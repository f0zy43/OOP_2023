import time
from random import randint, uniform
import pygame
from pygame.draw import *


pygame.init()


FPS = 60
screen = pygame.display.set_mode((800, 600))


x, y, r = 0, 0, 1
balls = []
objects = []
score = 0
combo = 1
combo_rect = 1
hits = 0
hits_rect = 0
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [BLUE, GREEN, YELLOW, RED, MAGENTA, CYAN, WHITE, WHITE]
LEVEL_START_COUNT = [2, 4, 6, 8, 10]
COMBO_DICT = {3: 2, 5: 3, 7: 5, 9: 10}
COMBO_DICT_RECT = {3: 3, 5: 4, 7: 6, 9: 11}
level = -1
global_speed = -1


class Ball:

    def __init__(self, start_speed, parent):
        self.x = randint(100, 700)
        self.y = randint(100, 500)
        self.r = randint(30, 50)
        self.parent = parent
        self.speed = start_speed
        self.color = COLORS[randint(1, 5)]
        self.speed_x = uniform(0, start_speed)
        self.speed_y = (self.speed ** 2 - self.speed_x ** 2) ** 0.5
        circle(screen, self.color, (self.x, self.y), self.r)

    """функция перемещения шарика"""
    def move(self):
        if self.x + self.r > 800:
            self.speed_x = -self.speed_x
            self.x += (self.r - abs(self.x - 800)) * self.speed_x / abs(self.speed_x)
        if self.x - self.r < 0:
            self.speed_x = -self.speed_x
            self.x += (self.r - abs(self.x)) * self.speed_x / abs(self.speed_x)
        if self.y + self.r > 600:
            self.speed_y = -self.speed_y
            self.y += (self.r - abs(self.y - 600)) * self.speed_y / abs(self.speed_y)
        if self.y - self.r < 0:
            self.speed_y = -self.speed_y
            self.y += (self.r - abs(self.y)) * self.speed_y / abs(self.speed_y)
        if level >= 1:
            for i in objects:
                if type(i) == Ball:
                    if (i.r + self.r - self.parent.distance(i.x, i.y, self.x, self.y)) >= 0 and \
                            (self.parent.distance(i.x, i.y, self.x + i.speed_x, self.y + i.speed_y) >
                             self.parent.distance(i.x, i.y, self.x, self.y)):
                        self.speed_x, i.speed_x = i.speed_x, self.speed_x
                        self.speed_y, i.speed_y = i.speed_y, self.speed_y
        self.x += self.speed_x  
        self.y += self.speed_y
        circle(screen, self.color, (self.x, self.y), self.r)
    
    """проверка на клик по шарику"""
    def check(self, xc, yc):
        if (xc - self.x) ** 2 + (yc - self.y) ** 2 < self.r ** 2:
            return True
        else:
            return False


class Wd:

    def new_objects(self, mode):
        if mode == 1:
            objects.append(Ball(global_speed, self))

    @staticmethod
    def distance(x1, y1, x2, y2):
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return dist

    def distance_decreasing(self, ball, rect):
        dist_before = self.distance(ball.x, ball.y, (rect.x + rect.width)//2, (rect.y + rect.height)//2)
        dist_after = self.distance(ball.x - ball.speed_x, ball.y - ball.speed_y, (rect.next_x + rect.width)//2, (rect.next_y + rect.height)//2)
        if dist_after < dist_before:
            return True
        else:
            return False

    """перемещение всех шариков массива"""
    @staticmethod
    def move_all():
        for o in objects:
            o.move()

    @staticmethod
    def in_rect(rect, ball, dirx, diry):
        if rect.x < ball.x + dirx * ball.r < rect.x + rect.width:
            if rect.y < ball.y + diry * ball.r < rect.y + rect.height:
                if not (rect.next_x < ball.x + dirx * ball.r + ball.speed_x < rect.next_x + rect.width):
                    if not (rect.next_y < ball.y + diry * ball.r + ball.speed_y < rect.next_y + rect.height):
                        return True
        return False

    @staticmethod
    def vertices_in_circle(ball, xr, yr, width, height):
        if ball.check(xr, yr) or ball.check(xr + width, yr) or \
                ball.check(xr, yr + height) or ball.check(xr+width, yr + height):
            return True
        else:
            return False

    def check_all(self, xc, yc):
        global hits, hits_rect, combo, combo_rect
        for o in objects:
            if o.check(xc, yc):  
                if type(o) == Ball:
                    hits += 1
                    
                objects.remove(o)
                if len(objects) <= final_count - 1:
                    if len(objects) == final_count - 1:
                        self.new_objects(randint(0, 1))
                    else:
                        self.new_objects(randint(0, 1))
                        self.new_objects(randint(0, 1))
                if type(o) == Ball:
                    return 1     
        hits = 0

    @staticmethod
    def win(mode):
        global score
        if mode == 1:
            balls.clear()
            win_font = pygame.font.SysFont('None', 32)
            text_win = win_font.render(f"Вы выиграли! Ваш счёт {score}", False, (0, 0, 255))
            screen.blit(text_win, (350, 300))
        elif mode == -1:
            balls.clear()
            fail_font = pygame.font.SysFont('None', 32)
            text_fail = fail_font.render(f"Вы проиграли! Ваш счёт {score}", False, (255, 0, 0))
            screen.blit(text_fail, (350, 300))
        
    @staticmethod
    def click(ev):
        print(ev.pos)

    @staticmethod
    def blit_text():
        font = pygame.font.SysFont('None', 24)
        text_score = font.render(f"Уровень #{level + 1} Счёт: {score}",False, (255, 255, 255))
        screen.blit(text_score, (10, 10))

    @staticmethod
    def find_angle(x1, y1, x2, y2, speed):
        cos = (x1 * x2 + y1 * y2) / speed ** 2
        return cos

    @staticmethod
    def load_level():
        global level, global_speed, start_count, final_count, win_flag, new_level
        if level < 4:
            level += 1
            global_speed += 2
            start_count = LEVEL_START_COUNT[level]
            final_count = (start_count + 2 * (start_count + start_count))
        elif level == 4:
            win_flag = 1
        for _ in range(start_count):
            MainWindow.new_objects(randint(0, 1))
        new_level = False


MainWindow = Wd()


pygame.display.update()
clock = pygame.time.Clock()
finished = False
new_level = True
win_flag = 0
start_count = LEVEL_START_COUNT[level]
final_count = (start_count + 2 * (start_count + start_count))
last_click_time = time.time()


while not finished:
    if win_flag == 0:
        if new_level:
            MainWindow.load_level()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                MainWindow.click(event)
                response = MainWindow.check_all(event.pos[0], event.pos[1])
                if response == 2:
                    last_click_time = time.time()
                    score += combo_rect
                    if score >= final_count:
                        new_level = True
                        objects.clear()
                elif response == 1:
                    last_click_time = time.time()
                    score += combo
                    if score >= final_count:
                        new_level = True
                        objects.clear()
        MainWindow.blit_text()
        MainWindow.move_all()

    if win_flag != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        MainWindow.win(win_flag)

    pygame.display.update()
    screen.fill(BLACK)


pygame.quit()