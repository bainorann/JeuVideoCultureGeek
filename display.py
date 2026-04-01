import pygame
import sys


class Display:
    def __init__(self, width=800, height=600, title="ASCII Game"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18)
        self.background_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

    def clear(self):
        self.screen.fill(self.background_color)

    def render_ascii(self, text, text_color, x=0, y=0):
        lines = text.strip().split('\n')
        for i, line in enumerate(lines):
            surface = self.font.render(line, True, text_color)
            self.screen.blit(surface, (x, y + i * self.font.get_height()))

    def render_char(self, char, text_color, grid_x, grid_y, offset_x=0, offset_y=0):
        surface = self.font.render(char, True, text_color)
        x = offset_x + grid_x #* self.font.get_width()
        y = offset_y + grid_y #* self.font.get_height()
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
