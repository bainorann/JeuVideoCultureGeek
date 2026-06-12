from tests.layouts import room_open_1, room_open_2
from tests.helpers import make_display


def run():
    display = make_display("ASCII Game")
    offset_x = 250
    offset_y = 200
    while display.is_open():
        display.clear()
        display.render_ascii(room_open_1, (150, 150, 255), offset_x, offset_y)
        display.render_ascii(room_open_2, (150, 255, 150), 0, offset_y)
        display.update()
    display.close()
