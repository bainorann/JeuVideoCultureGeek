import pygame
from random import randint

# ──────────────────────────────────────────────
#  Constantes visuelles
# ──────────────────────────────────────────────

COLOR_BG       = (  0,   0,   0)
COLOR_WHITE    = (255, 255, 255)
COLOR_YELLOW   = (255, 220,   0)
COLOR_GREEN    = (  0, 220,  80)
COLOR_RED      = (220,  40,  40)
COLOR_BLUE     = ( 80, 140, 255)
COLOR_GRAY     = (120, 120, 120)
COLOR_SELECTED = ( 60, 200,  60)
COLOR_DIMMED   = ( 60,  60,  60)

# Suits classiques cyclés sur 6 valeurs : 0♠ 1♥ 2♦ 3♣ 4♠ 5♥
SUITS = ["s", "h", "d", "c", "s", "h"]   # lettres ASCII, affichage ci-dessous
SUIT_SYMBOLS = {"s": "P", "h": "C", "d": "K", "c": "T"}  # fallback ASCII
# On essaie les vrais glyphes, on bascule sur ASCII si la police ne les supporte pas
SUIT_UNICODE = {"s": "\u2660", "h": "\u2665", "d": "\u2666", "c": "\u2663"}

RANKS = ["7", "10", "V", "D", "R", "A"]

# couleur rouge pour coeur/carreau
def suit_color(value):
    return COLOR_RED if SUITS[value] in ("h", "d") else COLOR_WHITE

# ──────────────────────────────────────────────
#  Logique Casino (inchangée)
# ──────────────────────────────────────────────

class Casino:
    def __init__(self, money):
        self.wallet = money
        self.bet    = 0

    def hand(self):
        return [randint(0, 5) for _ in range(5)]

    def change(self, l, lind):
        for i in lind:
            l[i] = randint(0, 5)
        return l
    
    def smart_change(self, l):
        r = self.sort(l)
        # Trouver la valeur la plus fréquente (à conserver en priorité)
        max_count = max(r)
        if max_count >= 2:
            # Garder toutes les cartes qui forment la meilleure répétition
            keep_val = max(i for i in range(6) if r[i] == max_count)
            to_change = [i for i, v in enumerate(l) if v != keep_val]
        else:
            # Carte haute : échanger les 3 cartes les plus basses
            sorted_indices = sorted(range(5), key=lambda i: l[i])
            to_change = sorted_indices[:3]
        return self.change(l, to_change)

    def sort(self, l):
        r = [0] * 6
        for n in l:
            r[n] += 1
        return r

    def score(self, r):
        score  = 0
        factor = 1
        f3 = p = 0
        for i in range(6):
            if r[i] == 5:
                score  += 1000 * (i + 1) + 15000
                factor  = 16
            if r[i] == 4:
                score  += 2000 * (i + 1)
                factor  = 8
            if r[i] == 3:
                score  += 100 * (i + 1)
                f3     += 1
            if r[i] == 2:
                score  += (i + 1)
                p      += 1
        if f3 == 1:
            score  += 1000 * f3 * p
            factor  = 4 + 2 * min(1, p)
        elif p > 0:
            score  += 50 * max(0, p - 1)
            factor  = 2 + max(0, p - 1)
        return score, factor

    def hand_label(self, r):
        counts = sorted([c for c in r if c > 0], reverse=True)
        if 5 in counts:                      return "QUINTE FLUSH ROYALE"
        if 4 in counts:                      return "CARRE"
        if 3 in counts and 2 in counts:      return "FULL HOUSE"
        if 3 in counts:                      return "BRELAN"
        if counts.count(2) == 2:             return "DOUBLE PAIRE"
        if 2 in counts:                      return "PAIRE"
        return "CARTE HAUTE"

# ──────────────────────────────────────────────
#  Helpers d'affichage
# ──────────────────────────────────────────────

def draw_text(screen, font, text, x, y, color=COLOR_WHITE):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
    return surf.get_rect(topleft=(x, y))

def draw_button(screen, font, label, rect, active=False, color=None):
    col_border = color if color else (COLOR_BLUE if active else COLOR_GRAY)
    col_bg     = (15, 35, 70) if active else (15, 15, 15)
    pygame.draw.rect(screen, col_bg,     rect, border_radius=8)
    pygame.draw.rect(screen, col_border, rect, 2, border_radius=8)
    txt = font.render(label, True, col_border)
    screen.blit(txt, (rect.x + rect.w // 2 - txt.get_width() // 2,
                      rect.y + rect.h // 2 - txt.get_height() // 2))

# ──────────────────────────────────────────────
#  Rendu d'une carte  (dimensions en % écran)
# ──────────────────────────────────────────────

def draw_card(screen, font_rank, font_suit, value, x, y, w, h,
              selected=False, hidden=False, cursor=False):
    # Fond
    pygame.draw.rect(screen, (28, 28, 28), (x, y, w, h), border_radius=10)

    # Bordure : curseur jaune > sélectionné vert > blanc
    if cursor:
        border_col, bw = COLOR_YELLOW, 3
    elif selected:
        border_col, bw = COLOR_SELECTED, 3
    else:
        border_col, bw = COLOR_WHITE, 2
    pygame.draw.rect(screen, border_col, (x, y, w, h), bw, border_radius=10)

    if hidden:
        for dy in range(14, h - 14, 14):
            pygame.draw.line(screen, COLOR_DIMMED,
                             (x + 8, y + dy), (x + w - 8, y + dy), 1)
        q = font_rank.render("?", True, COLOR_GRAY)
        screen.blit(q, (x + w // 2 - q.get_width() // 2,
                        y + h // 2 - q.get_height() // 2))
        return

    col   = suit_color(value)
    rank  = RANKS[value]
    suit  = SUIT_UNICODE[SUITS[value]]

    # Rang coin haut-gauche
    tr = font_rank.render(rank, True, col)
    screen.blit(tr, (x + 6, y + 4))

    # Rang coin bas-droite (retourné visuellement = même texte)
    br = font_rank.render(rank, True, col)
    screen.blit(br, (x + w - br.get_width() - 6, y + h - br.get_height() - 4))

    # Symbole centré (grand)
    sym = font_suit.render(suit, True, col)
    screen.blit(sym, (x + w // 2 - sym.get_width() // 2,
                      y + h // 2 - sym.get_height() // 2))

    # Étiquette "CHANGER" au-dessus si sélectionné
    if selected:
        tag = font_rank.render("CHANGER", True, COLOR_SELECTED)
        screen.blit(tag, (x + w // 2 - tag.get_width() // 2, y - tag.get_height() - 4))


def draw_hand(screen, font_rank, font_suit, hand, cx, y, cw, ch,
              spacing, selected_set=None, cursor_idx=None, hidden=False):
    """cx = x du centre de la main entière."""
    n     = len(hand)
    total = n * cw + (n - 1) * spacing
    x0    = cx - total // 2
    for i, val in enumerate(hand):
        x   = x0 + i * (cw + spacing)
        sel = selected_set is not None and i in selected_set
        cur = cursor_idx is not None and i == cursor_idx
        draw_card(screen, font_rank, font_suit, val, x, y, cw, ch,
                  selected=sel, hidden=hidden, cursor=cur)
    return x0  # retourné pour calcul des clics

# ──────────────────────────────────────────────
#  Sélecteur de mise
# ──────────────────────────────────────────────

def draw_bet_selector(screen, font, bet, wallet, cx, y, btn_h):
    """Boutons -10 -1 +1 +10 centrés en cx."""
    bw   = 80
    gap  = 12
    step = [(-10, "-10"), (-1, "-1"), (1, "+1"), (10, "+10")]
    total = len(step) * bw + (len(step) - 1) * gap
    x0   = cx - total // 2
    rects = []
    for i, (delta, lbl) in enumerate(step):
        r = pygame.Rect(x0 + i * (bw + gap), y, bw, btn_h)
        reachable = (delta > 0 and casino_can_add(bet, wallet, delta)) or \
                    (delta < 0 and bet + delta >= 0)
        col = COLOR_WHITE if reachable else COLOR_DIMMED
        draw_button(screen, font, lbl, r, color=col)
        rects.append((r, delta))
    return rects

def casino_can_add(bet, wallet, delta):
    return bet + delta <= wallet

# ──────────────────────────────────────────────
#  Fonction principale
# ──────────────────────────────────────────────

def casino_game(display, starting_money=20):
    """
    Retourne le solde final quand le joueur quitte.
    Ordre des états :
      deal  ->  bet  ->  change  ->  result  ->  (deal | quit)
    La mise se fait APRES avoir vu ses cartes.
    """
    screen = display.screen
    clock  = display.clock

    # ── dimensions adaptées à la résolution de l'écran ──────────────
    SW, SH = screen.get_size()

    # Tailles de polices relatives à la hauteur écran
    fs_big  = max(22, SH // 30)
    fs_mid  = max(18, SH // 38)
    fs_sm   = max(14, SH // 50)
    fs_suit = max(30, SH // 18)   # symbole de couleur

    font_big  = pygame.font.SysFont("monospace", fs_big,  bold=True)
    font_mid  = pygame.font.SysFont("monospace", fs_mid)
    font_sm   = pygame.font.SysFont("monospace", fs_sm)
    font_suit = pygame.font.SysFont("monospace", fs_suit, bold=True)

    # Dimensions des cartes
    CARD_W    = max(90,  SW // 11)
    CARD_H    = int(CARD_W * 1.45)
    CARD_GAP  = max(8, CARD_W // 10)

    # Zones verticales
    MARGIN_TOP   = SH // 14
    DEALER_Y     = MARGIN_TOP + fs_sm + 6
    SEP_Y        = DEALER_Y + CARD_H + fs_sm + 20
    PLAYER_Y     = SEP_Y + 20
    BOTTOM_Y     = PLAYER_Y + CARD_H + fs_sm + 20   # zone mise + boutons
    BTN_H        = max(38, SH // 18)
    BTN_W_SM     = max(100, SW // 9)
    BTN_W_LG     = max(160, SW // 6)

    CX = SW // 2   # centre horizontal

    casino        = Casino(starting_money)
    state         = "deal"
    pl_hand       = []
    dl_hand       = []
    selected      = set()
    card_cursor   = 0
    result_msg    = ""
    result_col    = COLOR_WHITE
    bet_rects     = []    # liste de (Rect, delta)
    result_done   = False

    # ── boutons fixes (repositionnés selon résolution) ───────────────
    def make_rects():
        nonlocal btn_confirm, btn_quit
        btn_confirm = pygame.Rect(CX - BTN_W_LG - 10, SH - BTN_H - 20, BTN_W_LG, BTN_H)
        btn_quit    = pygame.Rect(CX + 10,             SH - BTN_H - 20, BTN_W_SM, BTN_H)

    btn_confirm = btn_quit = None
    make_rects()

    # ── boucle principale ────────────────────────────────────────────
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return casino.wallet

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if btn_quit.collidepoint(mx, my):
                    return casino.wallet

                # ── DEAL : distribuer et passer à BET ──
                if state == "deal":
                    if btn_confirm.collidepoint(mx, my):
                        pl_hand = casino.hand()
                        dl_hand = casino.hand()
                        selected.clear()
                        card_cursor = 0
                        casino.bet  = 0
                        state = "bet"

                # ── BET : choisir la mise ──
                elif state == "bet":
                    for r, delta in bet_rects:
                        if r.collidepoint(mx, my):
                            new_bet = casino.bet + delta
                            casino.bet = max(0, min(casino.wallet, new_bet))
                    if btn_confirm.collidepoint(mx, my) and casino.bet > 0:
                        casino.wallet -= casino.bet
                        state = "change"

                # ── CHANGE : sélectionner les cartes ──
                elif state == "change":
                    # Clic sur une carte
                    n     = len(pl_hand)
                    total = n * CARD_W + (n - 1) * CARD_GAP
                    x0    = CX - total // 2
                    for i in range(n):
                        cx_card = x0 + i * (CARD_W + CARD_GAP)
                        r = pygame.Rect(cx_card, PLAYER_Y, CARD_W, CARD_H)
                        if r.collidepoint(mx, my):
                            selected.symmetric_difference_update({i})
                    if btn_confirm.collidepoint(mx, my):
                        pl_hand = casino.change(pl_hand, list(selected))
                        dl_hand = casino.smart_change(dl_hand)
                        result_done = False
                        state = "result"

                # ── RESULT : rejouer ──
                elif state == "result":
                    if btn_confirm.collidepoint(mx, my) and casino.wallet > 0:
                        result_msg  = ""
                        result_done = False
                        casino.bet  = 0
                        state = "deal"

            if event.type == pygame.KEYDOWN:
                if state == "change":
                    if event.key == pygame.K_LEFT:
                        card_cursor = (card_cursor - 1) % 5
                    elif event.key == pygame.K_RIGHT:
                        card_cursor = (card_cursor + 1) % 5
                    elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN):
                        selected.symmetric_difference_update({card_cursor})
                    elif event.key == pygame.K_RETURN:
                        pl_hand = casino.change(pl_hand, list(selected))
                        dl_hand = casino.smart_change(dl_hand)
                        result_done = False
                        state = "result"
                    elif event.key == pygame.K_ESCAPE:
                        casino.wallet += casino.bet
                        casino.bet = 0
                        state = "bet"

        # ── DESSIN ───────────────────────────────────────────────────
        screen.fill(COLOR_BG)

        # En-tête : portefeuille et mise
        draw_text(screen, font_mid,
                  f"Portefeuille : {casino.wallet}",
                  20, 16, COLOR_YELLOW)
        draw_text(screen, font_mid,
                  f"Mise : {casino.bet}",
                  20, 16 + fs_mid + 4, COLOR_WHITE)

        # Séparateur horizontal
        pygame.draw.line(screen, COLOR_DIMMED, (0, SEP_Y), (SW, SEP_Y), 1)

        # Labels zones
        draw_text(screen, font_sm, "CROUPIER",
                  20, DEALER_Y - fs_sm - 4, COLOR_GRAY)
        draw_text(screen, font_sm, "JOUEUR",
                  20, PLAYER_Y - fs_sm - 4, COLOR_GRAY)

        # ── Mains ────────────────────────────────────────────────────
        if state == "deal":
            # Pas encore de cartes : message d'invite
            msg = font_big.render("Cliquez sur DISTRIBUER pour commencer", True, COLOR_GRAY)
            screen.blit(msg, (CX - msg.get_width() // 2, SEP_Y // 2 - msg.get_height() // 2))

        elif state == "bet":
            # Montrer la main du joueur, croupier caché
            draw_hand(screen, font_mid, font_suit,
                      dl_hand, CX, DEALER_Y, CARD_W, CARD_H, CARD_GAP, hidden=True)
            draw_hand(screen, font_mid, font_suit,
                      pl_hand, CX, PLAYER_Y, CARD_W, CARD_H, CARD_GAP)

            # Sélecteur de mise centré
            MID_Y = BOTTOM_Y + (SH - BTN_H - 20 - BOTTOM_Y) // 2 - BTN_H
            draw_text(screen, font_mid,
                      f"Mise actuelle : {casino.bet}  /  Wallet : {casino.wallet}",
                      0, MID_Y - fs_mid - 10, COLOR_YELLOW)
            # centrage du texte
            tw = font_mid.size(f"Mise actuelle : {casino.bet}  /  Wallet : {casino.wallet}")[0]
            # redessiner centré
            screen.fill(COLOR_BG, (0, MID_Y - fs_mid - 14, SW, fs_mid + 6))
            draw_text(screen, font_mid,
                      f"Mise actuelle : {casino.bet}  /  Wallet : {casino.wallet}",
                      CX - tw // 2, MID_Y - fs_mid - 10, COLOR_YELLOW)
            bet_rects = draw_bet_selector(screen, font_mid,
                                          casino.bet, casino.wallet,
                                          CX, MID_Y, BTN_H)
            draw_button(screen, font_mid, "CONFIRMER LA MISE", btn_confirm,
                        active=casino.bet > 0,
                        color=COLOR_GREEN if casino.bet > 0 else COLOR_GRAY)

        elif state == "change":
            draw_hand(screen, font_mid, font_suit,
                      dl_hand, CX, DEALER_Y, CARD_W, CARD_H, CARD_GAP, hidden=True)
            draw_hand(screen, font_mid, font_suit,
                      pl_hand, CX, PLAYER_Y, CARD_W, CARD_H, CARD_GAP,
                      selected_set=selected, cursor_idx=card_cursor)

            hint = font_sm.render(
                "Clic / <- -> ESPACE pour selectionner  |  ENTREE pour valider  |  ECHAP pour re-miser",
                True, COLOR_GRAY)
            screen.blit(hint, (CX - hint.get_width() // 2, BOTTOM_Y))

            draw_button(screen, font_mid, "ECHANGER & VOIR", btn_confirm,
                        active=True, color=COLOR_GREEN)

        elif state == "result":
            draw_hand(screen, font_mid, font_suit,
                      dl_hand, CX, DEALER_Y, CARD_W, CARD_H, CARD_GAP)
            draw_hand(screen, font_mid, font_suit,
                      pl_hand, CX, PLAYER_Y, CARD_W, CARD_H, CARD_GAP)

            spl, fp = casino.score(casino.sort(pl_hand))
            sdl      = casino.score(casino.sort(dl_hand))[0]

            draw_text(screen, font_sm,
                      f"-> {casino.hand_label(casino.sort(dl_hand))}  ({sdl} pts)",
                      20, DEALER_Y + CARD_H + 4, COLOR_GRAY)
            draw_text(screen, font_sm,
                      f"-> {casino.hand_label(casino.sort(pl_hand))}  ({spl} pts)",
                      20, PLAYER_Y + CARD_H + 4, COLOR_GRAY)

            # Résolution (une seule fois par round)
            if not result_done:
                if spl > sdl:
                    gain           = casino.bet * fp
                    casino.wallet += gain
                    result_msg     = f"GAGNE ! +{gain}  (x{fp})"
                    result_col     = COLOR_GREEN
                elif spl < sdl:
                    result_msg = "PERDU - La mise est perdue."
                    result_col  = COLOR_RED
                else:
                    casino.wallet += casino.bet
                    result_msg     = "EGALITE - Mise remboursee."
                    result_col     = COLOR_YELLOW
                casino.bet  = 0
                result_done = True

            rmsg = font_big.render(result_msg, True, result_col)
            screen.blit(rmsg, (CX - rmsg.get_width() // 2,
                               SEP_Y // 2 - rmsg.get_height() // 2))

            if casino.wallet > 0:
                draw_button(screen, font_mid, "REJOUER", btn_confirm,
                            active=True, color=COLOR_BLUE)
            else:
                go = font_big.render("GAME OVER - Plus d'argent !", True, COLOR_RED)
                screen.blit(go, (CX - go.get_width() // 2,
                                 SEP_Y // 2 + rmsg.get_height() + 6))

        # Bouton Quitter toujours visible
        draw_button(screen, font_sm, "QUITTER", btn_quit, color=COLOR_GRAY)

        # En état "deal", le bouton confirm = DISTRIBUER
        if state == "deal":
            draw_button(screen, font_mid, "DISTRIBUER", btn_confirm,
                        active=True, color=COLOR_YELLOW)

        pygame.display.flip()
        clock.tick(60)


# ──────────────────────────────────────────────
#  Point d'entrée autonome
# ──────────────────────────────────────────────

if __name__ == "__main__":
    from display import Display
    d = Display(title="Casino")
    final = casino_game(d, starting_money=20)
    print(f"Solde final : {final}")
    d.close()