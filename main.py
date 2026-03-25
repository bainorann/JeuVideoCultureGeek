import os
import time

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
        self.layout =  layout_in
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
r = Room("east", l)
print(r)
print(j)
print(f"\033[48:2::FF:FF:FFm \033[49m")
