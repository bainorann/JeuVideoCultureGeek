import sys

import pygame

from screen import choose_font


class Display:
    def __init__(self, width=800, height=600, title="ASCII Game"):
        pygame.init()
        pygame.mixer.init()
        info = pygame.display.Info()
        # screen_width = info.current_w
        # screen_height = info.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/fonts/DejaVuSansMono.ttf", choose_font())
        self.background_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self._fontw = self.font.size("          ")[0] // 10
        self._fonth = self.font.size("A")[1]

    def clear(self):
        self.screen.fill(self.background_color)

    def render_ascii(self, text, text_color, x=0, y=0):
        lines = text.strip().split("\n")
        for i, line in enumerate(lines):
            surface = self.font.render(line, True, text_color)
            self.screen.blit(surface, (x, y + i * self._fonth))

    def render_char(self, char, text_color, grid_x, grid_y, offset_x=0, offset_y=0):
        surface = self.font.render(char, True, text_color)
        x = (offset_x * 16 + grid_x) * self._fontw
        y = (offset_y * 8 + grid_y) * self._fonth
        self.screen.blit(surface, (x, y))

    def update(self):
        pygame.display.flip()
        self.clock.tick(60)

    def is_open(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def close(self):
        pygame.quit()
        sys.exit()


def print_mat(m):
    for y in range(len(m[0])):
        line = ""
        for x in range(len(m)):
            line += str(m[x][y])
        print(line)
