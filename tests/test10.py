import pygame

import enemies
import tests.layouts as layouts
from input_handler import handle_input
from map import Floor, Room, show_floor
from player import Player
from tests.helpers import make_display


def run():
    display = make_display("First Layer Layout")
    pygame.mixer.init()
    pygame.mixer.music.load("tests/tks_for_playing_KLICKAUD.mp3")
    pygame.mixer.music.play(-1)
    floor = Floor()

    room_coords = [
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 5),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 4),
        (3, 5),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 0),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (6, 0),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 4),
        (7, 1),
        (7, 2),
        (7, 4),
        (7, 5),
        (8, 0),
        (8, 1),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (9, 1),
        (9, 2),
        (9, 3),
        (9, 4),
        (9, 5),
    ]

    for i, (x, y) in enumerate(room_coords):
        layout = getattr(layouts, f"room_{x}_{y}")
        mat = getattr(layouts, f"room_{x}_{y}_mat", None)
        if mat is None:
            mat = [[0 for _ in range(8)] for _ in range(16)]
        room = Room(mat, layout, 1, i, (150, 150, 255))
        floor.add_room(x, y, room)

    player = Player(4, 3)
    enemy = enemies.spawn_enemy(0, 0, 2, 1)
    running = True
    while running:
        running = handle_input(player, floor, enemy)
        floor.visit_room(player.x(), player.y())
        show_floor(floor, display)
        display.render_char(
            "@",
            (255, 255, 255),
            player.localx(),
            player.localy(),
            player.x(),
            player.y(),
        )
        display.update()
    display.close()
