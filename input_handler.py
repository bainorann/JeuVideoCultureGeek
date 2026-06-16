import sys

import pygame


def handle_input(player, floor):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RIGHT:
                player.move(1, 0, floor)
                # enemy.move_to_player(player, floor)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0, floor)
                # enemy.move_to_player(player, floor)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1, floor)
                # enemy.move_to_player(player, floor)
            elif event.key == pygame.K_UP:
                player.move(0, -1, floor)
                # enemy.move_to_player(player, floor)
    return True
