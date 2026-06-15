from random import randint

import pygame

COLOR_BG = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 220, 0)
COLOR_GREEN = (0, 220, 80)
COLOR_RED = (220, 40, 40)
COLOR_BLUE = (80, 140, 255)
COLOR_GRAY = (120, 120, 120)
COLOR_SELECTED = (60, 200, 60)
COLOR_DIMMED = (60, 60, 60)

SUITS = ["s", "h", "d", "c", "s", "h"]
SUIT_UNICODE = {"s": "\u2660", "h": "\u2665", "d": "\u2666", "c": "\u2663"}
RANKS = ["7", "10", "V", "D", "R", "A"]


def suit_color(value):
    return COLOR_RED if SUITS[value] in ("h", "d") else COLOR_WHITE


# ──────────────────────────────────────────────
#  Logique Casino
# ──────────────────────────────────────────────


class Casino:
    def __init__(self, money):
        self.wallet = money
        self.bet = 0

    def hand(self):
        return [randint(0, 5) for _ in range(5)]

    def change(self, l, lind):
        for i in lind:
            l[i] = randint(0, 5)
        return l

    def smart_change(self, l):
        r = self.sort(l)
        max_count = max(r)
        if max_count >= 2:
            keep_val = max(i for i in range(6) if r[i] == max_count)
            to_change = [i for i, v in enumerate(l) if v != keep_val]
        else:
            sorted_indices = sorted(range(5), key=lambda i: l[i])
            to_change = sorted_indices[:3]
        return self.change(l, to_change)

    def sort(self, l):
        r = [0] * 6
        for n in l:
            r[n] += 1
        return r

    def score(self, r):
        score = 0
        factor = 1
        f3 = p = 0
        for i in range(6):
            if r[i] == 5:
                score += 1000 * (i + 1) + 15000
                factor = 16
            if r[i] == 4:
                score += 2000 * (i + 1)
                factor = 8
            if r[i] == 3:
                score += 100 * (i + 1)
                f3 += 1
            if r[i] == 2:
                score += i + 1
                p += 1
        if f3 == 1:
            score += 1000 * f3 * p
            factor = 4 + 2 * min(1, p)
        elif p > 0:
            score += 50 * max(0, p - 1)
            factor = 2 + max(0, p - 1)
        return score, factor

    def hand_label(self, r):
        counts = sorted([c for c in r if c > 0], reverse=True)
        if 5 in counts:
            return "QUINTE FLUSH ROYALE"
        if 4 in counts:
            return "CARRE"
        if 3 in counts and 2 in counts:
            return "FULL HOUSE"
        if 3 in counts:
            return "BRELAN"
        if counts.count(2) == 2:
            return "DOUBLE PAIRE"
        if 2 in counts:
            return "PAIRE"
        return "CARTE HAUTE"

    def hand_rank(self, r):
        """Indice de force de la main : 0 = carte haute ... 6 = quinte flush royale."""
        counts = sorted([c for c in r if c > 0], reverse=True)
        if 5 in counts:
            return 6
        if 4 in counts:
            return 5
        if 3 in counts and 2 in counts:
            return 4
        if 3 in counts:
            return 3
        if counts.count(2) == 2:
            return 2
        if 2 in counts:
            return 1
        return 0


# ──────────────────────────────────────────────
#  Helpers d'affichage
# ──────────────────────────────────────────────


def draw_text(screen, font, text, x, y, color=COLOR_WHITE):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
    return surf.get_rect(topleft=(x, y))


def draw_button(screen, font, label, rect, active=False, color=None, focused=False):
    col_border = color if color else (COLOR_BLUE if active else COLOR_GRAY)
    col_bg = (15, 35, 70) if active else (15, 15, 15)
    pygame.draw.rect(screen, col_bg, rect, border_radius=8)
    pygame.draw.rect(screen, col_border, rect, 2, border_radius=8)
    # Halo blanc autour du bouton si curseur dessus
    if focused:
        pygame.draw.rect(screen, COLOR_WHITE, rect.inflate(6, 6), 2, border_radius=11)
    txt = font.render(label, True, col_border)
    screen.blit(
        txt,
        (
            rect.x + rect.w // 2 - txt.get_width() // 2,
            rect.y + rect.h // 2 - txt.get_height() // 2,
        ),
    )


# ──────────────────────────────────────────────
#  Rendu des cartes
# ──────────────────────────────────────────────


def draw_card(
    screen,
    font_rank,
    font_suit,
    value,
    x,
    y,
    w,
    h,
    selected=False,
    hidden=False,
    cursor=False,
):
    pygame.draw.rect(screen, (28, 28, 28), (x, y, w, h), border_radius=10)
    if cursor:
        border_col, bw = COLOR_YELLOW, 3
    elif selected:
        border_col, bw = COLOR_SELECTED, 3
    else:
        border_col, bw = COLOR_WHITE, 2
    pygame.draw.rect(screen, border_col, (x, y, w, h), bw, border_radius=10)

    if hidden:
        for dy in range(14, h - 14, 14):
            pygame.draw.line(
                screen, COLOR_DIMMED, (x + 8, y + dy), (x + w - 8, y + dy), 1
            )
        q = font_rank.render("?", True, COLOR_GRAY)
        screen.blit(
            q, (x + w // 2 - q.get_width() // 2, y + h // 2 - q.get_height() // 2)
        )
        return

    col = suit_color(value)
    rank = RANKS[value]
    suit = SUIT_UNICODE[SUITS[value]]

    tr = font_rank.render(rank, True, col)
    screen.blit(tr, (x + 6, y + 4))
    br = font_rank.render(rank, True, col)
    screen.blit(br, (x + w - br.get_width() - 6, y + h - br.get_height() - 4))
    sym = font_suit.render(suit, True, col)
    screen.blit(
        sym, (x + w // 2 - sym.get_width() // 2, y + h // 2 - sym.get_height() // 2)
    )
    if selected:
        tag = font_rank.render("CHANGER", True, COLOR_SELECTED)
        screen.blit(tag, (x + w // 2 - tag.get_width() // 2, y - tag.get_height() - 4))


def draw_hand(
    screen,
    font_rank,
    font_suit,
    hand,
    cx,
    y,
    cw,
    ch,
    spacing,
    selected_set=None,
    cursor_idx=None,
    hidden=False,
):
    n = len(hand)
    total = n * cw + (n - 1) * spacing
    x0 = cx - total // 2
    for i, val in enumerate(hand):
        x = x0 + i * (cw + spacing)
        sel = selected_set is not None and i in selected_set
        cur = cursor_idx is not None and i == cursor_idx
        draw_card(
            screen,
            font_rank,
            font_suit,
            val,
            x,
            y,
            cw,
            ch,
            selected=sel,
            hidden=hidden,
            cursor=cur,
        )
    return x0


# ──────────────────────────────────────────────
#  Sélecteur de mise
# ──────────────────────────────────────────────


def draw_bet_selector(screen, font, bet, wallet, cx, y, btn_h, focused_idx=None):
    """
    Affiche les 4 boutons de mise.
    focused_idx (0-3) : bouton surligné par le curseur clavier.
    Retourne la liste des (Rect, delta).
    """
    bw = 80
    gap = 12
    step = [(-10, "-10"), (-1, "-1"), (1, "+1"), (10, "+10")]
    total = len(step) * bw + (len(step) - 1) * gap
    x0 = cx - total // 2
    rects = []
    for i, (delta, lbl) in enumerate(step):
        r = pygame.Rect(x0 + i * (bw + gap), y, bw, btn_h)
        reachable = (delta > 0 and bet + delta <= wallet) or (
            delta < 0 and bet + delta >= 0
        )
        col = COLOR_WHITE if reachable else COLOR_DIMMED
        draw_button(screen, font, lbl, r, color=col, focused=(focused_idx == i))
        rects.append((r, delta))
    return rects


# ──────────────────────────────────────────────
#  Fonction principale
# ──────────────────────────────────────────────


def casino_game(display, dette=1000000000, starting_money=20, mode="balanced"):
    """
    Retourne le solde final.
    États : deal -> bet -> change -> result -> (deal | quit)
    Entièrement jouable au clavier.

    mode :
      "balanced" : jeu normal, bouton QUITTER disponible.
      "unfair"   : le croupier triche pour gagner dès que la main du
                   joueur est plus faible qu'un carré. Pas de bouton
                   QUITTER ; la partie s'arrête automatiquement quand
                   le portefeuille du joueur atteint 0.
      "fair"     : le croupier triche pour NE PAS gagner quand le joueur
                   serait sur le point de perdre sa mise. Pas de bouton
                   QUITTER ; la partie s'arrête automatiquement quand le
                   portefeuille du joueur dépasse 10000.
    """
    screen = display.screen
    clock = display.clock

    SW, SH = screen.get_size()

    fs_big = max(22, SH // 30)
    fs_mid = max(18, SH // 38)
    fs_sm = max(14, SH // 50)
    fs_suit = max(30, SH // 18)

    # font_path = "assets/fonts/DejaVuSansMono.ttf"
    # Font = pygame.font.Font
    # font_big = Font(font_path, fs_big)
    font_big = pygame.font.SysFont("monospace", fs_big, bold=True)
    font_mid = pygame.font.SysFont("monospace", fs_mid)
    font_sm = pygame.font.SysFont("monospace", fs_sm)
    font_suit = pygame.font.SysFont("monospace", fs_suit, bold=True)

    CARD_W = max(90, SW // 11)
    CARD_H = int(CARD_W * 1.45)
    CARD_GAP = max(8, CARD_W // 10)

    MARGIN_TOP = SH // 14
    DEALER_Y = MARGIN_TOP + fs_sm + 6
    SEP_Y = DEALER_Y + CARD_H + fs_sm + 20
    PLAYER_Y = SEP_Y + 20
    BOTTOM_Y = PLAYER_Y + CARD_H + fs_sm + 20
    BTN_H = max(38, SH // 18)
    BTN_W_SM = max(100, SW // 9)
    BTN_W_LG = max(160, SW // 6)
    CX = SW // 2

    has_quit = mode == "balanced"

    casino = Casino(starting_money)
    state = "deal"
    pl_hand = []
    dl_hand = []
    selected = set()
    card_cursor = 0
    result_msg = ""
    result_col = COLOR_WHITE
    bet_rects = []
    result_done = False

    # ── Curseurs clavier par état ────────────────────────────────────
    # deal   : 0 = DISTRIBUER, (1 = QUITTER si has_quit)
    # bet    : 0-3 = boutons mise, 4 = CONFIRMER, (5 = QUITTER si has_quit)
    # change : 0-4 = cartes, 5 = ECHANGER&VOIR, (6 = QUITTER si has_quit)
    # result : 0 = REJOUER, (1 = QUITTER si has_quit)
    btn_cursor = 0

    btn_confirm = pygame.Rect(CX - BTN_W_LG - 10, SH - BTN_H - 20, BTN_W_LG, BTN_H)
    btn_quit = pygame.Rect(CX + 10, SH - BTN_H - 20, BTN_W_SM, BTN_H)

    def n_positions():
        if state == "deal":
            return 2 if has_quit else 1
        if state == "bet":
            return 6 if has_quit else 5
        if state == "change":
            return 7 if has_quit else 6
        if state == "result":
            return 2 if has_quit else 1
        return 1

    def nonlocal_set_state(s):
        nonlocal state, btn_cursor
        state = s
        btn_cursor = 0

    # ── Triche du croupier ────────────────────────────────────────
    def rig_hand(check, max_attempts=400):
        """Cherche une main satisfaisant `check`, sinon retourne la
        dernière main testée (cas extrême où c'est impossible)."""
        attempt = [randint(0, 5) for _ in range(5)]
        for _ in range(max_attempts):
            attempt = [randint(0, 5) for _ in range(5)]
            if check(attempt):
                return attempt
        return attempt

    def reveal_dealer(pl_final):
        """Calcule la main finale du croupier selon le mode choisi."""
        dl_final = casino.smart_change(dl_hand[:])
        spl = casino.score(casino.sort(pl_final))[0]

        if mode == "balanced":
            no = randint(1, 3)
            if max(casino.sort(pl_final)) < 4 and no == 3:
                dl_final = rig_hand(lambda h: casino.score(casino.sort(h))[0] > spl)

        if mode == "unfair":
            # Le croupier triche dès que le joueur n'a pas au moins un carré
            if max(casino.sort(pl_final)) < 4:
                dl_final = rig_hand(lambda h: casino.score(casino.sort(h))[0] > spl)

        elif mode == "fair":
            sdl = casino.score(casino.sort(dl_final))[0]
            pl_rank = casino.hand_rank(casino.sort(pl_final))
            # Une défaite ferait-elle tomber le solde à 0 ?
            # (la mise a déjà été déduite du portefeuille)
            ruin = casino.wallet == 0

            if pl_rank >= 2:
                # Double paire ou mieux : victoire garantie
                if sdl >= spl:
                    dl_final = rig_hand(lambda h: casino.score(casino.sort(h))[0] < spl)
            elif ruin:
                # Manche fatidique : le joueur ne peut pas perdre
                # (victoire ou égalité acceptées)
                if sdl > spl:
                    dl_final = rig_hand(
                        lambda h: casino.score(casino.sort(h))[0] <= spl
                    )
            # Sinon : le croupier joue normalement, le joueur peut perdre

        return dl_final

    def resolve_change():
        """Transition CHANGE -> RESULT (clic ou Entrée)."""
        nonlocal pl_hand, dl_hand, result_done
        pl_final = casino.change(pl_hand, list(selected))
        pl_hand[:] = pl_final
        dl_hand[:] = reveal_dealer(pl_final)
        result_done = False
        nonlocal_set_state("result")

    # ── Confirmation du bouton actuellement focalisé ─────────────────
    def confirm_focused():
        nonlocal state, result_msg, result_done, card_cursor

        if state == "deal":
            if btn_cursor == 0:  # DISTRIBUER
                pl_hand[:] = casino.hand()
                dl_hand[:] = casino.hand()
                selected.clear()
                card_cursor = 0
                casino.bet = 0
                nonlocal_set_state("bet")
            elif has_quit and btn_cursor == 1:  # QUITTER
                return "quit"

        elif state == "bet":
            if btn_cursor <= 3:  # boutons mise
                _, delta = (
                    bet_rects[btn_cursor]
                    if bet_rects
                    else (None, [-10, -1, 1, 10][btn_cursor])
                )
                new_bet = casino.bet + delta
                casino.bet = max(0, min(casino.wallet, new_bet))
            elif btn_cursor == 4:  # CONFIRMER
                if casino.bet > 0:
                    casino.wallet -= casino.bet
                    nonlocal_set_state("change")
            elif has_quit and btn_cursor == 5:  # QUITTER
                return "quit"

        elif state == "change":
            if btn_cursor <= 4:  # sélection carte
                selected.symmetric_difference_update({btn_cursor})
            elif btn_cursor == 5:  # ECHANGER & VOIR
                resolve_change()
            elif has_quit and btn_cursor == 6:  # QUITTER
                return "quit"

        elif state == "result":
            if btn_cursor == 0 and casino.wallet > 0:  # REJOUER
                result_msg = ""
                result_done = False
                casino.bet = 0
                nonlocal_set_state("deal")
            elif has_quit and btn_cursor == 1:  # QUITTER
                return "quit"

        return None

    # ── Boucle principale ────────────────────────────────────────────
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return casino.wallet

            # ── Souris ──────────────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if has_quit and btn_quit.collidepoint(mx, my):
                    return casino.wallet

                if state == "deal":
                    if btn_confirm.collidepoint(mx, my):
                        pl_hand = casino.hand()
                        dl_hand = casino.hand()
                        selected.clear()
                        card_cursor = 0
                        casino.bet = 0
                        nonlocal_set_state("bet")

                elif state == "bet":
                    for r, delta in bet_rects:
                        if r.collidepoint(mx, my):
                            casino.bet = max(0, min(casino.wallet, casino.bet + delta))
                    if btn_confirm.collidepoint(mx, my) and casino.bet > 0:
                        casino.wallet -= casino.bet
                        nonlocal_set_state("change")

                elif state == "change":
                    n = len(pl_hand)
                    total = n * CARD_W + (n - 1) * CARD_GAP
                    x0 = CX - total // 2
                    for i in range(n):
                        r = pygame.Rect(
                            x0 + i * (CARD_W + CARD_GAP), PLAYER_Y, CARD_W, CARD_H
                        )
                        if r.collidepoint(mx, my):
                            selected.symmetric_difference_update({i})
                    if btn_confirm.collidepoint(mx, my):
                        resolve_change()

                elif state == "result":
                    if btn_confirm.collidepoint(mx, my) and casino.wallet > 0:
                        result_msg = ""
                        result_done = False
                        casino.bet = 0
                        nonlocal_set_state("deal")

            # ── Clavier ─────────────────────────────────────────────
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_UP):
                    btn_cursor = (btn_cursor - 1) % n_positions()
                    if state == "change" and btn_cursor <= 4:
                        card_cursor = btn_cursor

                elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                    btn_cursor = (btn_cursor + 1) % n_positions()
                    if state == "change" and btn_cursor <= 4:
                        card_cursor = btn_cursor

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    result = confirm_focused()
                    if result == "quit":
                        return casino.wallet

                elif event.key == pygame.K_ESCAPE:
                    # Retour arrière contextuel
                    if state == "change":
                        casino.wallet += casino.bet
                        casino.bet = 0
                        nonlocal_set_state("bet")
                    elif state == "bet":
                        casino.bet = 0
                        nonlocal_set_state("deal")

                elif event.key == pygame.K_q:
                    return casino.wallet

        # ── DESSIN ───────────────────────────────────────────────────
        screen.fill(COLOR_BG)

        draw_text(
            screen, font_mid, f"Portefeuille : {casino.wallet}", 20, 16, COLOR_YELLOW
        )
        draw_text(
            screen, font_mid, f"Mise : {casino.bet}", 20, 16 + fs_mid + 4, COLOR_WHITE
        )
        if mode == "fair":
            msg = font_big.render(
                f"Objectif : {max(100 * starting_money, 10000)}", True, COLOR_GRAY
            )
            screen.blit(msg, (CX - msg.get_width() // 2, 16))
        if mode == "balanced":
            msg = font_big.render(f"Dette : {dette}", True, COLOR_GRAY)
            screen.blit(msg, (CX - msg.get_width() // 2, 16))

        pygame.draw.line(screen, COLOR_DIMMED, (0, SEP_Y), (SW, SEP_Y), 1)
        draw_text(screen, font_sm, "CROUPIER", 20, DEALER_Y - fs_sm - 4, COLOR_GRAY)
        draw_text(screen, font_sm, "JOUEUR", 20, PLAYER_Y - fs_sm - 4, COLOR_GRAY)

        # ── États ───────────────────────────────────────────────────
        if state == "deal":
            msg = font_big.render(
                "Pressez DISTRIBUER pour commencer.", True, COLOR_GRAY
            )
            screen.blit(
                msg, (CX - msg.get_width() // 2, SEP_Y // 2 - msg.get_height() // 2)
            )
            draw_button(
                screen,
                font_mid,
                "DISTRIBUER",
                btn_confirm,
                active=True,
                color=COLOR_YELLOW,
                focused=(btn_cursor == 0),
            )
            if has_quit:
                draw_button(
                    screen,
                    font_sm,
                    "QUITTER",
                    btn_quit,
                    color=COLOR_GRAY,
                    focused=(btn_cursor == 1),
                )

        elif state == "bet":
            draw_hand(
                screen,
                font_mid,
                font_suit,
                dl_hand,
                CX,
                DEALER_Y,
                CARD_W,
                CARD_H,
                CARD_GAP,
                hidden=True,
            )
            draw_hand(
                screen,
                font_mid,
                font_suit,
                pl_hand,
                CX,
                PLAYER_Y,
                CARD_W,
                CARD_H,
                CARD_GAP,
            )

            MID_Y = BOTTOM_Y + (SH - BTN_H - 20 - BOTTOM_Y) // 2 - BTN_H
            tw = font_mid.size(
                f"Mise actuelle : {casino.bet}  /  Portefeuille : {casino.wallet}"
            )[0]
            draw_text(
                screen,
                font_mid,
                f"Mise actuelle : {casino.bet}  /  Portefeuille : {casino.wallet}",
                CX - tw // 2,
                MID_Y - fs_mid - 10,
                COLOR_YELLOW,
            )

            focused_bet = btn_cursor if btn_cursor <= 3 else None
            bet_rects = draw_bet_selector(
                screen,
                font_mid,
                casino.bet,
                casino.wallet,
                CX,
                MID_Y,
                BTN_H,
                focused_idx=focused_bet,
            )
            draw_button(
                screen,
                font_mid,
                "CONFIRMER LA MISE",
                btn_confirm,
                active=casino.bet > 0,
                color=COLOR_GREEN if casino.bet > 0 else COLOR_GRAY,
                focused=(btn_cursor == 4),
            )
            if has_quit:
                draw_button(
                    screen,
                    font_sm,
                    "QUITTER",
                    btn_quit,
                    color=COLOR_GRAY,
                    focused=(btn_cursor == 5),
                )

        elif state == "change":
            draw_hand(
                screen,
                font_mid,
                font_suit,
                dl_hand,
                CX,
                DEALER_Y,
                CARD_W,
                CARD_H,
                CARD_GAP,
                hidden=True,
            )
            active_card_cursor = card_cursor if btn_cursor <= 4 else None
            draw_hand(
                screen,
                font_mid,
                font_suit,
                pl_hand,
                CX,
                PLAYER_Y,
                CARD_W,
                CARD_H,
                CARD_GAP,
                selected_set=selected,
                cursor_idx=active_card_cursor,
            )

            hint = font_sm.render(
                "<- -> pour naviguer  |  ESPACE pour selectionner  |  ECHAP pour re-miser",
                True,
                COLOR_GRAY,
            )
            screen.blit(hint, (CX - hint.get_width() // 2, BOTTOM_Y))

            draw_button(
                screen,
                font_mid,
                "ECHANGER & VOIR",
                btn_confirm,
                active=True,
                color=COLOR_GREEN,
                focused=(btn_cursor == 5),
            )
            if has_quit:
                draw_button(
                    screen,
                    font_sm,
                    "QUITTER",
                    btn_quit,
                    color=COLOR_GRAY,
                    focused=(btn_cursor == 6),
                )

        elif state == "result":
            draw_hand(
                screen,
                font_mid,
                font_suit,
                dl_hand,
                CX,
                DEALER_Y,
                CARD_W,
                CARD_H,
                CARD_GAP,
            )
            draw_hand(
                screen,
                font_mid,
                font_suit,
                pl_hand,
                CX,
                PLAYER_Y,
                CARD_W,
                CARD_H,
                CARD_GAP,
            )

            spl, fp = casino.score(casino.sort(pl_hand))
            sdl = casino.score(casino.sort(dl_hand))[0]

            draw_text(
                screen,
                font_sm,
                f"-> {casino.hand_label(casino.sort(dl_hand))}",
                20,
                DEALER_Y + CARD_H + 4,
                COLOR_GRAY,
            )
            draw_text(
                screen,
                font_sm,
                f"-> {casino.hand_label(casino.sort(pl_hand))}",
                20,
                PLAYER_Y + CARD_H + 4,
                COLOR_GRAY,
            )

            if not result_done:
                if spl > sdl:
                    gain = casino.bet * fp
                    casino.wallet += gain
                    result_msg = f"GAGNE ! +{gain}  (x{fp})"
                    result_col = COLOR_GREEN
                elif spl < sdl:
                    result_msg = "PERDU - La mise est perdue."
                    result_col = COLOR_RED
                else:
                    casino.wallet += casino.bet
                    result_msg = "EGALITE - Mise remboursee."
                    result_col = COLOR_YELLOW
                casino.bet = 0
                result_done = True

            rmsg = font_big.render(result_msg, True, result_col)
            screen.blit(
                rmsg, (CX - rmsg.get_width() // 2, SEP_Y // 2 - rmsg.get_height() // 2)
            )

            # Condition de fin spécifique au mode
            game_over_unfair = mode == "unfair" and casino.wallet <= 0
            objective_fair = mode == "fair" and casino.wallet > max(
                50 * starting_money, 10000
            )

            if objective_fair:
                go = font_big.render("OBJECTIF ATTEINT - BRAVO !", True, COLOR_GREEN)
                screen.blit(
                    go, (CX - go.get_width() // 2, SEP_Y // 2 + rmsg.get_height() + 6)
                )
            elif casino.wallet > 0:
                draw_button(
                    screen,
                    font_mid,
                    "REJOUER",
                    btn_confirm,
                    active=True,
                    color=COLOR_BLUE,
                    focused=(btn_cursor == 0),
                )
            else:
                go = font_big.render("GAME OVER - Plus d'argent !", True, COLOR_RED)
                screen.blit(
                    go, (CX - go.get_width() // 2, SEP_Y // 2 + rmsg.get_height() + 6)
                )

            if has_quit:
                draw_button(
                    screen,
                    font_sm,
                    "QUITTER",
                    btn_quit,
                    color=COLOR_GRAY,
                    focused=(btn_cursor == 1),
                )

        pygame.display.flip()
        clock.tick(60)

        # ── Fin automatique de partie (modes "unfair" / "fair") ──────
        if state == "result" and result_done:
            if mode == "unfair" and casino.wallet <= 0:
                pygame.time.delay(1500)
                return casino.wallet
            if mode == "fair" and casino.wallet > max(50 * starting_money, 10000):
                pygame.time.delay(1500)
                return casino.wallet


# ──────────────────────────────────────────────
#  Point d'entrée autonome
# ──────────────────────────────────────────────

if __name__ == "__main__":
    from display import Display

    d = Display(title="Casino")
    final = casino_game(d, starting_money=20, mode="balanced")
    print(f"Solde final : {final}")
    d.close()
