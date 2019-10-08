import os
from grid_element import Wall, EmptySquare, Door, Hole, Crate, Character


# Déplacer cette fonction dans utils fait tout planter
def clear():
    """To clear the screen between two moves"""
    # windows
    if os.name == 'nt':
        _ = os.system('cls')

    # unix based systems
    else:
        _ = os.system('clear')


class Grid:
    """This class contains all the elements of the game."""

    def __init__(self, level: str):
        """Constructor of Grid

        It contains a table in which all the elements of the current level are
        contained. It has methods to show the grid, to move the elements and
        to know if the game is won.

        Inputs:
            --level: path to a textfile containig the level"""

        # Opening the file containing the level
        try:
            level_file = open(level, 'r')
        except Exception:
            print("Can't read the level")
        lines = level_file.readlines()
        lines = [line.rstrip() for line in lines]

        # grid dimensions
        self.n_lig = len(lines)
        self.n_col = len(lines[0])

        # win is equal to -1 if the game is lost, 1 if it's won, 0 else
        self._win = 0

        # Initialisation of table table, which contains all grid elements
        self.table = [[0]*self.n_col for _ in range(self.n_lig)]

        check_door = 0
        check_char = 0

        for i in range(self.n_lig):
            for j in range(self.n_col):
                if lines[i][j] == '#':
                    self.table[i][j] = Wall(i, j)
                if lines[i][j] == ' ':
                    self.table[i][j] = EmptySquare(i, j)
                if lines[i][j] == '@':
                    self.table[i][j] = Door(i, j)
                    check_door += 1
                if lines[i][j] == 'o':
                    self.table[i][j] = Hole(i, j)
                if lines[i][j] == '*':
                    self.table[i][j] = Crate(i, j)
                if lines[i][j] == '1':
                    self.table[i][j] = Character(i, j)
                    self.char_h = i
                    self.char_v = j
                    check_char += 1

        if check_char > 1 or check_door > 1:
            raise Exception("Must be only one door and/or only one character")

    @property
    def win(self):
        """To get the value of win in the main loop"""
        return self._win

    def __getitem__(self, key: int):
        """Return the grid_element table[i][j]"""
        return self.table[key[0]][key[1]]

    def __setitem__(self, key: int, case):
        """Set the grid_element table[i][j]"""
        self.table[key[0]][key[1]] = case

    def move(self, direction_h: int, direction_v: int):
        """Function that manage the movement:
            Input: an order typed with the keyboard (string)
            Output: nothing"""

        # player = Character object in the grid
        player = self[self.char_h, self.char_v]
        # target = grid_element towards which the player is heading
        target = self[self.char_h+direction_h, self.char_v+direction_v]

        # door leads to victory
        if isinstance(target, Door):
            self._win = 1

        elif not(isinstance(target, Wall)) and not(isinstance(target, Door)):
            # if the player moves a crate, the element behind must be checked
            beyond_target = self[self.char_h+2*direction_h,
                                 self.char_v+2*direction_v]
            if isinstance(target, Hole):
                self._win = -1

            elif isinstance(target, EmptySquare):
                player.move(direction_h, direction_v)
                target.move(-direction_h, -direction_v)
                self[self.char_h, self.char_v] = target
                self[self.char_h+direction_h,
                     self.char_v+direction_v] = player
                self.char_h += direction_h
                self.char_v += direction_v

            elif (isinstance(target, Crate) and
                    not(isinstance(beyond_target, Wall)) and
                    not(isinstance(beyond_target, Crate))):
                beyond_target = self[self.char_h+2*direction_h,
                                     self.char_v+2*direction_v]
                player.move(direction_h, direction_v)
                self[self.char_h+direction_h,
                     self.char_v+direction_v] = player
                self[self.char_h,
                     self.char_v] = EmptySquare(self.char_h, self.char_v)

                if isinstance(beyond_target, EmptySquare):
                    target.move(direction_h, direction_v)
                    self[self.char_h+2*direction_h,
                         self.char_v+2*direction_v] = target
                elif isinstance(beyond_target, Hole):
                    self[self.char_h+2*direction_h,
                         self.char_v+2*direction_v] = EmptySquare(self.char_h+2*direction_h,
                                                                  self.char_v+2*direction_v)

                self.char_h += direction_h
                self.char_v += direction_v

    def show(self):
        """function that show the grid"""
        clear()
        for i in range(self.n_lig):
            line = ""
            for j in range(self.n_col):
                line += str(self.table[i][j])
            print(line)