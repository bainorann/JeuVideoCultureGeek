from display import Display
from map import Room
from map import Floor
from map import show_floor
import time
from player import Player


l = r"""
██████████████████████
██                  ██
██                  ██
██                  ▹
██                  ██
██                  ██
██████████████████████"""

room_open_east = r"""
%%%%%%%%%%%%%%%%
%%            %%
%%            %%
%%            %%
%%              
%%            %%
%%            %%
%%%%%%%%%%%%%%%%"""

room_open_north = r"""
█████████    █████████
██                  ██
██                  ██
██                  ██
██                  ██
██                  ██
██████████████████████"""

room_open_south = r"""
██████████████████████
██                  ██
██                  ██
██                  ██
██                  ██
██                  ██
█████████    █████████"""

room_open_west = r"""
██████████████████████
██                  ██
██                  ██
                    ██
██                  ██
██                  ██
██████████████████████"""

#r = Room("east", l)


def test1():
    display = Display(800, 600, "ASCII Game")
    offset_x = 250
    offset_y = 200
#pixel size seems to be 8x8 for the squares
    #or 10x10 ? not sure ...
#for simplicity's sake let's define the room tiles
    while display.is_open():
        display.clear()
        display.render_ascii(room_open_east, (150, 150, 255), offset_x, offset_y)
        display.render_ascii(room_open_west, (150, 255, 150), 0, offset_y)
        display.render_char('@', (255, 255, 255), player.x, player.y, offset_x, offset_y)
        display.update()

    display.close()

def test2():
    display = Display(800, 600, "yippee")
    room1 = Room(0, 1, room_open_east, 1, 0, (150, 150, 255))
    room2 = Room(0, 1, room_open_east, 1, 1, (150, 255, 150))
    floor1 = Floor(2)
    print(floor1)
    floor1.add_room(0, 0, room1)
    floor1.add_room(0, 1, room2)
    print(floor1)
    while display.is_open():
        show_floor(floor1, display)
        display.update()

if __name__ == "__main__":
    #test1()
    test2()
