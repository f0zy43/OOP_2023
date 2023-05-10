import pygame 
from pygame.draw import * 


pygame.init() 

a=1 

FPS = 30 

def smail(): 
    screen = pygame.display.set_mode((400, 400)) 
    screen.fill((255, 255, 255)) 
    circle(screen, (150, 150, 0), (200, 200), 170) 
    circle(screen, (0, 0, 0), (200, 200), 170, 5) 
    circle(screen, (100, 0, 0), (140, 140), 30) 
    circle(screen, (0, 0, 0), (135, 140), 15) 
    circle(screen, (100, 0, 0), (260, 140), 35) 
    circle(screen, (0, 0, 0), (260, 140), 15) 
    polygon(screen, (0, 0, 0), [(60, 85), (50, 75), (180, 115), (175, 120)]) 
    polygon(screen, (0, 0, 0), [(210, 120), (215, 115), (370, 75), (380, 85)]) 
    rect(screen, (0, 0, 0), (100, 260, 200, 15)) 
  
 
if a==1: 
    smail() 

pygame.display.update() 
clock = pygame.time.Clock() 
finished = False 
  
while not finished: 
    clock.tick(FPS) 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            finished = True 
  
pygame.quit()