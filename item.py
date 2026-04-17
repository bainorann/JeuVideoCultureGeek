class Item:
    def __init__(self, name, hp, sh, st, qty):
        self._name = name
        self._hp = hp
        self._sh = sh
        self._st = st
        self._qty = qty

    def __str__(self):
        return f"""{self._name} | hp : {self._hp} | sh : {self._sh} | st : {self._st} | qty : {self._qty}"""