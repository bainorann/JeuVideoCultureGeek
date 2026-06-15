from display import Display, print_mat

const_char_offset = 11  # see test3 in main.py
const_room_offset = const_char_offset * 15


class Room:
    def __init__(self, mat, layout, size, id, colour):
        self._layout = layout
        self._size = size  # always consider a room starts at the top right
        self._id = id
        self._colour = colour
        self._mat = mat

    def __str__(self):
        return self._layout

    def size(self):
        return self._size

    def layout(self):
        return self._layout

    def id(self):
        return self._id

    def colour(self):
        return self._colour  # a 3 long list containing rgb values for the room colour

    def mat(self):
        return self._mat


class Floor:
    def __init__(self):
        self._mat = [[-1 for i in range(6)] for i in range(10)]
        self._visited = [[False for _ in range(6)] for _ in range(10)]
        self._size = (10, 6)
        self._tab = [
            Room([], "", 1, -1, (0, 0, 0)) for i in range(60)
        ]  # a list containing the rooms (Room class), for which the index is the id of the room

    def __str__(self):
        string = ""
        cols, rows = self._size
        for i in range(rows):
            for j in range(cols):
                string = string + str(self._mat[j][i])
            string = string + "\n"
        return string

    def size(self):
        return self._size

    def mat(self):
        return self._mat

    def tab(self):
        return self._tab

    def visited(self):
        return self._visited

    def visit_room(self, x, y):
        self._visited[x][y] = True

    def add_room(self, x, y, room):
        s = room.size()
        self._tab[room.id()] = room
        for i in range(s):
            for j in range(s):
                self._mat[x + i][y + j] = (
                    room.id()
                )  # in this function we consider the room is placeable


# the map will be defined with a matrix, where the number will correspond to a room ID


# the objective of this function is to print an entire floor
def show_floor(f, display):
    display.clear()
    cols, rows = f.size()
    for i in range(rows):
        for j in range(cols):
            curr_room = f.tab()[f.mat()[j][i]]
            if curr_room.id() != -1:
                colour = tuple(curr_room.colour()) if f.visited()[j][i] else (0, 0, 0)
                display.render_ascii(
                    curr_room.layout(),
                    colour,
                    j * display._fontw * 14.66,
                    i * display._fonth * 8,
                )
