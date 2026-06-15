import time
import pygame

from display import Display
from player import Player
from item import Item

# ── Palette ───────────────────────────────────────────────────────────────────

C_WHITE    = (255, 255, 255)
C_GREY     = (100, 100, 100)
C_DARK     = ( 30,  30,  30)
C_GOLD     = (255, 210,  50)
C_GREEN    = ( 80, 200, 120)
C_RED      = (220,  70,  70)
C_BLUE     = ( 80, 130, 255)
C_BORDER_N = (160, 140,  80)   # bordure bouton normal
C_BORDER_S = (255, 210,  50)   # bordure bouton sélectionné
C_BORDER_D = ( 55,  55,  55)   # bordure bouton désactivé


# ── Catalogue du magasin ─────────────────────────────────────────────────────
# Chaque entrée définit un type d'objet, ses bonus, son prix d'achat
# (chez le marchand) et son prix de revente (au joueur).

SHOP_STOCK = [
    {"name": "Potion Soin (I)",   "hp": 5,  "sh": 0, "st": 0, "buy": 200, "sell": 100},
    {"name": "Potion Soin (II)",   "hp": 8,  "sh": 0, "st": 0, "buy": 500, "sell": 250},
    {"name": "Potion Soin (III)",   "hp": 12,  "sh": 0, "st": 0, "buy": 1000, "sell": 500},
    {"name": "Potion Défensive (I)", "hp": 0,  "sh": 3, "st": 0, "buy": 120, "sell": 60},
    {"name": "Potion Défensive (II)", "hp": 0,  "sh": 6, "st": 0, "buy": 225, "sell": 110},
    {"name": "Potion Offensive (I)", "hp": 0,  "sh": 0, "st": 4, "buy": 200, "sell": 100},
    {"name": "Potion Offensive (II)", "hp": 0,  "sh": 0, "st": 8, "buy": 500, "sell": 250},
    {"name": "Elixir",   "hp": 3, "sh": 3, "st": 3, "buy": 700, "sell": 400},
]


# ── Helpers d'affichage ────────────────────────────────────────────────────────

def _cx(screen, text, char_w=8):
    """Retourne x pour centrer `text`."""
    SW = screen.get_width()
    return SW // 2 - len(text) * char_w // 2


def draw_box(screen, x, y, w, h, border_color, alpha=170):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((0, 0, 0, alpha))
    screen.blit(surf, (x, y))
    pygame.draw.rect(screen, border_color, (x, y, w, h), 2, border_radius=8)


def draw_button(display, label, x, y, w, h, selected, disabled):
    screen = display.screen
    if disabled:
        bg_alpha = 60
        border   = C_BORDER_D
        txt_col  = C_GREY
    elif selected:
        bg_alpha = 200
        border   = C_BORDER_S
        txt_col  = C_GOLD
    else:
        bg_alpha = 130
        border   = C_BORDER_N
        txt_col  = C_WHITE

    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((20, 20, 20, bg_alpha))
    screen.blit(surf, (x, y))
    pygame.draw.rect(screen, border, (x, y, w, h), 2, border_radius=8)

    tx = x + w // 2 - len(label) * 8 // 2
    ty = y + h // 2 - 7
    display.render_ascii(label, txt_col, tx, ty)


# ── Logique objets / argent ────────────────────────────────────────────────────

def matches(item, template):
    return (item._name == template["name"] and item._hp == template["hp"]
            and item._sh == template["sh"] and item._st == template["st"])


def get_sell_price(item):
    """Prix de revente : celui du catalogue si l'objet y figure, sinon une
    estimation basée sur ses statistiques."""
    for t in SHOP_STOCK:
        if matches(item, t):
            return t["sell"]
    return max(1, (item._hp + item._sh + item._st) * 2)


def buy_item(player, template):
    """Achète un exemplaire de `template`. Retourne True si l'achat a eu lieu."""
    if player.money < template["buy"]:
        return False
    player.money -= template["buy"]
    for item in player.bag:
        if matches(item, template):
            item._qty += 1
            return True
    player.bag.append(Item(template["name"], template["hp"], template["sh"],
                            template["st"], 1))
    return True


def sell_item(player, item):
    """Vend un exemplaire de `item`. Retourne True si la vente a eu lieu."""
    if item._qty <= 0:
        return False
    item._qty -= 1
    player.money += get_sell_price(item)
    return True


# ── Écran principal du magasin ──────────────────────────────────────────────────

def shop(display, player):
    """
    Lance l'interface du magasin.
    Retourne quand le joueur choisit de sortir.

    player doit exposer :
        player.money (int)         – argent disponible
        player.bag   (list[Item])  – sac d'objets du joueur
    """

    # États possibles : "main" | "buy" | "sell"
    state = "main"
    sel   = 0

    move_delay     = 0.18
    last_move_time = 0.0
    space_last     = False

    COLS = 3   # colonnes de la grille d'objets

    while True:
        if not display.is_open():
            return

        display.clear()
        screen = display.screen
        SW, SH = screen.get_size()

        current_time = time.time()
        keys         = pygame.key.get_pressed()
        space_now    = keys[pygame.K_RETURN]

        # ── Panneau principal centré ─────────────────────────────────
        panel_w = int(SW * 0.66)
        panel_h = int(SH * 0.68)
        panel_x = SW // 2 - panel_w // 2
        panel_y = int(SH * 0.22)
        draw_box(screen, panel_x, panel_y, panel_w, panel_h, C_BORDER_N, alpha=150)

        # ── Ligne de séparation haut ─────────────────────────────────
        sep_y = panel_y + 90
        pygame.draw.line(screen, C_BORDER_N,
                         (panel_x + 16, sep_y), (panel_x + panel_w - 16, sep_y), 1)

        # ── Solde ──────────────────────────────────────────────────
        lbl_money = f"Argent disponible :  $ {player.money}"
        display.render_ascii(lbl_money, C_GOLD, _cx(screen, lbl_money), panel_y + 30)

        title = "─  MAGASIN  ─"
        display.render_ascii(title, C_WHITE, _cx(screen, title), panel_y + 4)

        # ── Ligne de séparation bas ──────────────────────────────────
        sep_y2 = panel_y + panel_h - 60
        pygame.draw.line(screen, C_BORDER_N,
                         (panel_x + 16, sep_y2), (panel_x + panel_w - 16, sep_y2), 1)

        # ── Hint navigation (toujours visible) ───────────────────────
        hint = "<- -> haut/bas naviguer    ENTREE valider    BACKSPACE retour"
        display.render_ascii(hint, C_GREY, _cx(screen, hint), panel_y + panel_h - 30)

        # ════════════════════════════════════════════════════════════
        #  État : menu principal (Acheter / Vendre / Sortir)
        # ════════════════════════════════════════════════════════════
        if state == "main":

            sub = "─  QUE SOUHAITEZ-VOUS FAIRE ?  ─"
            display.render_ascii(sub, C_WHITE, _cx(screen, sub), sep_y + 30)

            btn_labels = ["  ACHETER  ", "  VENDRE  ", "   SORTIR  "]
            btn_count  = len(btn_labels)
            btn_w      = int(panel_w * 0.26)
            btn_h      = 46
            btn_gap    = (panel_w - btn_count * btn_w) // (btn_count + 1)
            btn_y      = sep_y + 80

            for i, lbl in enumerate(btn_labels):
                bx = panel_x + btn_gap * (i + 1) + btn_w * i
                draw_button(display, lbl, bx, btn_y, btn_w, btn_h,
                            selected=i == sel, disabled=False)

            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    sel = (sel - 1) % btn_count
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    sel = (sel + 1) % btn_count
                    last_move_time = current_time
                elif space_now and not space_last:
                    if sel == 0:
                        state = "buy"
                        sel = 0
                    elif sel == 1:
                        state = "sell"
                        sel = 0
                    elif sel == 2:
                        return   # sortir du magasin

        # ════════════════════════════════════════════════════════════
        #  État : achat
        # ════════════════════════════════════════════════════════════
        elif state == "buy":

            sub = "─  CHOISISSEZ UN OBJET A ACHETER  ─"
            display.render_ascii(sub, C_GREEN, _cx(screen, sub), sep_y + 24)

            n = len(SHOP_STOCK)
            grid_top = sep_y + 64
            cell_w   = panel_w // COLS
            cell_h   = 60

            for i, t in enumerate(SHOP_STOCK):
                row, col = i // COLS, i % COLS
                bx = panel_x + col * cell_w + 8
                by = grid_top + row * cell_h
                bw = cell_w - 16
                bh = cell_h - 12

                disabled = player.money < t["buy"]
                label = f"{t['name']}  $ {t['buy']}"
                draw_button(display, label, bx, by, bw, bh,
                            selected=i == sel, disabled=disabled)

            rows = -(-n // COLS)  # ceil
            back_y = grid_top + rows * cell_h + 14
            back_w = int(panel_w * 0.36)
            back_x = SW // 2 - back_w // 2
            draw_button(display, "  RETOUR AU MENU  ", back_x, back_y, back_w, 38,
                         selected=sel == n, disabled=False)

            # Détails de l'objet survolé
            if sel < n:
                t = SHOP_STOCK[sel]
                detail = f"HP +{t['hp']}  SH +{t['sh']}  ST +{t['st']}   (revente : $ {t['sell']})"
                display.render_ascii(detail, C_GREY, _cx(screen, detail), back_y + 50)

            # Navigation
            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    sel = (sel - 1) % (n + 1)
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    sel = (sel + 1) % (n + 1)
                    last_move_time = current_time
                elif keys[pygame.K_UP]:
                    sel = sel - COLS if sel - COLS >= 0 else 0
                    last_move_time = current_time
                elif keys[pygame.K_DOWN]:
                    sel = sel + COLS if sel + COLS < n + 1 else n
                    last_move_time = current_time
                elif keys[pygame.K_BACKSPACE]:
                    state = "main"
                    sel   = 0

            if space_now and not space_last:
                if sel == n:
                    state = "main"
                    sel   = 0
                else:
                    t = SHOP_STOCK[sel]
                    buy_item(player, t)

        # ════════════════════════════════════════════════════════════
        #  État : vente
        # ════════════════════════════════════════════════════════════
        elif state == "sell":

            sub = "─  CHOISISSEZ UN OBJET A VENDRE  ─"
            display.render_ascii(sub, C_RED, _cx(screen, sub), sep_y + 24)

            usable_items = [item for item in player.bag if item._qty > 0]
            n = len(usable_items)
            sel = min(sel, n)   # clamp si le dernier exemplaire a été vendu

            if n == 0:
                empty = "Votre sac est vide."
                display.render_ascii(empty, C_GREY, _cx(screen, empty), sep_y + 90)
            else:
                grid_top = sep_y + 64
                cell_w   = panel_w // COLS
                cell_h   = 60

                for i, item in enumerate(usable_items):
                    row, col = i // COLS, i % COLS
                    bx = panel_x + col * cell_w + 8
                    by = grid_top + row * cell_h
                    bw = cell_w - 16
                    bh = cell_h - 12

                    label = f"{item._name} x{item._qty}  $ {get_sell_price(item)}"
                    draw_button(display, label, bx, by, bw, bh,
                                selected=i == sel, disabled=False)

                rows = -(-n // COLS)
                back_y = grid_top + rows * cell_h + 14

                if sel < n:
                    item = usable_items[sel]
                    detail = (f"HP +{item._hp}  SH +{item._sh}  ST +{item._st}"
                              f"   (en stock : {item._qty})")
                    display.render_ascii(detail, C_GREY, _cx(screen, detail), back_y + 50)
            # (calcul de back_y même si n == 0, pour le bouton retour)
            if n == 0:
                back_y = sep_y + 150

            back_w = int(panel_w * 0.36)
            back_x = SW // 2 - back_w // 2
            draw_button(display, "  RETOUR AU MENU  ", back_x, back_y, back_w, 38,
                         selected=sel == n, disabled=False)

            # Navigation
            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    sel = (sel - 1) % (n + 1)
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    sel = (sel + 1) % (n + 1)
                    last_move_time = current_time
                elif keys[pygame.K_UP]:
                    sel = sel - COLS if sel - COLS >= 0 else 0
                    last_move_time = current_time
                elif keys[pygame.K_DOWN]:
                    sel = sel + COLS if sel + COLS < n + 1 else n
                    last_move_time = current_time
                elif keys[pygame.K_BACKSPACE]:
                    state = "main"
                    sel   = 0

            if space_now and not space_last:
                if sel == n:
                    state = "main"
                    sel   = 0
                else:
                    sell_item(player, usable_items[sel])

        if keys[pygame.K_ESCAPE]:
            return

        space_last = space_now
        display.update()


# ── TEST ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    d = Display(900, 650, "Magasin")

    p = Player()
    p.money = 1800
    p.bag = [
    ]

    shop(d, p)
    print(f"Fin — Argent : ${p.money}")
    print("Sac :")
    for it in p.bag:
        print(" ", it)