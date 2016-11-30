

class Board:
    def __init__(self, cells):
        self.grid = cells
        self.rows = len(self.grid)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(self.grid[0])
        self.owner = None

    def __str__(self):
        pieces = {None: ' ', 'O': 'O', 'X': 'X'}
        if self.rows == self.cols == 0:
            return ("+---+\n| {} |\n+---+").format(pieces[self.owner])
        else:
            contents = [pieces[b.owner] for row in self.grid for b in row]
            cell = " {} "
            row = (cell + "|")*(self.cols - 1) + cell + "\n"
            row_with_line = row + "---+"*(self.cols - 1) + "---" "\n"
            return (row_with_line*(self.rows - 1) + row).format(*contents)

    def perform_move(self, player, coords):
        """Returns False if the selected cell has an owner."""
        if self.owner is None:
            if not coords:
                self.owner = player
                return True
            else:
                coord = coords.pop(0)
                is_valid = self.grid[coord[0]][coord[1]].perform_move(player,
                    coords)
                self.check_completion()
                return is_valid
        else:
            return False

    def check_completion(self):
        pass






if __name__ == '__main__':
    size = 4
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            b = Board([])
            row.append(b)
        grid.append(row)

    main_board = Board(grid)
    main_board.perform_move('O', [(0, 1)])
    main_board.perform_move('X', [(2, 2)])
    main_board.perform_move('X', [(3, 0)])
    print(main_board)
    print(main_board.grid[0][1])
