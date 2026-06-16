import os
import time
import pygame
from display import Display

box = r"""
█████████████████████████████████████████████████████████████████████████████
█                                                                           █
█                                                                           █
█                                                                           █
█                                                                           █
█                                                                           █
█                                                                           █
█                                                                           █
█                                                                           █
█                                                                           █
█████████████████████████████████████████████████████████████████████████████
"""


def ascii_size(display, text):
    """Largeur/hauteur en pixels d'un bloc ascii (texte multi-lignes)."""
    lines = text.strip('\n').split('\n')
    w = max(len(line) for line in lines) * display._fontw
    h = len(lines) * display._fonth
    return w, h


def dialogue(display, text_file, portrait_file):
    with open(text_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    portrait_text = ""
    if portrait_file and os.path.exists(portrait_file):
        with open(portrait_file, "r", encoding="utf-8") as f:
            portrait_text = f.read()

    line_index = 0

    LINE_SPACING = display._fonth
    MAX_LINES = 8

    space_pressed_last_frame = True

    running = True

    while running:
        if not display.is_open():
            return

        display.clear()

        SW, SH = display.screen.get_size()

        current_time = time.time()
        keys = pygame.key.get_pressed()
        space_pressed_now = keys[pygame.K_RETURN]

        if keys[pygame.K_ESCAPE]:
            return


        # ── Boîte de dialogue : centrée horizontalement, en bas ──────────
        box_w, box_h = ascii_size(display, box)
        margin_bottom = int(SH * 0.03)
        box_x = SW // 2 - box_w // 2
        box_y = SH - box_h - margin_bottom

        display.render_ascii(box, (255, 255, 255), box_x, box_y)

        # ── Portrait du PNJ : centré horizontalement, au-dessus de la boîte ──
        if portrait_text:
            port_w, port_h = ascii_size(display, portrait_text)
            port_x = SW // 2 - port_w // 2
            margin_top = int(SH * 0.05)
            port_y = (box_y - port_h) // 2
            port_y = max(margin_top, port_y)

            display.render_ascii(portrait_text, (255, 255, 255), port_x, port_y)

        # ── Texte du dialogue, positionné relativement à la boîte ────────
        text_x = box_x + int(box_w * 0.04)
        text_y = box_y + int(box_h * 0.16)

        for i in range(MAX_LINES):
            if line_index + i < len(lines):
                line = lines[line_index + i].strip()
                display.render_ascii(
                    line,
                    (255, 255, 255),
                    text_x,
                    text_y + i * LINE_SPACING
                )

        if space_pressed_now and not space_pressed_last_frame:
            line_index += MAX_LINES

        space_pressed_last_frame = space_pressed_now

        if line_index >= len(lines):
            running = False

        display.update()

    return

master = r"""'
                ███████████               
          ██   █░░█     █░░█              
        ██  █  █░░░█   █░░░█ ███          
      ██     ████████████████   ██        
     █    ████::::::║║::::::█     ██      
   ██░█  ██#####::::║║:::####███    █     
 ██  █░█ █########::::::#######█  ██ ███  
█     █░██#########****########█ ██     █ 
█     █░░║║######********######║║░█      █
█ ██  █░░║║#██#************#██#║║░░█  ██ █
█ █░█ █░░░██@@███*********██@@███░░█ █░██ 
█ █░░██░██@@@@@@@██****███@@@@@@@████║║█  
 █║║░███@@@@@@@@@@@████@@@@@@@@@@@@██║║   
  ║║░░█@@@███████@@@@@@@@███████@@@█      
    ███@@@@@@@@@@@@@@@@@@@@@@@@@@@@████   
   █   █@@@@@@@@@@@@██@@@@@@@@@@@███   █  
  █    ███@@@@@@@███  ███@@@@@@██  █    █ 
 █     ██ ███████ │    │ ██████   █      █
 █   ██ █          \__/          █ ██    █
  ███    █          []          █    █   █
 █        █     <╥╥╥╥╥╥╥╥╥>    █      █ █ 
 █         █     ╘╧╧╧╧╧╧╧╛    █ █      █  
  █      ██ ██              ██   █    █   
   █  ███     ██          ██      █ ██    
    ██          ██████████         █      
      █       ██          ██       █      
       █     █              █    ██       
        ██  █                █  █         
          ██                  ██          
            ██████████████████       """

if __name__ == "__main__":
    d = Display()
    dialogue(d, "dette_casino.txt", "arlequin.txt")