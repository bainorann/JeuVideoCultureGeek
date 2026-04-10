from display import Display
from map import Room
import time

class Player:
    def __init__(self, x=12, y=4):
        self.hp = 10
        self.sh = 10
        self.st = 10
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"health points : {self.hp} \nshield : {self.sh} \nstrength : {self.st} \nx : {self.x} \ny : {self.y}"



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
player = Player(50,50)


def main():
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


if __name__ == "__main__":
    print(player)
    main()
