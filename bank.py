import time

import pygame

from display import Display
from player import Player

# ── Palette ───────────────────────────────────────────────────────────────────

C_WHITE = (255, 255, 255)
C_GREY = (100, 100, 100)
C_DARK = (30, 30, 30)
C_GOLD = (255, 210, 50)
C_GREEN = (80, 200, 120)
C_RED = (220, 70, 70)
C_BLUE = (80, 130, 255)
C_BG_BOX = (0, 0, 0, 170)
C_BORDER_N = (160, 140, 80)  # bordure bouton normal
C_BORDER_S = (255, 210, 50)  # bordure bouton sélectionné
C_BORDER_D = (55, 55, 55)  # bordure bouton désactivé


# ── Montants prédéfinis ────────────────────────────────────────────────────────

AMOUNTS = [10, 50, 100, 500, "TOUT"]


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
        border = C_BORDER_D
        txt_col = C_GREY
    elif selected:
        bg_alpha = 200
        border = C_BORDER_S
        txt_col = C_GOLD
    else:
        bg_alpha = 130
        border = C_BORDER_N
        txt_col = C_WHITE

    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((20, 20, 20, bg_alpha))
    screen.blit(surf, (x, y))
    pygame.draw.rect(screen, border, (x, y, w, h), 2, border_radius=8)

    # Texte centré dans le bouton
    tx = x + w // 2 - len(label) * 8 // 2
    ty = y + h // 2 - 7
    display.render_ascii(label, txt_col, tx, ty)


# ── Écran principal de la banque ───────────────────────────────────────────────


def bank(display, player):
    """
    Lance l'interface de la banque.
    Retourne quand le joueur choisit de sortir.

    player doit exposer :
        player.money  (int) – argent sur soi
        player.bank   (int) – solde bancaire
    """

    # États possibles : "main" | "deposit" | "withdraw"
    state = "main"
    amount_index = 0  # index dans AMOUNTS
    error_msg = ""
    error_timer = 0.0

    # Index de sélection dans chaque écran
    # main    : 0=Déposer  1=Retirer  2=Sortir
    # deposit / withdraw : 0‥len(AMOUNTS)-1
    sel = 0

    move_delay = 0.18
    last_move_time = 0.0
    space_last = False

    def resolve_amount(idx, source):
        """Retourne le montant entier selon l'index et la source disponible."""
        a = AMOUNTS[idx]
        return source if a == "TOUT" else int(a)

    while True:
        if not display.is_open():
            return

        display.clear()
        screen = display.screen
        SW, SH = screen.get_size()

        current_time = time.time()
        keys         = pygame.key.get_pressed()
        space_now    = keys[pygame.K_RETURN]

        # ── Fond : art ASCII centré ──────────────────────────────────
        art_x = _cx(screen, "       ______________________________", 8)
        art_y = int(SH * 0.04)

        # ── Panneau principal centré ─────────────────────────────────
        panel_w = int(SW * 0.62)
        panel_h = int(SH * 0.68)
        panel_x = SW // 2 - panel_w // 2
        panel_y = int(SH * 0.22)
        draw_box(screen, panel_x, panel_y, panel_w, panel_h, C_BORDER_N, alpha=150)

        # ── Ligne de séparation haut ─────────────────────────────────
        sep_y = panel_y + 90
        pygame.draw.line(
            screen,
            C_BORDER_N,
            (panel_x + 16, sep_y),
            (panel_x + panel_w - 16, sep_y),
            1,
        )

        # ── Soldes ──────────────────────────────────────────────────
        lbl_bank = f"Solde compte  :  $ {player._bank}"
        lbl_money = f"Argent sur soi:  $ {player._money}"
        display.render_ascii(lbl_bank, C_GOLD, _cx(screen, lbl_bank), panel_y + 18)
        display.render_ascii(lbl_money, C_GREEN, _cx(screen, lbl_money), panel_y + 48)

        # ── Ligne de séparation bas ──────────────────────────────────
        sep_y2 = panel_y + panel_h - 70
        pygame.draw.line(
            screen,
            C_BORDER_N,
            (panel_x + 16, sep_y2),
            (panel_x + panel_w - 16, sep_y2),
            1,
        )

        # ── Hint navigation (toujours visible) ───────────────────────
        hint = "<- -> naviguer    ENTREE valider    BACKSPACE retour"
        display.render_ascii(hint, C_GREY, _cx(screen, hint), panel_y + panel_h - 50)

        # ════════════════════════════════════════════════════════════
        #  État : menu principal (Déposer / Retirer / Sortir)
        # ════════════════════════════════════════════════════════════
        if state == "main":
            title = "─  QUE SOUHAITEZ-VOUS FAIRE ?  ─"
            display.render_ascii(title, C_WHITE, _cx(screen, title), sep_y + 20)

            btn_labels = ["  DEPOSER  ", "  RETIRER  ", "   SORTIR  "]
            btn_disabled = [False, False, False]
            btn_count = len(btn_labels)
            btn_w = int(panel_w * 0.26)
            btn_h = 46
            btn_gap = (panel_w - btn_count * btn_w) // (btn_count + 1)
            btn_y = sep_y + 70

            for i, lbl in enumerate(btn_labels):
                bx = panel_x + btn_gap * (i + 1) + btn_w * i
                draw_button(
                    display,
                    lbl,
                    bx,
                    btn_y,
                    btn_w,
                    btn_h,
                    selected=i == sel,
                    disabled=btn_disabled[i],
                )

            # Navigation
            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    sel = (sel - 1) % btn_count
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    sel = (sel + 1) % btn_count
                    last_move_time = current_time
                elif space_now and not space_last:
                    if sel == 0:
                        state = "deposit"
                        amount_index = 0
                        sel = 0
                    elif sel == 1:
                        state = "withdraw"
                        amount_index = 0
                        sel = 0
                    elif sel == 2:
                        return  # sortir de la banque

        # ════════════════════════════════════════════════════════════
        #  État : dépôt
        # ════════════════════════════════════════════════════════════
        elif state == "deposit":
            title = "─  DEPOSER DE L'ARGENT  ─"
            display.render_ascii(title, C_GREEN, _cx(screen, title), sep_y + 20)

            sub = "Choisissez le montant a deposer :"
            display.render_ascii(sub, C_WHITE, _cx(screen, sub), sep_y + 48)

            _draw_amount_buttons(
                display, screen, panel_x, panel_w, sep_y, sel, source=player._money
            )

            # Le montant actuellement survolé est-il utilisable ?
            amount_valid = False
            if sel < len(AMOUNTS):
                amt = resolve_amount(sel, player._money)
                amount_valid = player._money > 0 and amt <= player._money

            # Bouton retour, toujours sélectionnable
            confirm_w = int(panel_w * 0.36)
            confirm_x = SW // 2 - confirm_w // 2
            confirm_y = sep_y2 - 54
            draw_button(
                display,
                "  RETOUR AU MENU  ",
                confirm_x,
                confirm_y,
                confirm_w,
                38,
                selected=sel == len(AMOUNTS),
                disabled=False,
            )

            # Navigation montants + bouton retour
            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    sel = (sel - 1) % (len(AMOUNTS) + 1)
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    sel = (sel + 1) % (len(AMOUNTS) + 1)
                    last_move_time = current_time
                elif keys[pygame.K_BACKSPACE]:
                    state = "main"
                    sel = 0

            if space_now and not space_last:
                if sel == len(AMOUNTS):
                    state = "main"
                    sel = 0
                elif amount_valid:
                    real_amt = resolve_amount(sel, player._money)
                    player._money -= real_amt
                    player._bank += real_amt

        # ════════════════════════════════════════════════════════════
        #  État : retrait
        # ════════════════════════════════════════════════════════════
        elif state == "withdraw":
            title = "─  RETIRER DE L'ARGENT  ─"
            display.render_ascii(title, C_RED, _cx(screen, title), sep_y + 20)

            sub = "Choisissez le montant a retirer :"
            display.render_ascii(sub, C_WHITE, _cx(screen, sub), sep_y + 48)

            _draw_amount_buttons(
                display, screen, panel_x, panel_w, sep_y, sel, source=player._bank
            )

            # Le montant actuellement survolé est-il utilisable ?
            amount_valid = False
            if sel < len(AMOUNTS):
                amt = resolve_amount(sel, player._bank)
                amount_valid = player._bank > 0 and amt <= player._bank

            # Bouton retour, toujours sélectionnable
            confirm_w = int(panel_w * 0.36)
            confirm_x = SW // 2 - confirm_w // 2
            confirm_y = sep_y2 - 54
            draw_button(
                display,
                "  RETOUR AU MENU  ",
                confirm_x,
                confirm_y,
                confirm_w,
                38,
                selected=sel == len(AMOUNTS),
                disabled=False,
            )

            if current_time - last_move_time > move_delay:
                if keys[pygame.K_LEFT]:
                    sel = (sel - 1) % (len(AMOUNTS) + 1)
                    last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    sel = (sel + 1) % (len(AMOUNTS) + 1)
                    last_move_time = current_time
                elif keys[pygame.K_BACKSPACE]:
                    state = "main"
                    sel = 0

            if space_now and not space_last:
                if sel == len(AMOUNTS):
                    state = "main"
                    sel = 0
                elif amount_valid:
                    real_amt = resolve_amount(sel, player._bank)
                    player._bank -= real_amt
                    player._money += real_amt

        if keys[pygame.K_ESCAPE]:
            return

        space_last = space_now
        display.update()


# ── Boutons de montant partagés dépôt/retrait ─────────────────────────────────


def _draw_amount_buttons(display, screen, panel_x, panel_w, sep_y, sel, source):
    """Affiche la rangée de boutons de montant, grisés si source insuffisante."""
    btn_count = len(AMOUNTS)
    btn_w = int(panel_w * 0.15)
    btn_h = 44
    btn_gap = (panel_w - btn_count * btn_w) // (btn_count + 1)
    btn_y = sep_y + 90

    for i, amt in enumerate(AMOUNTS):
        real = source if amt == "TOUT" else int(amt)
        disabled = real > source or source == 0
        label = f"$ {amt}" if amt != "TOUT" else "TOUT"
        bx = panel_x + btn_gap * (i + 1) + btn_w * i
        draw_button(
            display,
            label,
            bx,
            btn_y,
            btn_w,
            btn_h,
            selected=i == sel,
            disabled=disabled,
        )


# ── TEST ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    d = Display(900, 650, "Banque")

    p = Player()
    p._money = 320
    p._bank = 1500

    bank(d, p)
    print(f"Fin — Sur soi: ${p._money}  Banque: ${p._bank}")
