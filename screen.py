import sys

import pygame


def get_screen_info():
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    #    pygame.quit()
    return (screen_width, screen_height)


def choose_font():
    screen_w, screen_h = get_screen_info()
    #    pygame.init()
    i = 1
    Font = pygame.font.Font
    args = ("assets/fonts/DejaVuSansMono.ttf", i)
    font_w, font_h = Font(*args).size("%")

    # not widescreen
    if screen_w / screen_h <= 16 / 9:
        while font_w < int(screen_w / 160):
            print(i, screen_w)
            i += 1
            font_w, font_h = (pygame.font.SysFont("monospace", i)).size("%")

    # widescreen
    else:
        while font_h < int(screen_h / 48):
            i += 1
            font_w, font_h = (pygame.font.SysFont("monospace", i)).size("%")
    return i
