from json import loads as decode_json
from json.decoder import JSONDecodeError

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
            for i in range(self.rows):
                result_row = []
                for j in range(self.cols):
                    substr = str(self[i, j])
                    lines_of_substr = substr.split('\n')
                    str_length = len(lines_of_substr[0])
                    if self[i, j].check_winner() is None:
                        substr = "\n".join(
                            [" {} ".format(ln) for ln in lines_of_substr])
                    else:
                        winner = self[i, j].check_winner()
                        substr = "\n".join(
                            [" {} ".format(" " * str_length) for _ in
                                lines_of_substr])
                        substr_length = len(substr)
                        substr = substr[0:int(substr_length/2)] + winner + substr[int(substr_length/2) + 1:substr_length]
                    lines_of_substr = substr.split('\n')
                    str_length = len(lines_of_substr[0])
                    if str_length > 3: #Exclude single cell
                        blank_row = " " * str_length
                        substr = "{0}\n{1}\n{0}".format(blank_row, substr)
                    if i > 0: #Exclude first row
                        substr = '-' * str_length + '\n' + substr
                    if j > 0: #Exclude first column
                        new_substr = ""
                        substr_lines = substr.split("\n")
                        for k in range(len(substr_lines)):
                            new_substr += "|{}\n".format(substr_lines[k])
                        substr = new_substr
                    result_row.append(substr)
                for k in range(len(result_row)):
                    result_row[k] = result_row[k].split('\n')
                for k in range(len(result_row[0])):
                    for r in range(len(result_row)):
                        result += result_row[r][k]
                    result += '\n'
            return result[:-1]

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
        coords = coords.copy()
        if self.owner is not None:
            return False
        if not coords: # should also check rows==0?
            self.owner = player
            return True
        else:
            c = coords.pop(0)
            is_valid = self.grid[c[1]][c[0]].perform_move(player, coords)
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

def parse_move(user_input):
    try:
        move = tuple(decode_json(user_input))
        if len(move) == 2 and type(move[0]) is int and type(move[1]) is int:
            if move[0] >= 0 and move[0] < size and move[1] >= 0 and move[1] < size:
                return move
    except (JSONDecodeError, TypeError):
        if user_input == "FORFEIT":
            return "FORFEIT"

if __name__ == '__main__':
    size = int(input("Size of board: "))
    depth = int(input("Depth of board: "))

    main_board = create_board(size, depth)

    winner = None
    forfeiter = None

    print(main_board)

    coords = []
    layer = depth
    while len(coords) < depth - 1:
        coords.append(parse_move(input("Choose board to start on in layer {} ([col, row]): ".format(layer))))
        layer -= 1

    print("A valid move is either a coordinate as so: [0, 0], or FORFEIT")

    players = ["X", "O"]
    player_index = 0
    while (not main_board.check_winner()) and (not forfeiter):
        player = players[player_index]
        move = None
        while move is None:
            move = parse_move(input("Move for player {}: ".format(player)))
            if move is None:
                print("A valid move is either a coordinate as so: [0, 0], or FORFEIT")
        if move == "FORFEIT":
            forfeiter = player
        else:
            coords.append(move)
            main_board.perform_move(player, coords)
            coords.pop(0)
            print(main_board)
        player_index = (player_index + 1) % len(players)

    winner = main_board.check_winner()

    if winner is not None:
        print("Player {} won the board, and the game!".format(winner))
    elif forfeiter is not None:
        print("Player {} forfeited the game.".format(forfeiter))
        
