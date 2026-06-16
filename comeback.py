import os
import time
import pygame
from display import Display

yes = r"""
██████████████████
██      OUI     ██
██████████████████"""

no = r"""
██████████████████
██      NON     ██
██████████████████"""

def ascii_size(display, text):
    """Largeur/hauteur en pixels d'un bloc ascii (texte multi-lignes),
    cohérent avec la façon dont Display.render_ascii le découpe."""
    lines = text.strip().split('\n')
    w = max(len(line) for line in lines) * display._fontw
    h = len(lines) * display._fonth
    return w, h


def retour(display):
    
    space_last = True
    arrows_last = False
    state = 0
    msg=r"""Voulez-vous retourner en ville ?
(Cela vous permettra de conserver l'argent gagné.)"""

    lg, _ = ascii_size(display, msg)

    running = True

    SW, SH = display.screen.get_size()
    w, h = ascii_size(display, yes)

    while running:
        if not display.is_open():
            return

        display.clear()
        display.render_ascii(msg, (255, 255, 255), (SW-lg)//2, SH//2 - 100)

        current_time = time.time()
        keys = pygame.key.get_pressed()
        space_now = keys[pygame.K_RETURN]
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        if keys[pygame.K_ESCAPE]:
            running = False

        if state==0:
            display.render_ascii(yes, (0, 0, 255), (SW-w)//2 - 100, SH//2 + 50)
            display.render_ascii(no, (255, 255, 255), (SW-w)//2 + 100, SH//2 + 50)
        else :
            display.render_ascii(yes, (255, 255, 255), (SW-w)//2 - 100, SH//2 + 50)
            display.render_ascii(no, (0, 0, 255), (SW-w)//2 + 100, SH//2 + 50)
        
        if not arrows_last and (left or right) :
            state = (state+1)%2

        if not space_last and space_now :
            if state==0:
                return True
            else :
                return False

        space_last = space_now
        arrows_last = (left or right)
        display.update()

    return

if __name__ == "__main__":
    d = Display()
    retour(d)