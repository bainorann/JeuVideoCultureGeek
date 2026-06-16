import math
import time

import pygame

import tests.layouts as layouts
import tests.layouts_2 as layouts2
from bank import bank
from comeback import retour
from dialogue import dialogue, show_text_screen
from enemies import Enemy
from fight import combat
from input_handler import handle_input
from lasminas import casino_game
from map import Floor, Room, show_floor
from pages import Page
from player import Player
from shop import shop
from tests.helpers import make_display


def run():
    player = Player(1, 1)
    display = make_display("Second Floor Layout")

    pygame.mixer.music.load("assets/music/soul à la plage.wav")
    pygame.mixer.music.play(-1)
    show_text_screen(display, "title.txt")
    pygame.mixer.music.stop()

    game_state = {
        "intro": True,
        "fought_mini": False,
        "fought_boss": False,
        "talked": False,
        "debug": False,
    }
    return run_hub(True, player, display, game_state)


def run_hub(running, player, display, game_state):

    floor = Floor()

    for x in range(5):
        for y in range(4):
            layout = getattr(layouts2, f"room_{x}_{y}")
            mat = getattr(layouts2, f"room_{x}_{y}_mat")
            room = Room(mat, layout, 1, x * 4 + y, (150, 150, 255))
            floor.add_room(x, y, room)

    for x in range(5):
        for y in range(4):
            floor.visit_room(x, y)

    run_casino(display, running, player, "unfair")
    game_state["intro"] = True

    dialogue(display, "dette_casino.txt", "Arlequin.txt")

    while running:
        running = handle_input(player, floor)
        floor.visit_room(player.x(), player.y())
        show_floor(floor, display)
        display.render_char(
            "@",
            (255, 255, 255),
            player.localx(),
            player.localy(),
            player.x(),
            player.y(),
        )
        display.update()
        if (
            (player.x(), player.y()) == (4, 1)
            and player.localx() == 15
            and player.localy() <= 5
            and player.localy() >= 3
        ):
            run_dungeon(display, running, player, game_state)

        if (
            (player.x(), player.y()) == (1, 1)
            and player.localy() == 3
            and player.localx() <= 7
            and player.localx() >= 6
        ):
            if game_state["intro"]:
                dialogue(display, "comeback.txt", "Arlequin.txt")
                player.set_position(1, 1, 6, 4)
            else:
                run_casino(display, running, player, "balanced")
                player.set_position(1, 1, 6, 4)

        if (
            (player.x(), player.y()) == (3, 1)
            and player.localy() == 3
            and player.localx() <= 15
            and player.localx() >= 14
        ):
            print("yo")
            run_banque(display, running, player)

        if (
            (player.x(), player.y()) == (1, 2)
            and player.localy() == 7
            and player.localx() <= 5
            and player.localx() >= 4
        ):
            run_merchant(display, running, player)

        if (
            (player.x(), player.y()) == (4, 2)
            and player.localy() == 7
            and player.localx() <= 3
            and player.localx() >= 2
        ):
            dialogue(display, "maison.txt", "house.txt")
            player.set_position(4, 2, 1, 7)


def run_casino(display, running, player, mode):
    if running:
        pygame.mixer.music.stop()
        a = casino_game(display, player.debt(), player.money(), mode)
        print(a)
        player.min_debt(a)
        player.min_money(a)


def run_banque(display, running, player):
    if running:
        bank(display, player)
        player.set_position(3, 1, 13, 3)


def run_merchant(display, running, player):
    if running:
        shop(display, player)
        player.set_position(1, 2, 6, 7)


def flashback_animation(display, duration=1.5):
    screen = display.screen
    SW, SH = screen.get_size()
    cx, cy = SW // 2, SH // 2
    max_r = min(SW, SH) // 2 - 40
    start = time.time()
    clock = pygame.time.Clock()
    while time.time() - start < duration:
        elapsed = time.time() - start
        display.clear()
        for i in range(12):
            radius = 30 + (elapsed * 200 + i * 40) % max_r
            angle = elapsed * 3 + i * (math.pi * 2 / 12)
            r = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)
            pygame.draw.arc(screen, (255, 255, 255), r, angle, angle + 0.8, 3)
        display.update()
        clock.tick(60)


def run_dungeon(display, running, player, game_state):
    floor = Floor()
    room_coords = [
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 5),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 4),
        (3, 5),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 0),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (6, 0),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 4),
        (7, 1),
        (7, 2),
        (7, 4),
        (7, 5),
        (8, 0),
        (8, 1),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (9, 1),
        (9, 2),
        (9, 3),
        (9, 4),
        (9, 5),
    ]

    for i, (x, y) in enumerate(room_coords):
        layout = getattr(layouts, f"room_{x}_{y}")
        mat = getattr(layouts, f"room_{x}_{y}_mat", None)
        if mat is None:
            mat = [[0 for _ in range(8)] for _ in range(16)]
        room = Room(mat, layout, 1, i, (150, 150, 255))
        floor.add_room(x, y, room)

        player.set_position(0, 2, 4, 4)  # enemy = enemies.spawn_enemy(0, 0, 2, 1)

    pages = [
        Page("page1.txt", 3, 0, 4, 4, "book.txt"),
        Page("page2.txt", 5, 0, 4, 4, "book.txt"),
        Page("page3.txt", 7, 2, 8, 4, "book.txt"),
        Page("page4.txt", 1, 4, 8, 4, "book.txt"),
        Page("page5.txt", 8, 4, 6, 4, "book.txt"),
    ]

    pygame.mixer.music.load("assets/music/prise de drogue.wav")
    pygame.mixer.music.play(-1)

    while running:
        running = handle_input(player, floor)
        floor.visit_room(player.x(), player.y())
        show_floor(floor, display)
        display.render_char(
            "@",
            (255, 255, 255),
            player.localx(),
            player.localy(),
            player.x(),
            player.y(),
        )

        for page in pages:
            if page.check(player):
                page.trigger(display)

        for page in pages:
            page.render(display)

        if (player.x(), player.y()) == (4, 2) and not game_state["talked"]:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/tks_for_playing_KLICKAUD.mp3")
            pygame.mixer.music.play(-1)
            dialogue(display, "pre_fight.txt", "player.txt")
            game_state["talked"] = True
        if (player.x(), player.y()) == (4, 3) and not game_state["fought_mini"]:
            enemy = Enemy()
            if game_state["debug"]:
                enemy._hp = 1
                enemy._sh = 1
            else:
                enemy._hp = 20
                enemy._sh = 10
            enemy._st = 8
            a = combat(display, player, enemy, player.bag, "Arlequin.txt")
            if a == "win":
                game_state["fought_mini"] = True
                saved_money = player.money()
                dialogue(display, "bonheur1.txt", "player.txt")
                player._money = 1000
                flashback_animation(display)
                run_casino(display, running, player, "fair")
                flashback_animation(display)
                dialogue(display, "postnutclarity.txt", "player.txt")
                # Le joueur conserve son argent d'avant + 50
                player.min_money(player.money())
                player._money = saved_money + 50
                # Choix : retourner en ville ou rester dans le donjon
                if retour(display):
                    pygame.mixer.music.stop()
                    player.set_position(4, 1, 13, 4)
                    display.update()
                    return
                pygame.mixer.music.load("assets/music/prise de drogue.wav")
                pygame.mixer.music.play(-1)
            elif a == "lose":
                pygame.mixer.music.stop()
                game_state["fought_mini"] = True
                game_state["intro"] = False
                player.min_money(player.money())
                player._money = 1
                dialogue(display, "perte.txt", "player.txt")
                player.set_position(4, 1, 13, 4)
                display.update()
                return
        if (player.x(), player.y()) == (9, 3) and not game_state["fought_boss"]:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/tks_for_playing_KLICKAUD.mp3")
            pygame.mixer.music.play(-1)
            dialogue(display, "exfemme.txt", "femme.txt")
            enemy = Enemy()
            if game_state["debug"]:
                enemy._hp = 1
            else:
                enemy._hp = 40
            enemy._sh = 20
            enemy._st = 12
            a = combat(display, player, enemy, player.bag, "femme.txt")
            if a == "win":
                game_state["fought_boss"] = True
                flashback_animation(display)
                saved_money = player._money
                player._money = 1000
                run_casino(display, running, player, "unfair")
                player._money = saved_money + 100
                flashback_animation(display)
                dialogue(display, "redemption1.txt", "player.txt")
                show_text_screen(display, "end.txt")
                display.close()
            else:
                dialogue(display, "defaite_boss.txt", "player.txt")
                pygame.mixer.music.stop()
                game_state["fought_mini"] = True
                game_state["intro"] = False
                player._money = 1
                player.set_position(4, 1, 13, 4)
                display.update()
                return

        display.update()
    pygame.mixer.music.stop()
    player.set_position(4, 1, 13, 4)
