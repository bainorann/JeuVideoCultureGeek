class Room:
    def __init__(self, door, layout, size, id):
        self._door = door
        self._layout = layout
        self._size = size #always consider a room starts at the top right
        self._id = id

    def __str__(self):
        return self._layout
    
    def size(self):
        return self._size

    def id(self):
        return self._id

class Floor:
    def __init__(self, size):
        self._mat = [[0 for i in range(size)] for i in range(size)]
        self._size = size
    
    def __str__(self):
        string = ""
        for i in range(self._size):
            for j in range(self._size):
                string = string + str(self._mat[i][j])
            string = string + "\n"
        return string
    
    def add_room(self, x, y, room):
        s = room.size()
        for i in range(s):
            for j in range(s):
                self._mat[x+i][y+j] = room.id() #in this function we consider the room is placeable
                        
#the map will be defined with a matrix, where the number will correspond to a room ID


map1 = Floor(4)
print(map1)
room1 = Room("e",[], 2, 1)
map1.add_room(1,1,room1)
print(map1)
