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
    room_id = 0
    for y in range(6):
        for x in range(10):
            room = Room(0, 1, room_open_1, 1, room_id, (150, 150, 255))
            print_mat(room.mat())
            print(" ")
            print(" ")
            floor.add_room(x, y, room)
            room_id += 1
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
