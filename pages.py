from dialogue import dialogue


class Page:
    def __init__(self, text_file, room_x, room_y, local_x, local_y, portrait_file=None):
        self._text_file = text_file
        self._portrait_file = portrait_file
        self._room_x = room_x
        self._room_y = room_y
        self._local_x = local_x
        self._local_y = local_y
        self._collected = False

    def render(self, display):
        if not self._collected:
            display.render_char(
                "?", (255, 255, 200), self._local_x, self._local_y,
                self._room_x, self._room_y,
            )

    def check(self, player):
        return (
            not self._collected
            and player.x() == self._room_x
            and player.y() == self._room_y
            and player.localx() == self._local_x
            and player.localy() == self._local_y
        )

    def trigger(self, display):
        dialogue(display, self._text_file, self._portrait_file)
        self._collected = True
