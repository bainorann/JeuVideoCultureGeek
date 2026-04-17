import time
import pygame

from display import Display
from player import Player
from item import Item


class Button:
    def __init__(self, name, layout):
        self.name = name
        self.layout = layout

    def __str__(self):
        return self.layout

l_fight = r"""
██████████████████
██     FIGHT    ██
██████████████████"""

l_item = r"""
██████████████████
██     ITEM     ██
██████████████████"""

l_run = r"""
██████████████████
██      RUN     ██
██████████████████"""


def combat(display, player1, enemy1, bag):

    state = "main0"
    message=""

    selection_index = 0
    item_index = 0

    move_delay = 0.2
    last_move_time = 0
    space_last = False

    buttons = [Button("fight", l_fight), Button("item", l_item), Button("run", l_run)]

    while True:
        if not display.is_open():
            return

        display.clear()
        draw_stats(display, player1, enemy1)

        current_time = time.time()
        keys = pygame.key.get_pressed()
        space_now = keys[pygame.K_SPACE]

        if state == "end":

            if enemy1._hp <= 0:
                display.render_ascii("ENEMY DOWN", (0,255,0), 350, 300)
                if space_now and not space_last:
                    display.update()
                    return "win"

            if player1._hp <= 0:
                state_timer = time.time()
                display.render_ascii("YOU DIED", (255,0,0), 350, 300)
                if space_now and not space_last:
                    display.update()
                    return "lose"

        elif state == "main0":

            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    selection_index = (selection_index - 1) % 3
                    last_move_time = current_time

                elif keys[pygame.K_RIGHT]:
                    selection_index = (selection_index + 1) % 3
                    last_move_time = current_time

                elif space_now and not space_last:

                    if selection_index == 0:
                        message = "You attack!"
                        state_timer = time.time()
                        state = "anim_player"

                    elif selection_index == 1:
                        item_index = 0
                        state = "item"

                    elif selection_index == 2:
                        state = "run"

            for i, button in enumerate(buttons):
                col = (0,0,255) if i == selection_index else (255,255,255)
                display.render_ascii(str(button), col, 50 + i*250, 500)

        elif state == "anim_player":

            pygame.time.delay(500)
            display.render_ascii(message, (255,255,255), 350, 300)

            if time.time() - state_timer > 0.7:
                damage(player1, enemy1)
                if enemy1._hp > 0:
                    state = "main1"
                else :
                    state = "end"

        elif state == "main1":
            message = "Enemy attacks!"
            state_timer = time.time()
            state = "anim_enemy"

        elif state == "anim_enemy":

            pygame.time.delay(500)
            display.render_ascii(message, (255,255,255), 350, 300)

            if time.time() - state_timer > 0.7:
                damage(enemy1, player1)
                if player1._hp > 0:
                    state = "main0"
                else :
                    state = "end"

        elif state == "item":

            usable_items = [item for item in bag if item._qty > 0]

            if len(usable_items) == 0:
                display.render_ascii("No items!", (255,255,255), 350, 300)
                if space_now and not space_last:
                    state = "main0"

            else:
                if current_time - last_move_time > move_delay:
                    if keys[pygame.K_LEFT]:
                        item_index = (item_index - 1) % len(usable_items)
                        last_move_time = current_time

                    elif keys[pygame.K_RIGHT]:
                        item_index = (item_index + 1) % len(usable_items)
                        last_move_time = current_time

                    elif space_now and not space_last:
                        item = usable_items[item_index]
                        use(item, player1)
                        state = "main1"
                    
                    elif keys[pygame.K_ESCAPE]:
                        state = "main0"

                for i, item in enumerate(usable_items):
                    col = (0,0,255) if i == item_index else (255,255,255)
                    display.render_ascii(f"{item._name} x{item._qty}", col, 50 + (i%4)*200,300 + int(i/4)*20)

        elif state == "run":
            display.render_ascii("You ran away...", (255,255,255), 325, 300)
            display.update()
            pygame.time.delay(700)
            return "quit"

        space_last = space_now
        display.update()

def damage(attacker, defender):
    dmg = int(3 * attacker._st / 10)
    defender._sh -= dmg
    if defender._sh < 0:
        defender._hp += defender._sh
        defender._sh = 0
    if defender._hp < 0:
        defender._hp = 0

def use(item, player):
    player._hp += item._hp
    player._sh += item._sh
    player._st += item._st
    item._qty -= 1

def draw_stats(display, player, enemy):
    display.render_ascii(
        f"PLAYER  HP:{player._hp} SH:{player._sh} ST:{player._st}",
        (255,255,255),
        50,
        50
    )

    display.render_ascii(
        f"ENEMY   HP:{enemy._hp} SH:{enemy._sh} ST:{enemy._st}",
        (255,255,255),
        50,
        80
    )

# TEST

if __name__ == "__main__":
    d = Display(800, 600, "Combat")

    j = Player()
    e = Player()
    e._sh = 4
    e._st = 5

    potion = Item('potion',5,0,0,2)
    shield = Item('shield',0,2,0,1)
    sword = Item('sword',0,0,4,1)
    potion1 = Item('potion',5,0,0,1)
    potion2 = Item('potion',5,0,0,2)
    potion3 = Item('potion',5,0,0,2)
    potion4 = Item('potion',5,0,0,99)
    potion5 = Item('potion',5,0,0,0)
    potion6 = Item('potion',5,0,0,3)
    potion7 = Item('potion',5,0,0,2)
    potion8 = Item('potion',5,0,0,100)
    potion9 = Item('potion',5,0,0,2)

    bag = [potion, shield, sword, potion1, potion2, potion3, potion4, potion5, potion6, potion7, potion8, potion9]

    combat(d, j, e, bag)