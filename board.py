

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
            return ("""
             ---
            | {} |
             ---
            """).format(pieces[self.owner])
        elif self.rows != 3:
            return "" # Not implemented yet
        else:
            contents = [pieces[b.owner] for row in self.grid for b in row]
            return ("""
             {} | {} | {}
            -----------
             {} | {} | {}
            -----------
             {} | {} | {}
            """).format(*contents)

    def perform_move(self, player, coords):
        if self.owner is None:
            coord = coords.pop(0)
            if not coord:
                self.owner = player
                return True
            is_valid = self.grid[coord[0]][coord[1]].perform_move(player,
                coords)
            self.check_completion()
            return is_valid
        else:
            return False

    def check_completion(self):
        pass






if __name__ == '__main__':
    grid = []
    for i in range(3):
        row = []
        for j in range(3):
            b = Board([])
            row.append(b)
        grid.append(row)

    main_board = Board(grid)
    main_board.perform_move('O', [(0, 1), ()])
    main_board.perform_move('X', [(2, 2), ()])
    print(main_board)
    print(main_board.grid[0][1])

