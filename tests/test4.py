from tests.layouts import room_open_1
from map import Room


def run():
    r = Room(3, 2, room_open_1, 1, 0, (150, 150, 255))
    print(r)
