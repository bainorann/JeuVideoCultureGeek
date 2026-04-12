import os
import time
import pygame

from display import Display

class Button:
    def __init__(self, action, layout_in):
        self.action = action
        self.layout = layout_in
    def __str__(self):
        return self.layout
    
fight = r"""
██████████████████
██     FIGHT    ██
██████████████████"""

heal = r"""
██████████████████
██     HEAL     ██
██████████████████"""

run = r"""
██████████████████
██      RUN     ██
██████████████████"""

def main():
    display = Display(800, 600, "ASCII Game")
    selection_index = 0

    move_delay = 0.2
    last_move_time = 0

    while display.is_open():
        display.clear()

        current_time = time.time()
        keys = pygame.key.get_pressed()

        if current_time - last_move_time > move_delay:
            if keys[pygame.K_LEFT]:
                selection_index = (selection_index - 1) % 3
                last_move_time = current_time

            elif keys[pygame.K_RIGHT]:
                selection_index = (selection_index + 1) % 3
                last_move_time = current_time

        buttons = [fight, heal, run]

        for i, text in enumerate(buttons):
            col = (0, 0, 255) if i == selection_index else (255, 255, 255)
            display.render_ascii(text, col, 50 + i * 250, 500)

        display.update()

    display.close()

if __name__ == "__main__":
    main()