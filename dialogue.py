import os
import time
import pygame

box = r"""
████████████████████████████████████████████████████████████████
██                                                            ██
██                                                            ██
██                                                            ██
██                                                            ██
██                                                            ██
████████████████████████████████████████████████████████████████
"""

def dialogue(display, text_file, portrait_file):
    with open(text_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    line_index = 0

    TEXT_X = 90
    TEXT_Y = 450
    LINE_SPACING = 20
    MAX_LINES = 4

    space_pressed_last_frame = True

    running = True

    while running:
        if not display.is_open():
            return

        display.clear()

        current_time = time.time()
        keys = pygame.key.get_pressed()
        space_pressed_now = keys[pygame.K_SPACE]

        display.render_ascii(box, (255, 255, 255), 50, 425)

        for i in range(MAX_LINES):
            if line_index + i < len(lines):
                line = lines[line_index + i].strip()
                display.render_ascii(
                    line,
                    (255, 255, 255),
                    TEXT_X,
                    TEXT_Y + i * LINE_SPACING
                )
        
        if space_pressed_now and not space_pressed_last_frame:
            line_index += MAX_LINES

        space_pressed_last_frame = space_pressed_now

        if line_index >= len(lines):
            running = False

        display.update()

    return