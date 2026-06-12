from tests.layouts import room_open_1
from tests.helpers import make_display
from map import Room, Floor, show_floor
from map import print_mat
from player import Player
from input_handler import handle_input


def run():
    player = Player()
    display = make_display()
    floor = Floor()
    room0 = Room(3, 2, room_open_1, 1, 0, (150, 150, 255))
    print_mat(room0.mat())
    floor.add_room(0, 0, room0)
    running = True
    while running:
        running = handle_input(player, floor)
        show_floor(floor, display)
        print("localx :", player.localx(), ", localy :", player.localy())
        display.render_char(
            '@', (255, 255, 255),
            player.localx(), player.localy(),
            player.x(), player.y()
        )
        display.update()
    display.close()
