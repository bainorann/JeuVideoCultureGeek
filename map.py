from display import Display

const_char_offset = 11 #see test3 in main.py
const_room_offset = const_char_offset*15

class Room:
    def __init__(self, door_in, door_out, layout, size, id, colour):
        self._door_in = door_in
        self._door_out = door_out
        self._layout = layout
        self._size = size #always consider a room starts at the top right
        self._id = id
        self._colour = colour

    def __str__(self):
        return self._layout
    
    def size(self):
        return self._size
    
    def layout(self):
        return self._layout

    def id(self):
        return self._id

    def colour(self):
        return self._colour #a 3 long list containing rgb values for the room colour

class Floor:
    def __init__(self, size):
        self._mat = [[-1 for i in range(size)] for i in range(size)]
        self._size = size
        self._tab = [Room(0, 0, '', 0, -1, (0,0,0)) for i in range(size*size)] #a list containing the rooms (Room class), for which the index is the id of the room
    
    def __str__(self):
        string = ""
        for i in range(self._size):
            for j in range(self._size):
                string =  string + str(self._mat[i][j])
            string = string + "\n"
        return string
   
    def size(self):
        return self._size

    def mat(self):
        return self._mat
    
    def tab(self):
        return self._tab

    def add_room(self, x, y, room):
        s = room.size()
        self._tab[room.id()] = room
        for i in range(s):
            for j in range(s):
                self._mat[x+i][y+j] = room.id() #in this function we consider the room is placeable
                        
#the map will be defined with a matrix, where the number will correspond to a room ID

#the objective of this function is to print an entire floor
def show_floor(f, display):
    display.clear()
    for i in range(f.size()):
        for j in range(f.size()):
            curr_room = f.tab()[f.mat()[i][j]]
            if curr_room.id() != -1:
        #we know for a fact here (see readme) that rooms are separated in 16x8 tiles.
        #the only thing left to do is to print the entire matrix from topleft to bootom right
        #while adding a 16 char offset (16*10 or 8 pixels, not sure yet...)
                display.render_ascii(curr_room.layout(), tuple(curr_room.colour()), j*const_room_offset, i*const_room_offset)
            

