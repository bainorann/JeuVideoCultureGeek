from tests.layouts import room_open_1
from tests.helpers import make_display
from map import Room, Floor, show_floor
from player import Player
from input_handler import handle_input


def run():
    display = make_display("yippee")
    room1 = Room(0, 1, room_open_1, 1, 0, (150, 150, 255))
    room2 = Room(0, 1, room_open_1, 1, 1, (150, 255, 150))
    floor1 = Floor()
    player = Player()
    print(floor1)
    floor1.add_room(0, 0, room1)
    floor1.add_room(0, 1, room2)
    print(floor1)
    running = True
    while running:
        running = handle_input(player, floor1)
        show_floor(floor1, display)
        offset_x = player.x() * display.font.get_width() * 15
        offset_y = player.y() * display.font.get_height() * 7
        display.render_char('@', (255, 255, 255), player.localx(), player.localy(), offset_x, offset_y)
        display.update()
    display.close()
