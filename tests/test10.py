import tests.layouts as layouts
from tests.helpers import make_display
from map import Room, Floor, show_floor


def run():
    display = make_display("First Layer Layout")
    floor = Floor()

    room_coords = [
        (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2), (1, 4), (1, 5),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
        (3, 0), (3, 1), (3, 2), (3, 4), (3, 5),
        (4, 2), (4, 3), (4, 4), (4, 5),
        (5, 0), (5, 2), (5, 3), (5, 4), (5, 5),
        (6, 0), (6, 1), (6, 2), (6, 3), (6, 4),
        (7, 1), (7, 2), (7, 4), (7, 5),
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
        (9, 1), (9, 2), (9, 3), (9, 4), (9, 5),
    ]

    for i, (x, y) in enumerate(room_coords):
        layout = getattr(layouts, f'room_{x}_{y}')
        room = Room(0, 2, layout, 1, i, (150, 150, 255))
        floor.add_room(x, y, room)

    while display.is_open():
        show_floor(floor, display)
        display.update()
    display.close()
