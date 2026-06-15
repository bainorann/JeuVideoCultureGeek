import tests.layouts_2 as layouts2
from input_handler import handle_input
from map import Floor, Room, show_floor
from player import Player
from tests.helpers import make_display


def run():
    display = make_display("Second Floor Layout")
    floor = Floor()

    for x in range(5):
        for y in range(4):
            layout = getattr(layouts2, f"room_{x}_{y}")
            mat = getattr(layouts2, f"room_{x}_{y}_mat")
            room = Room(mat, layout, 1, x * 4 + y, (150, 150, 255))
            floor.add_room(x, y, room)

    player = Player(1, 3)
    floor.visit_room(1, 3)

    running = True
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
