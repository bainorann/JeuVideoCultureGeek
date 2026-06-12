import pygame
import random as rand

def handle_input(player, floor, enemy):
    for event in pygame.event.get():
        randx = rand.randint(-1, 1)
        randy = rand.randint(-1, 1)
        randside = rand.randint(0, 1)
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_RIGHT:
                player.move(1, 0, floor)
                enemy.move(randx*randside, randy*(1-randside), floor)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0, floor)
                enemy.move(randx*randside, randy*(1-randside), floor)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1, floor)
                enemy.move(randx*randside, randy*(1-randside), floor)
            elif event.key == pygame.K_UP:
                player.move(0, -1, floor)
                enemy.move(randx*randside, randy*(1-randside), floor)
    return True
