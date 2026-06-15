from display import print_mat
from map import Floor, Room


class Player:
    def __init__(self, x=0, y=0):
        self._hp = 10
        self._sh = 10
        self._st = 10
        self._debt = 1000000000
        self._money = 20
        # used to tell which room we're in
        self._x = x  # between 0 and 9 bc 10 rooms
        self._y = y  # between 0 and 5 bc 6 rooms
        # below are defined x and y coords within a room chunk (16x16)
        self._localx = 6
        self._localy = 4
        self._bank = 0
        self.bag = []

    def move(self, dx, dy, floor):
        # if self._localx>=14 or self._localx<=2 or self._localy>=7 or self._localy<=1:
        match check_wall(self, floor, dx, dy):
            case 0 | 1 | 2 | 3:
                # print("got to case 1")
                self._localx += dx
                self._localy += dy
                # self._x unchanged, we are still in the same room
            case 4:
                # print("got to case 2")
                self._localx = 0
                # self._localy unchanged, we only moved to the right
                self._x += 1
            case 5:
                # print("got to case 3")
                self._localx = 15
                self._x += -1
            case 6:
                # print("got to case 4")
                self._localy = 0
                self._y += 1
            case 7:
                # print("got to case 5")
                self._localy = 7
                self._y += -1
            case 8:
                ()
                # print("Floor change: DOWN")
            case 9:
                ()
                # print("Floor change: UP")
            case _:
                ()
                # print(f"wtf² : {self.localx()},{self.localy()} | {self.x()},{self.y()}")
        # otherwise the character should not move

    def __str__(self):
        return f"hp : {self._hp} | sh : {self._sh} | st : {self._st}\nx : {self._x} | y : {self._y} | localx : {self._localx} | localy : {self._localy}"

    def x(self):
        return self._x

    def y(self):
        return self._y

    def localx(self):
        return self._localx

    def localy(self):
        return self._localy

    def debt(self):
        return self._debt

    def min_debt(self, num):
        self._debt = self._debt - num

    def money(self):
        return self._money

    def min_money(self, num):
        self._money = self._money - num

    def set_position(self, room_x, room_y, local_x, local_y):
        self._x = room_x
        self._y = room_y
        self._localx = local_x
        self._localy = local_y


# précond : appelé avec UNIQUEMENT dx >=0 OU dy>=0
# devrait être ok, lors de l'appel par rapport à la touche pressée, appeler la fonction avec un seul argument >=0
def check_wall(player, floor, dx, dy):
    room_id = floor.mat()[player.x()][player.y()]
    curr_room = floor.tab()[room_id]

    # the player is within the interior of the room
    if 0 < player.localx() < 15 and 0 < player.localy() < 7:
        if curr_room.mat()[player.localx() + dx][player.localy() + dy] == 0:
            return 0

    else:  # the player is on a room border, just check door collision
        # necessarily west door, check up and down
        # otherwise out of bounds index...
        if (
            player.localx() == 0
            and (dy != 0 or dx >= 0)
            and (player.localy() != 0 or dy > 0)
            and (player.localy() != 7 or dy < 0)
        ):
            if curr_room.mat()[player.localx() + dx][player.localy() + dy] == 0:
                return 1

        # necessarily east door, check up and down
        if (
            player.localx() == 15
            and (dy != 0 or dx <= 0)
            and (player.localy() != 0 or dy > 0)
            and (player.localy() != 7 or dy < 0)
        ):
            if curr_room.mat()[player.localx() + dx][player.localy() + dy] == 0:
                return 2

        # necessarily north or south
        if (
            player.localy() == 0
            and (dx != 0 or dy >= 0)
            and (player.localx() != 0 or dx > 0)
            and (player.localx() != 15 or dx < 0)
        ) or (
            player.localy() == 7
            and (dx != 0 or dy <= 0)
            and (player.localx() != 0 or dx > 0)
            and (player.localx() != 15 or dx < 0)
        ):
            if curr_room.mat()[player.localx() + dx][player.localy() + dy] == 0:
                return 3

        # changing rooms
        else:
            if player.localx() == 15 and dx > 0:
                # check to see if we are at the edge of a floor
                if player.x() < 9:
                    next_room_id = floor.mat()[player.x() + 1][player.y()]
                    next_room = floor.tab()[next_room_id]
                    if next_room.mat()[0][player.localy()] == 0:
                        return 4
                else:
                    return 8  # change FLOOR signal, go DOWN

            elif player.localx() == 0 and dx < 0:
                if player.x() > 0:
                    next_room_id = floor.mat()[player.x() - 1][player.y()]
                    next_room = floor.tab()[next_room_id]
                    if next_room.mat()[15][player.localy()] == 0:
                        return 5
                else:
                    return 9  # change FLOOR signal, go UP

            elif player.localy() == 7 and dy > 0:
                next_room_id = floor.mat()[player.x()][player.y() + 1]
                next_room = floor.tab()[next_room_id]
                if next_room.mat()[player.localx()][0] == 0:
                    return 6

            elif player.localy() == 0 and dy < 0:
                next_room_id = floor.mat()[player.x()][player.y() - 1]
                next_room = floor.tab()[next_room_id]
                if next_room.mat()[player.localx()][7] == 0:
                    return 7
