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
    font_path = "assets/fonts/DejaVuSansMono.ttf"
    Font = pygame.font.Font
    i = 1

    if screen_w / screen_h <= 16 / 9:
        font_w = Font(font_path, i).size("          ")[0] // 10
        while font_w < int(screen_w / 160):
            i += 1
            font_w = Font(font_path, i).size("          ")[0] // 10
    else:
        _, font_h = Font(font_path, i).size("A")
        while font_h < int(screen_h / 48):
            i += 1
            _, font_h = Font(font_path, i).size("A")
    return i
