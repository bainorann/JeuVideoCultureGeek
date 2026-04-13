from display import Display
from dialogue import dialogue
from map import Room
import time
import pygame

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

#r = Room("east", l)
player = Player(50,50)


def main():
    display = Display(800, 600, "ASCII Game")
    offset_x = 250
    offset_y = 200
    space_pressed_last_frame = False

    while display.is_open():

        current_time = time.time()

        display.clear()
        display.render_ascii(room_open_east, (150, 150, 255), offset_x, offset_y)
        display.render_ascii(room_open_west, (150, 255, 150), 8, offset_y + 10)
        display.render_char('@', (255, 255, 255), player.x, player.y, offset_x, offset_y)
        display.update()
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        space_pressed_now = keys[pygame.K_SPACE]

        if space_pressed_now and not space_pressed_last_frame:
            dialogue(display, "test.txt", "test.txt")

        space_pressed_last_frame = space_pressed_now

        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        player.move(dx, dy)

        display.update()

    display.close()


if __name__ == "__main__":
    print(player)
    main()
