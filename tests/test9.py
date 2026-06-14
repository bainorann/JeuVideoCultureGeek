import enemies
from input_handler import handle_input
from map import Floor, Room, show_floor
from player import Player
from tests.helpers import make_display
from tests.layouts import room_open_1, room_open_2, room_open_3, room_open_4


def run():
    player = Player()
    enemy = enemies.spawn_enemy(0, 0, 2, 1)
    display = make_display()
    floor = Floor()
    room0 = Room(1, 2, room_open_1, 1, 0, (150, 150, 255))
    floor.add_room(0, 0, room0)
    room1 = Room(2, 3, room_open_2, 1, 1, (150, 150, 255))
    floor.add_room(1, 0, room1)
    room2 = Room(0, 1, room_open_3, 1, 2, (150, 150, 255))
    floor.add_room(0, 1, room2)
    room3 = Room(0, 3, room_open_4, 1, 3, (150, 150, 255))
    floor.add_room(1, 1, room3)
    running = True
    while running:
        running = handle_input(player, floor, enemy)
        show_floor(floor, display)
        display.render_char(
            "@",
            (255, 255, 255),
            player.localx(),
            player.localy(),
            player.x(),
            player.y(),
        )
        display.render_char(
            "X", (255, 150, 150), enemy.localx(), enemy.localy(), enemy.x(), enemy.y()
        )
        display.update()
    display.close()
