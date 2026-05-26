from display import Display
from display import print_mat
from map import Room
from map import Floor
from map import show_floor
import time
from player import Player
import pygame
import sys
from screen import choose_font
from input_handler import handle_input

l = r"""
██████████████████████
██                  ██
██                  ██
██                  ▹
██                  ██
██                  ██
██████████████████████"""

room_open_1 = r"""
%%%%%%%%%%%%%%%%
%%            %%
%%            %%
%%            
%%              
%%            %%
%%            %%
%%%%%%%  %%%%%%%"""

room_open_2 = r"""
%%%%%%%%%%%%%%%%
%%            %%
%%            %%
              %%            
              %%
%%            %%
%%            %%
%%%%%%%  %%%%%%%"""

room_open_3 = r"""
%%%%%%%  %%%%%%%
%%            %%
%%            %%
%%                        
%%            
%%            %%
%%            %%
%%%%%%%%%%%%%%%%"""

room_open_4 = r"""
%%%%%%%  %%%%%%%
%%            %%
%%            %%
              %%          
              %%
%%            %%
%%            %%
%%%%%%%%%%%%%%%%"""

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

def test3():
    pygame.init()
    font = pygame.font.SysFont("monospace", 29)
    print(font.size("%"))

def test4():
    r = Room(3, 2, room_open_east, 1, 0,(150, 150, 255))

def test5():
    player = Player()
    display = Display()
    floor = Floor()
    room_id = 0
    for y in range(6):
        for x in range(10):
            room = Room(0, 1, room_open_east, 1, room_id, (150, 150, 255))
            print_mat(room.mat())
            print(" ")
            print(" ")
            floor.add_room(x, y, room)
            room_id += 1
    running = True
    while running:
        running = handle_input(player, floor)
        show_floor(floor, display)
        print(f"localx : {player.localx()}, localy : {player.localy()}")
        display.render_char('@', (255, 255, 255), player.localx(), player.localy(), player.x(), player.y())
        display.update()
    display.close()

def test6():
    player = Player()
    display = Display()
    floor = Floor()
    room0 = Room(1, 2, room_open_1, 1, 0, (150, 150, 255))
    print_mat(room0.mat())
    print(" ")
    print(" ")
    floor.add_room(0, 0, room0)
    room1 = Room(2, 3, room_open_2, 1, 1, (150, 150, 255))
    print_mat(room1.mat())
    print(" ")
    print(" ")
    floor.add_room(1, 0, room1)
    room2 = Room(0, 1, room_open_3, 1, 2, (150, 150, 255))
    print_mat(room2.mat())
    print(" ")
    print(" ")
    floor.add_room(0, 1, room2)
    room3 = Room(0, 3, room_open_4, 1, 3, (150, 150, 255))
    print_mat(room3.mat())
    print(" ")
    print(" ")
    floor.add_room(1, 1, room3)
    running = True
    while running:
        running = handle_input(player, floor)
        show_floor(floor, display)
        #print(f"localx : {player.localx()}, localy : {player.localy()}")
        display.render_char('@', (255, 255, 255), player.localx(), player.localy(), player.x(), player.y())
        display.update()
    display.close()

def test7():
    player = Player()
    display = Display()
    floor = Floor()
    room0 = Room(3, 2, room_open_east, 1, 0, (150, 150, 255))
    print_mat(room0.mat())
    floor.add_room(0, 0, room0)
    running = True
    while running:
        running = handle_input(player, floor)
        show_floor(floor, display)
        print(f"localx : {player.localx()}, localy : {player.localy()}")
        display.render_char('@', (255, 255, 255), player.localx(), player.localy(), player.x(), player.y())
        display.update()
    display.close()

def test8():
    player = Player()
    display = Display()
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
        running = handle_input(player, floor)
        show_floor(floor, display)
        display.render_char('@', (255, 255, 255), player.localx(), player.localy(), player.x(), player.y())
        display.update()
    display.close()

if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    #test4()
    #test5()
    #test6()
    #test7()
    test8()
    #print(choose_font())
