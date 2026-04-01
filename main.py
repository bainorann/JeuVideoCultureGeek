import os
import time

from display import Display


class Joueur:
    def __init__(self):
        self.hp = 10
        self.sh = 10
        self.st = 10
    
    def __str__(self):
        return f"health points : {self.hp} \nshield : {self.sh} \nstrength : {self.st}"


class Room:
    def __init__(self, door_in, layout_in):
        self.door = door_in
        self.layout = layout_in
    def __str__(self):
        return self.layout


j = Joueur()

l = r"""
██████████████████████
██                  ██
██                  ██
██                  ▹
██                  ██
██                  ██
██████████████████████"""

room_open_east = r"""
██████████████████████
██                  ██
██                  ██
██                  
██                  ██
██                  ██
██████████████████████"""

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

r = Room("east", l)


def main():
    display = Display(800, 600, "ASCII Game")

    while display.is_open():
        display.clear()
        display.render_ascii(l, 250, 200)
        display.update()

    display.close()


if __name__ == "__main__":
    main()
