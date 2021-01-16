"""
Implementation of a generalised tic-tac-toe board.
"""

__all__ = ("Board", "create_board")

from typing import List, Optional, Tuple


class Board:
    def __init__(self, cells: List[List["Board"]]):
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
        return self.draw_board(None)

    def __bytes__(self):
        if len(self.grid) == 0:
            return bytes("'" + str(self.owner) + "'", "utf8")
        ret = b"["  # byte string (to use bytes method recursively below)
        ret += b",".join(
            [
                b"[" + b",".join(map(bytes, self.grid[r])) + b"]"
                for r in range(self.rows)
            ]
        )
        ret += b"]"
        return ret

    def __getitem__(self, pos):
        try:
            return self.grid[pos[0]][pos[1]]
        except IndexError:
            raise IndexError("Index {} out of board range".format(pos))

    def draw_board(self, active_coordinates):
        piece = {None: " ", "O": "O", "X": "X"}[self.owner]
        if self.rows == self.cols == 0:
            return piece
        else:
            result = ""
            for i in range(self.rows):
                result_rows = []
                for j in range(self.cols):
                    substr = ""
                    if active_coordinates and active_coordinates[0] == (j, i):
                        # print(active_coordinates[1:])
                        substr = self[i, j].draw_board(active_coordinates[1:])
                    else:
                        substr = self[i, j].draw_board(None)
                    lines_of_substr = substr.split("\n")
                    str_length = len(lines_of_substr[0])
                    if self[i, j].check_winner() is None:
                        substr = "\n".join(
                            [" {} ".format(ln) for ln in lines_of_substr]
                        )
                    else:
                        winner = self[i, j].check_winner()
                        substr = "\n".join(
                            [" {} ".format(" " * str_length) for _ in lines_of_substr]
                        )
                        substr_length = len(substr)
                        substr = (
                            substr[0 : int(substr_length / 2)]
                            + winner
                            + substr[int(substr_length / 2) + 1 : substr_length]
                        )
                    lines_of_substr = substr.split("\n")
                    str_length = len(lines_of_substr[0])
                    if str_length > 3:  # Check not single cell
                        # print(active_coordinates)
                        if active_coordinates and active_coordinates[0] == (j, i):
                            blank_row = "*" + " " * (str_length - 2) + "*"
                        else:
                            blank_row = " " * str_length
                        substr = "{0}\n{1}\n{0}".format(blank_row, substr)
                    if i > 0:  # Only after first row
                        substr = "-" * str_length + "\n" + substr
                    if j > 0:  # Only after first column
                        lines_of_substr = substr.split("\n")
                        substr = ""  # Rebuild from here...
                        for line in lines_of_substr:
                            substr += "|{}\n".format(line)
                    result_rows.append(substr)
                result_rows = [x.splitlines() for x in result_rows]
                for k in range(len(result_rows[0])):
                    for row in result_rows:
                        result += row[k]
                    result += "\n"
            return result[0:-1]

    def get_rows(self) -> List[List["Board"]]:
        return self.grid

    def get_cols(self) -> List[List["Board"]]:
        return [[row[i] for row in self.grid] for i in range(self.cols)]

    def get_diags(self) -> List[List["Board"]]:
        """
        Get a list of the cells along the diagonals, where the first includes
        the top left cell and the second includes the top right.
        """
        if self.rows != self.cols or not self.grid:
            return []
        return [
            [self.grid[i][i] for i in range(self.rows)],
            [self.grid[i][-1 - i] for i in range(self.rows)],
        ]

    def perform_move(
        self, player: Optional[str], coords: List[Tuple[int, int]]
    ) -> bool:
        """
        Arguments are:
        player - single-character represtation of a player e.g. 'O', 'X',
            or use None to perform a dry-run to check if the move is valid
        coords - list of coordindate tuples from top layer to bottom
        Iterates through coords returning False if selected cell has an owner,
        otherwise iterates a layer deeper. If coords is empty, the owner of
        the board is set to player (even if not at layer 0).
        """
        coords = coords.copy()
        if self.owner is not None:
            return False
        if not coords:  # should also check rows==0?
            self.owner = player
            return True
        else:
            c = coords.pop(0)
            is_valid = self.grid[c[1]][c[0]].perform_move(player, coords)
            self.owner = self.check_winner()  # Only needs to be called if inner
            # board becomes completed
            return is_valid

    def check_move(self, coords: List[Tuple[int, int]]) -> bool:
        return self.perform_move(None, coords)

    def check_winner(self) -> Optional[str]:
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


def create_board(size: int = 3, depth: int = 1) -> Board:
    """Returns a board which has dimensions size x size x depth."""
    if depth == 0:
        return Board([])
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(create_board(size, depth=depth - 1))
        grid.append(row)
    return Board(grid)
