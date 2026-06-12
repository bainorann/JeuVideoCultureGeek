from player import Player


class Enemy(Player):
    def __init__(self, x=0, y=0, localx=4, localy=4):
        super().__init__(x, y)
        self._localx = localx
        self._localy = localy


def spawn_enemy(x, y, localx, localy):
    return Enemy(x, y, localx, localy)
