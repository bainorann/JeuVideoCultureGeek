class Player:
    def __init__(self, x=0, y=0):
        self._hp = 10
        self._sh = 10
        self._st = 10
        self._x = x 
        self._y = y
        #below are defined x and y coords within a room chunk (16x16)
        self._localx = 0
        self._localy = 0

    def move(self, dx, dy, floor):
        if self._localx>=14 or self._localx<=2 or self._localy>=7 or self._localy<=1:
            if check_wall(self, floor):
                self._x += dx
                self._y += dy
            #otherwise the character should not move
    
    def __str__(self):
        return f"hp : {self._hp} | sh : {self._sh} | st : {self._st}\nx : {self._x} | y : {self._y} | localx : {self._localx} | localy : {self._localy}"

        
