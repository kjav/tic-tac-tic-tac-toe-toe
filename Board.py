from piece import Piece


class Board(object):
    def __init__(self, cells):
        self.grid = cells
        self.rows = len(self.grid)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(self.grid[0])
        self.owner = None

    def perform_move(player, coords):
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


