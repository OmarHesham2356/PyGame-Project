import pygame
import time
import random

WIDTH ,HEIGHT=1000,800

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE DODGE")

BG= pygame.image.load("bg.jpg")

def draw():
    WIN.blit(BG,(0,0))
    pygame.display.update()

def main():
    run = True

    while run:
        for event in pygame.event.get ():
            if event.type==pygame.QUIT:
                run = False
                break 
