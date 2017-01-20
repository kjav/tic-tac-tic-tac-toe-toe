

class Board:
    def __init__(self, cells):
        """
        Pass in a list of lists of Board objects in a rectangular grid, or
        an empty list for a single cell (layer 0).
        """
        self.grid = cells
        self.rows = len(self.grid)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(self.grid[0])
        self.layer = 0
        inner_grid = self.grid
        while len(inner_grid) > 0:
            self.layer += 1
            inner_grid = inner_grid[0][0].grid
        self.owner = None

    def __repr__(self):
        return "<Board at layer {}>".format(self.layer)

    def __str__(self):
        piece = {None: ' ', 'O': 'O', 'X': 'X'}[self.owner]
        if self.rows == self.cols == 0:
            return piece
        else:
            result = ""
            for i in range(len(self.grid)):
                result_row = []
                for j in range(len(self.grid[0])):
                    substring = "\n".join([ " " + line + " " for line in self.grid[i][j].__str__().split('\n')])
                    length = len(substring.split('\n')[0])
                    if (length > 3):
                        substring = " " * length + "\n" + substring + "\n" + " " * length
                    if i > 0:
                        substring = "-" * (len(substring.split('\n')[0])) + "\n" + substring
                    if j > 0:
                        new_substring = ""
                        split_substring = substring.split("\n")
                        for k in range(len(split_substring)):
                            new_substring += "|" + split_substring[k] + "\n"
                        substring = new_substring
                    result_row.append(substring)
                for k in range(len(result_row)):
                    result_row[k] = result_row[k].split('\n')
                for k in range(len(result_row[0])):
                    for r in range(len(result_row)):
                        result += result_row[r][k]
                    result += '\n'
            return result[:-1] )

    def __getitem__(self, pos):
        try:
            return self.grid[pos[0]][pos[1]]
        except IndexError:
            raise IndexError("Index " + str(pos) + " out of board range")

    def get_rows(self):
        return self.grid

    def get_cols(self):
        return [[row[i] for row in self.grid] for i in range(self.cols)]

    def get_diags(self):
        """
        Get a list of the cells along the diagonals, where the first includes
        the top left cell and the second includes the top right.
        """
        if self.rows != self.cols or not self.grid:
            return []
        return [
            [self.grid[i][i] for i in range(self.rows)],
            [self.grid[i][-1-i] for i in range(self.rows)]
            ]

    def perform_move(self, player, coords):
        """
        Arguments are:
        player - single-character represtation of a player e.g. 'O', 'X'
        coords - list of coordindate tuples from top layer to bottom
        Iterates through coords - returns False if selected cell has an owner,
        otherwise iterates a layer deeper. If coords is empty, the owner of
        the board is set to player.
        """
        if self.owner is not None:
            return False
        if not coords: # should also check rows==0?
            self.owner = player
            return True
        else:
            c = coords.pop(0)
            is_valid = self.grid[c[0]][c[1]].perform_move(player, coords)
            self.owner = self.check_winner() #Only needs to be called if inner
                                             #board becomes completed
            return is_valid

    def check_winner(self):
        """
        Return the owner of the board after checking for completion. A (square)
        board of size n is defined as being completed if there is a single
        player who owns a line of n cells, which can be vertical, horizontal,
        or diagonal through the centre cell.
        """
        if self.owner is not None:
            return self.owner
        for row in self.get_rows():
            if len([c for c in row if c.owner == row[0].owner != None]) == self.cols:
                return row[0].owner
        for col in self.get_cols():
            if len([c for c in col if c.owner == col[0].owner != None]) == self.rows:
                return col[0].owner
        for diag in self.get_diags():
            if len([c for c in diag if c.owner == diag[0].owner != None]) == self.rows:
                return diag[0].owner
        return None



def create_board(size=3, depth=1):
    """Returns a board which has dimensions size x size x depth."""
    if depth == 0:
        return Board([])
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(create_board(size, depth=depth-1))
        grid.append(row)
    return Board(grid)



if __name__ == '__main__':
    main_board = create_board(4, 1)
    main_board.perform_move('O', [(0, 1)])
    main_board.perform_move('X', [(2, 2)])
    main_board.perform_move('X', [(3, 0)])
    print(main_board)
    print(main_board[0, 1])
