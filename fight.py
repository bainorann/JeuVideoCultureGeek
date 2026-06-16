import time
import math
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
██   ATTAQUER   ██
██████████████████"""

l_item = r"""
██████████████████
██    OBJETS    ██
██████████████████"""

l_run = r"""
██████████████████
██     FUIR     ██
██████████████████"""

monster = r"""'
             |
             |
             |
             |
             |
             |
             |
             |
             |
        \/   |    \/  
        ||   |    ||
        ------------
       <  [•]  [•]   >
}======<  [•]  [•]   >======{
       <  [•]  [•]   >
}======<  [•]  [•]   >======{
       <     ww      >
        ------------
          ||   ||
          /\   /\ """

monster_hit = r"""'
             |
             |
             |
             |
             |
             |
             |
             X
            /|\
        \/   |    \/  
        ||   |    ||
        ------------
       <  [x]  [x]   >
}======<  [x]  [x]   >======{
       <  [x]  [x]   >
}======<  [x]  [x]   >======{
       <     ~~      >
        ------------
          ||   ||
          /\   /\ """

monster_attack = r"""'
             |
             |
             |
       >>>   |
      >>>>>  |
       >>>   |
             |
             |
             |
        \/   |    \/  
        ||   |    ||
        ------------
       <  [>]  [>]   >
}======<  [>]  [>]   >======{
       <  [>]  [>]   >
}======<  [>]  [>]   >======{
       <    >>>      >
        ------------
          ||   ||
          /\   /\ """

# ──────────────────────────────────────────────
#  Paramètres du mini-jeu "Bob-it Smash"
# ──────────────────────────────────────────────

DIFFICULTIES = [
    {"name": "FACILE",    "speed": 2.2, "zone": 0.34, "crit": 0.14,
     "hit_mult": 0.5, "crit_mult": 1, "miss_mult": 0},
    {"name": "MOYEN",     "speed": 3.4, "zone": 0.24, "crit": 0.10,
     "hit_mult": 1, "crit_mult": 2, "miss_mult": 0},
    {"name": "DIFFICILE", "speed": 4.8, "zone": 0.16, "crit": 0.07,
     "hit_mult": 2, "crit_mult": 3, "miss_mult": 0},
    {"name": "EXPERT",    "speed": 6.5, "zone": 0.10, "crit": 0.045,
     "hit_mult": 3, "crit_mult": 4, "miss_mult": 0},
]

QTE_ATTACK_TIME_LIMIT = 4.0
QTE_DEFEND_TIME_LIMIT = 3.0

COLOR_TRACK        = ( 60,  60,  60)
COLOR_BORDER       = (255, 255, 255)
COLOR_ZONE         = ( 70, 170,  70)
COLOR_CRIT         = (255, 210,   0)
COLOR_CURSOR_OUT   = (220,  60,  60)
COLOR_CURSOR_ZONE  = (255, 255, 255)
COLOR_CURSOR_CRIT  = (  0,   0,   0)


def qte_result(pos, zone, crit):
    dist = abs(pos - 0.5)
    if dist <= crit / 2:
        return "crit"
    elif dist <= zone / 2:
        return "hit"
    else:
        return "miss"


def defend_params(enemy):
    speed = 2.5 + enemy._st * 0.4
    zone  = max(0.10, 0.32 - enemy._st * 0.02)
    crit  = max(0.04, zone * 0.35)
    return speed, zone, crit


def draw_qte_bar(display, pos, zone, crit, title, hint):
    screen = display.screen
    SW, SH = screen.get_size()

    bar_w = int(SW * 0.55)
    bar_h = 40
    bar_x = SW // 2 - bar_w // 2
    bar_y = SH - 140

    # Piste
    pygame.draw.rect(screen, COLOR_TRACK, (bar_x, bar_y, bar_w, bar_h), border_radius=10)

    # Zone "touché"
    zone_w = int(bar_w * zone)
    zone_x = bar_x + (bar_w - zone_w) // 2
    pygame.draw.rect(screen, COLOR_ZONE, (zone_x, bar_y, zone_w, bar_h))

    # Zone "critique"
    crit_w = int(bar_w * crit)
    crit_x = bar_x + (bar_w - crit_w) // 2
    pygame.draw.rect(screen, COLOR_CRIT, (crit_x, bar_y, crit_w, bar_h))

    # Bordure
    pygame.draw.rect(screen, COLOR_BORDER, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=10)

    # Curseur
    dist = abs(pos - 0.5)
    if dist <= crit / 2:
        cursor_col = COLOR_CURSOR_CRIT
    elif dist <= zone / 2:
        cursor_col = COLOR_CURSOR_ZONE
    else:
        cursor_col = COLOR_CURSOR_OUT

    cur_x = bar_x + int(pos * bar_w)
    pygame.draw.line(screen, cursor_col, (cur_x, bar_y - 14), (cur_x, bar_y + bar_h + 14), 5)

    # Textes centrés sur la barre
    display.render_ascii(title, (255, 255, 255), bar_x, bar_y - 54)
    display.render_ascii(hint,  (190, 190, 190), bar_x, bar_y + bar_h + 18)


def ascii_size(display, text):
    """Largeur/hauteur en pixels d'un bloc ascii (texte multi-lignes),
    cohérent avec la façon dont Display.render_ascii le découpe."""
    lines = text.strip().split('\n')
    w = max(len(line) for line in lines) * display._fontw
    h = len(lines) * display._fonth
    return w, h


def enemy_sprite_position(display, enemy_sprite, bottom_limit, top_margin=None):
    """Calcule (x, y) pour afficher `enemy_sprite` centré horizontalement
    sur l'écran, et centré verticalement dans la zone comprise entre
    `top_margin` et `bottom_limit` (au-dessus des boutons / de la barre QTE),
    quelle que soit la taille du sprite."""
    screen = display.screen
    SW, SH = screen.get_size()

    if top_margin is None:
        top_margin = int(SH * 0.03)

    w, h = ascii_size(display, enemy_sprite)

    x = SW // 2 - w // 2

    available = max(0, bottom_limit - top_margin)
    y = top_margin + max(0, (available - h) // 2)

    return x, y


def draw_centered_title(display, text, color, y_ratio=0.30):
    """Affiche un texte centré horizontalement à une hauteur relative."""
    screen = display.screen
    SW, SH = screen.get_size()
    # Estimation de la largeur : 8px par caractère en police monospace basique
    approx_w = len(text) * 8
    x = SW // 2 - approx_w // 2
    y = int(SH * y_ratio)
    display.render_ascii(text, color, x, y)


def draw_end_screen(display, win):
    """Affiche l'écran de fin de combat, bien centré."""
    screen = display.screen
    SW, SH = screen.get_size()

    if win:
        lines = [
            ("V I C T O I R E !",  (0, 255, 100)),
            ("",                    (255, 255, 255)),
            ("L'ennemi a été vaincu.",  (200, 255, 200)),
            ("",                    (255, 255, 255)),
            ("[ ENTREE ] pour continuer", (180, 180, 180)),
        ]
    else:
        lines = [
            ("D E F A I T E . . .", (255, 60, 60)),
            ("",                    (255, 255, 255)),
            ("Vous avez succombé à vos blessures.", (255, 180, 180)),
            ("",                    (255, 255, 255)),
            ("[ ENTREE ] pour continuer", (180, 180, 180)),
        ]

    # Boîte centrale semi-transparente
    box_w = int(SW * 0.55)
    box_h = 180
    box_x = SW // 2 - box_w // 2
    box_y = SH // 2 - box_h // 2 - 20

    overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (box_x, box_y))
    pygame.draw.rect(screen,
                     (0, 255, 100) if win else (255, 60, 60),
                     (box_x, box_y, box_w, box_h), 2, border_radius=10)

    line_h = box_h // (len(lines) + 1)
    for i, (text, color) in enumerate(lines):
        approx_w = len(text) * 8
        x = SW // 2 - approx_w // 2
        y = box_y + line_h * (i + 1) - 8
        display.render_ascii(text, color, x, y)


def draw_result_message(display, message, msg_color):
    """Affiche le message de résultat dans la zone inférieure, bien lisible, loin du sprite."""
    screen = display.screen
    SW, SH = screen.get_size()
    # Boîte de fond semi-transparente
    box_w = max(len(message) * 10 + 40, 260)
    box_h = 36
    box_x = SW // 2 - box_w // 2
    box_y = SH - 80
    overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (box_x, box_y))
    approx_w = len(message) * 8
    display.render_ascii(message, msg_color, SW // 2 - approx_w // 2, box_y + 10)


def anim_hit_enemy(display, enemy_sprite, player1, enemy1, message, msg_color):
    """Flash d'impact sur l'ennemi : alterne entre le sprite normal coloré en rouge
    et un overlay de flash blanc, indépendamment du sprite utilisé."""
    screen = display.screen
    SW, SH = screen.get_size()

    # séquence : (couleur du sprite, intensité du flash blanc 0-255, décalage x)
    frames = [
        ((255, 255, 255), 0,   0),
        ((255,  80,  80), 200, -8),
        ((255, 160, 160), 80,   6),
        ((255,  60,  60), 220, -4),
        ((255, 255, 255), 0,   0),
    ]

    for sprite_col, flash_alpha, offset_x in frames:
        display.clear()
        draw_stats(display, player1, enemy1)
        monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, SH - 200)
        monster_x += offset_x
        display.render_ascii(enemy_sprite, sprite_col, monster_x, monster_y)

        if flash_alpha > 0:
            flash = pygame.Surface((SW, SH), pygame.SRCALPHA)
            flash.fill((255, 60, 60, flash_alpha))
            screen.blit(flash, (0, 0))

        draw_result_message(display, message, msg_color)
        display.update()
        pygame.time.delay(110)


def anim_player_hit(display, enemy_sprite, player1, enemy1, message, msg_color):
    """Flash blanc à l'écran quand le joueur subit des dégâts."""
    screen = display.screen
    SW, SH = screen.get_size()

    flash_sequence = [200, 120, 60, 0]

    for alpha in flash_sequence:
        display.clear()
        draw_stats(display, player1, enemy1)
        monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, SH - 200)
        display.render_ascii(enemy_sprite, (255, 255, 255), monster_x, monster_y)

        if alpha > 0:
            flash = pygame.Surface((SW, SH), pygame.SRCALPHA)
            flash.fill((255, 255, 255, alpha))
            screen.blit(flash, (0, 0))

        draw_result_message(display, message, msg_color)
        display.update()
        pygame.time.delay(100)


def combat(display, player1, enemy1, bag, sprite=None):

    if sprite==None:
        enemy_sprite = monster
    else:
        with open(sprite, "r", encoding="utf-8") as f:
            enemy_sprite = f.read()

    """
    enemy_sprite : chaîne ASCII représentant l'ennemi.
    Si omis, on utilise le sprite 'monster' défini dans ce fichier.
    """
    if enemy_sprite is None:
        enemy_sprite = monster
    else : 
        with open(enemy_sprite, "r", encoding = "utf-8") as f:
            enemy_sprite = f.read()

    state = "main0"
    message = ""
    msg_color = (255, 255, 255)

    selection_index = 0
    item_index = 0

    move_delay = 0.2
    last_move_time = 0
    space_last = False

    buttons = [Button("fight", l_fight), Button("item", l_item), Button("run", l_run)]

    diff_index     = 0
    dmg_multiplier = 1.0

    qte_speed     = 0.0
    qte_zone      = 0.0
    qte_crit      = 0.0
    qte_hit_mult  = 1.0
    qte_crit_mult = 1.0
    qte_miss_mult = 1.0
    qte_start      = 0.0
    qte_time_limit = 0.0
    state_timer    = 0.0

    while True:
        if not display.is_open():
            return

        display.clear()
        screen = display.screen
        SW, SH = screen.get_size()
        draw_stats(display, player1, enemy1)

        current_time = time.time()
        keys = pygame.key.get_pressed()
        space_now = keys[pygame.K_RETURN]

        # ── Écran de fin ─────────────────────────────────────────────
        if state == "end":
            win = enemy1._hp <= 0
            draw_end_screen(display, win)
            if space_now and not space_last:
                display.update()
                return "win" if win else "lose"

        # ── Menu principal ────────────────────────────────────────────
        elif state == "main0":

            # Ennemi centré, au-dessus des boutons
            btn_y = SH - 160
            monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, btn_y - 10)
            display.render_ascii(enemy_sprite, (255, 255, 255), monster_x, monster_y)

            # Boutons centrés et espacés régulièrement
            btn_count  = len(buttons)
            btn_spacing = SW // (btn_count + 1)
            for i, button in enumerate(buttons):
                col = (80, 80, 255) if i == selection_index else (255, 255, 255)
                bx = btn_spacing * (i + 1) - 90
                display.render_ascii(str(button), col, bx, btn_y)

            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    selection_index = (selection_index - 1) % 3
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    selection_index = (selection_index + 1) % 3
                    last_move_time = current_time
                elif space_now and not space_last:
                    if selection_index == 0:
                        state = "select_difficulty"
                    elif selection_index == 1:
                        item_index = 0
                        state = "item"
                    elif selection_index == 2:
                        state = "run"

        # ── Sélection de la difficulté ────────────────────────────────
        elif state == "select_difficulty":

            # Titre centré
            title = "CHOISISSEZ LA DIFFICULTE"
            approx_w = len(title) * 8
            display.render_ascii(title, (255, 255, 255), SW // 2 - approx_w // 2, SH // 2 - 80)

            diff_spacing = SW // (len(DIFFICULTIES) + 1)
            for i, d in enumerate(DIFFICULTIES):
                col = (80, 80, 255) if i == diff_index else (255, 255, 255)
                dx = diff_spacing * (i + 1) - len(d["name"]) * 4
                display.render_ascii(d["name"], col, dx, SH // 2 - 10)

            hint = "<- -> choisir   ENTREE valider   BACKSPACE annuler"
            approx_w = len(hint) * 8
            display.render_ascii(hint, (160, 160, 160), SW // 2 - approx_w // 2, SH // 2 + 50)

            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    diff_index = (diff_index - 1) % len(DIFFICULTIES)
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    diff_index = (diff_index + 1) % len(DIFFICULTIES)
                    last_move_time = current_time
                elif space_now and not space_last:
                    d = DIFFICULTIES[diff_index]
                    qte_speed     = d["speed"]
                    qte_zone      = d["zone"]
                    qte_crit      = d["crit"]
                    qte_hit_mult  = d["hit_mult"]
                    qte_crit_mult = d["crit_mult"]
                    qte_miss_mult = d["miss_mult"]
                    qte_start      = time.time()
                    qte_time_limit = QTE_ATTACK_TIME_LIMIT
                    state = "attack_qte"
                elif keys[pygame.K_BACKSPACE]:
                    state = "main0"

        # ── QTE Attaque ───────────────────────────────────────────────
        elif state == "attack_qte":

            monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, SH - 200)
            display.render_ascii(enemy_sprite, (255, 255, 255), monster_x, monster_y)

            elapsed = time.time() - qte_start
            pos = (math.sin(elapsed * qte_speed) + 1) / 2

            draw_qte_bar(display, pos, qte_zone, qte_crit,
                         "ATTAQUE - frappez au bon moment !",
                         "[ ENTREE ] pour frapper")

            result = None
            if space_now and not space_last:
                result = qte_result(pos, qte_zone, qte_crit)
            elif elapsed > qte_time_limit:
                result = "miss"

            if result is not None:
                if result == "crit":
                    dmg_multiplier = qte_crit_mult
                    message   = "*** COUP CRITIQUE ! ***"
                    msg_color = (255, 220, 0)
                    state = "anim_player"
                elif result == "hit":
                    dmg_multiplier = qte_hit_mult
                    message   = "Touche !"
                    msg_color = (100, 255, 100)
                    state = "anim_player"
                else:
                    # Coup raté : pas d'animation, transition directe
                    dmg_multiplier = qte_miss_mult
                    damage(player1, enemy1, dmg_multiplier)
                    display.clear()
                    draw_stats(display, player1, enemy1)
                    monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, SH - 200)
                    display.render_ascii(enemy_sprite, (255, 255, 255), monster_x, monster_y)
                    draw_result_message(display, "Coup manque...", (180, 180, 180))
                    display.update()
                    pygame.time.delay(700)
                    state = "end" if enemy1._hp <= 0 else "main1"

        # ── Animation attaque joueur (hit ou critique uniquement) ─────
        elif state == "anim_player":
            anim_hit_enemy(display, enemy_sprite, player1, enemy1, message, msg_color)
            damage(player1, enemy1, dmg_multiplier)
            pygame.time.delay(300)
            state = "end" if enemy1._hp <= 0 else "main1"

        # ── Transition vers défense ───────────────────────────────────
        elif state == "main1":
            speed, zone, crit = defend_params(enemy1)
            qte_speed      = speed
            qte_zone       = zone
            qte_crit       = crit
            qte_start      = time.time()
            qte_time_limit = QTE_DEFEND_TIME_LIMIT
            state = "defend_qte"

        # ── QTE Défense ───────────────────────────────────────────────
        elif state == "defend_qte":

            # L'ennemi s'affiche normalement, sans pose spéciale
            monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, SH - 200)
            display.render_ascii(enemy_sprite, (255, 255, 255), monster_x, monster_y)

            elapsed = time.time() - qte_start
            pos = (math.sin(elapsed * qte_speed) + 1) / 2

            draw_qte_bar(display, pos, qte_zone, qte_crit,
                         "DEFENSE - parez l'attaque ennemie !",
                         "[ ENTREE ] pour parer")

            result = None
            if space_now and not space_last:
                result = qte_result(pos, qte_zone, qte_crit)
            elif elapsed > qte_time_limit:
                result = "miss"

            if result is not None:
                if result == "crit":
                    dmg_multiplier = 0.0
                    message   = "*** PARADE PARFAITE ! ***"
                    msg_color = (0, 220, 255)
                elif result == "hit":
                    dmg_multiplier = 0.5
                    message   = "Coup paré !"
                    msg_color = (100, 200, 255)
                else:
                    dmg_multiplier = 1.0
                    message   = "Touché par l'ennemi !"
                    msg_color = (255, 80, 80)
                state = "anim_enemy"

        # ── Animation résultat de parade ──────────────────────────────
        elif state == "anim_enemy":
            damage(enemy1, player1, dmg_multiplier)
            if dmg_multiplier > 0:
                # Flash blanc : le joueur a subi des dégâts
                anim_player_hit(display, enemy_sprite, player1, enemy1, message, msg_color)
            else:
                # Parade parfaite : simple affichage du message, pas de flash
                display.clear()
                draw_stats(display, player1, enemy1)
                monster_x, monster_y = enemy_sprite_position(display, enemy_sprite, SH - 200)
                display.render_ascii(enemy_sprite, (255, 255, 255), monster_x, monster_y)
                draw_result_message(display, message, msg_color)
                display.update()
                pygame.time.delay(700)
            state = "end" if player1._hp <= 0 else "main0"

        # ── Inventaire ────────────────────────────────────────────────
        elif state == "item":

            usable_items = [item for item in bag if item._qty > 0]

            if len(usable_items) == 0:
                no_item_msg = "Aucun objet disponible !"
                approx_w = len(no_item_msg) * 8
                display.render_ascii(no_item_msg, (255, 255, 255), SW // 2 - approx_w // 2, SH // 2)
                hint = "[ ENTREE ] pour revenir"
                approx_w = len(hint) * 8
                display.render_ascii(hint, (160, 160, 160), SW // 2 - approx_w // 2, SH // 2 + 30)
                if space_now and not space_last:
                    state = "main0"
            else:
                title = "INVENTAIRE"
                approx_w = len(title) * 8
                display.render_ascii(title, (255, 220, 80), SW // 2 - approx_w // 2, SH // 2 - 120)

                cols = 4
                col_w = SW // (cols + 1)
                for i, item in enumerate(usable_items):
                    col_idx = i % cols
                    row_idx = i // cols
                    col_sel = (80, 80, 255) if i == item_index else (255, 255, 255)
                    ix = col_w * (col_idx + 1) - 40
                    iy = SH // 2 - 60 + row_idx * 28
                    display.render_ascii(f"{item._name} x{item._qty}", col_sel, ix, iy)

                hint2 = "Flèches: naviguer   ENTREE: utiliser   BACKSPACE: annuler"
                approx_w = len(hint2) * 8
                display.render_ascii(hint2, (160, 160, 160), SW // 2 - approx_w // 2, SH - 60)

                if current_time - last_move_time > move_delay:
                    if keys[pygame.K_LEFT]:
                        item_index = (item_index - 1) % len(usable_items)
                        last_move_time = current_time
                    elif keys[pygame.K_RIGHT]:
                        item_index = (item_index + 1) % len(usable_items)
                        last_move_time = current_time
                    elif keys[pygame.K_DOWN]:
                        item_index = min(item_index + cols, len(usable_items) - 1)
                        last_move_time = current_time
                    elif keys[pygame.K_UP]:
                        item_index = max(item_index - cols, 0)
                        last_move_time = current_time
                    elif space_now and not space_last:
                        item = usable_items[item_index]
                        use(item, player1)
                        # Utilisation d'objet : pas d'animation, tour ennemi direct
                        state = "main1"
                    elif keys[pygame.K_BACKSPACE]:
                        state = "main0"

        # ── Fuite ─────────────────────────────────────────────────────
        elif state == "run":
            flee_msg = "Vous avez fui le combat..."
            approx_w = len(flee_msg) * 8
            display.render_ascii(flee_msg, (200, 200, 200), SW // 2 - approx_w // 2, SH // 2)
            display.update()
            pygame.time.delay(900)
            return "quit"

        if keys[pygame.K_ESCAPE]:
            return "quit"

        space_last = space_now
        display.update()


def damage(attacker, defender, multiplier=1.0):
    dmg = int(3 * attacker._st / 10 * multiplier)
    defender._sh -= dmg
    if defender._sh < 0:
        defender._hp += defender._sh
        defender._sh = 0
    if defender._hp < 0:
        defender._hp = 0
    return dmg

def use(item, player):
    player._hp += item._hp
    player._sh += item._sh
    player._st += item._st
    item._qty -= 1

def draw_stats(display, player, enemy):
    screen = display.screen
    SW, SH = screen.get_size()
    display.render_ascii(
        f"JOUEUR  PV:{player._hp}  Bouclier:{player._sh}  Force:{player._st}",
        (100, 220, 255),
        30, 20
    )
    display.render_ascii(
        f"ENNEMI  PV:{enemy._hp}  Bouclier:{enemy._sh}  Force:{enemy._st}",
        (255, 100, 100),
        SW - 420, 20
    )


# ── TEST ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    d = Display(800, 600, "Combat")

    j = Player()
    e = Player()
    e._sh = 20
    e._hp = 40
    e._st = 10

    potion  = Item('potion',  5, 0, 0, 2)
    shield  = Item('bouclier',0, 2, 0, 1)
    sword   = Item('epee',    0, 0, 4, 1)
    potion1 = Item('potion',  5, 0, 0, 1)
    potion2 = Item('potion',  5, 0, 0, 2)
    potion3 = Item('potion',  5, 0, 0, 2)
    potion4 = Item('potion',  5, 0, 0, 99)
    potion5 = Item('potion',  5, 0, 0, 0)
    potion6 = Item('potion',  5, 0, 0, 3)
    potion7 = Item('potion',  5, 0, 0, 2)
    potion8 = Item('potion',  5, 0, 0, 100)
    potion9 = Item('potion',  5, 0, 0, 2)

    bag = [potion, shield, sword, potion1, potion2, potion3, potion4,
           potion5, potion6, potion7, potion8, potion9]

    result = combat(d, j, e, bag)
    print("Résultat :", result)