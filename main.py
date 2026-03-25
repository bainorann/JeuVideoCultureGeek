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
def a(string,r,g,b):
    return f"\033[38:2::{r}:{g}:{b}m{string}\033[39m"


clear = lambda: os.system('clear')
clear()

for i in range(100):
    print(a(l,255,0,0))
    time.sleep(1)
    clear()
    print(a(l,0,255,0))
    time.sleep(1)
    clear()
