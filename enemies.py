import random as rand

from player import Player


class Enemy(Player):
    def __init__(self, x=0, y=0, localx=4, localy=4):
        super().__init__(x, y)
        self._localx = localx
        self._localy = localy

    def move_to_player(self, player, floor):
        randx = rand.randint(-1, 1)
        randy = rand.randint(-1, 1)
        if (
            self.x() == player.x() and self.y() == player.y()
        ):  # the player is in the same room
            goal_x = player.localx() + randx
            goal_y = player.localy() + randy
            delta_x = goal_x - self.localx()
            delta_y = goal_y - self.localy()
            if abs(delta_x) > abs(delta_y) and delta_x != 0:  # should move towards x
                self.move(delta_x // abs(delta_x), 0, floor)
            elif delta_y != 0:
                self.move(0, delta_y // abs(delta_y), floor)


def spawn_enemy(x, y, localx, localy):
    return Enemy(x, y, localx, localy)
