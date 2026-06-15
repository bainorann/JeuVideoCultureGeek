import tests.layouts as layouts
import tests.layouts_2 as layouts2
from bank import bank
from input_handler import handle_input
from lasminas import casino_game
from map import Floor, Room, show_floor
from player import Player
from shop import shop
from tests.helpers import make_display


def run():
    player = Player(1, 1)
    return run_hub(True, player)


def run_hub(running, player):
    display = make_display("Second Floor Layout")
    floor = Floor()

    for x in range(5):
        for y in range(4):
            layout = getattr(layouts2, f"room_{x}_{y}")
            mat = getattr(layouts2, f"room_{x}_{y}_mat")
            room = Room(mat, layout, 1, x * 4 + y, (150, 150, 255))
            floor.add_room(x, y, room)

    for x in range(5):
        for y in range(4):
            floor.visit_room(x, y)

    while running:
        # print(player.x(), player.y(), player.localx(), player.localy())
        running = handle_input(player, floor)
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
        if (
            (player.x(), player.y()) == (4, 1)
            and player.localx() == 15
            and player.localy() <= 5
            and player.localy() >= 3
        ):
            run_dungeon(display, running, player)

        if (
            (player.x(), player.y()) == (1, 1)
            and player.localy() == 3
            and player.localx() <= 7
            and player.localx() >= 6
        ):
            run_casino(display, running, player)

        if (
            (player.x(), player.y()) == (3, 1)
            and player.localy() == 3
            and player.localx() <= 15
            and player.localx() >= 14
        ):
            print("yo")
            run_banque(display, running, player)

        if (
            (player.x(), player.y()) == (1, 2)
            and player.localy() == 7
            and player.localx() <= 5
            and player.localx() >= 4
        ):
            run_merchant(display, running, player)


def run_casino(display, running, player):
    if running:
        a = casino_game(display, player.debt(), player.money(), "balanced")
        player.min_debt(a)
        player.min_money(a)
        player.set_position(1, 1, 6, 4)


def run_banque(display, running, player):
    if running:
        bank(display, player)
        player.set_position(3, 1, 13, 3)


def run_merchant(display, running, player):
    if running:
        shop(display, player)
        player.set_position(1, 2, 6, 7)


def run_dungeon(display, running, player):
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

        player.set_position(0, 2, 4, 4)  # enemy = enemies.spawn_enemy(0, 0, 2, 1)
    while running:
        running = handle_input(player, floor)
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
