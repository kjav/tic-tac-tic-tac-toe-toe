function arrayEq(as, bs) {
  if (as.length != bs.length)
    return false;

  for (var i = 0; i < as.length; i++) {
    if (as[i] != bs[i])
      return false;
  }

  return true;
}

function Board(cells) {
    /*
    Pass in a list of lists of Board objects in a rectangular grid, or
    an empty list for a single cell (layer 0).
    */
    this.grid = cells;
    this.rows = this.grid.length;
    if (this.rows == 0)
        this.cols = 0;
    else
        this.cols = this.grid[0].length;
    this.layer = 0;
    var inner_grid = this.grid;
    while (inner_grid.length > 0) {
        this.layer += 1;
        inner_grid = inner_grid[0][0].grid;
    }
    this.owner = undefined;

    this.draw_board = function(active_coordinates) {
        debugger;
        var piece;
        //console.log("Owner: ", this.owner);
        if (this.owner == undefined)
            piece = ' ';
        else
            piece = this.owner.toString();

        var is_active = active_coordinates != undefined;
        if (is_active)
            is_active = is_active && (active_coordinates.length > 0);

        if (this.rows == 0 && this.cols == 0)
            return piece;
        else {
            var result = "";
            for (var i = 0; i < this.rows; i++) {
                var result_rows = [];
                for (var j = 0; j < this.cols; j++) {
                    var substr = "";
                    if (is_active && arrayEq(active_coordinates[0], [j, i])) {
                        substr = this.grid[i][j].draw_board(active_coordinates.slice(1));
                    } else {
                        substr = this.grid[i][j].draw_board(undefined);
                    }
                    var lines_of_substr = substr.split('\n');
                    var str_length = lines_of_substr[0].length;
                    if (this.grid[i][j].check_winner() == undefined) {
                        substr = (lines_of_substr.map(ln => " " + ln + " ")).join("\n");
                    } else {
                        var winner = this.grid[i][j].check_winner()
                        substr = (lines_of_substr.map(_ => " ".repeat(str_length))).join("\n");
                        var substr_length = substr.length;
                        substr = substr.slice(0, Math.floor(substr_length/2)) + winner + substr.slice(Math.floor(substr_length/2) + 1, substr_length);
                    }
                    lines_of_substr = substr.split('\n')
                    str_length = lines_of_substr[0].length
                    var blank_row;
                    if (str_length > 3) { //Check not single cell
                        if (is_active && (active_coordinates.length == 1) && arrayEq(active_coordinates[0], [j, i])) {
                            blank_row = "*" + " ".repeat(str_length - 2) + "*";
                        } else {
                            blank_row = " ".repeat(str_length);
                        }
                        substr = "{0}\n{1}\n{0}".replace(/\{0\}/g, blank_row).replace(/\{1\}/g, substr);
                    }
                    if (i > 0) { //Only after first row
                        substr = "-".repeat(str_length) + "\n" + substr;
                    }
                    if (j > 0) { //Only after first column
                        lines_of_substr = substr.split('\n');
                        substr = ""; // Rebuild from here...
                        for (var line of lines_of_substr)
                            substr += "|\{\}\n".replace(/\{\}/g, line);
                    }
                    result_rows.push(substr);
                }
                result_rows = result_rows.map(x => x.split("\n"));
                ////console.log(result_rows);
                for (var k = 0; k < result_rows[0].length; k++) {
                    for (var r of result_rows)
                        result += r[k];
                    ////console.log(k, ': ', result);
                    result += '\n';
                }
            }
            return result.slice(0, -1);
        }
    };
        

    this.str = function() {
        return this.draw_board(undefined)
    };

    this.getitem = function(pos) {
        return this.grid[pos[0]][pos[1]]
    };

    this.get_rows = function() {
        return this.grid;
    };

    this.get_cols = function() {
        var cs = [];
        for (var i = 0; i < this.cols; i++) {
            var row = [];
            for (var j = 0; j < this.grid.length; j++)
                row.push(this.grid[j][i]);
            cs.push(row);
        }
        return cs;
    };

    this.get_diags = function() {
        /*
        Get a list of the cells along the diagonals, where the first includes
        the top left cell and the second includes the top right.
        */
        if ((this.rows != this.cols) || !(this.grid.length))
            return [];
        var left_diag = [];
        var right_diag = [];
        for (var i = 0; i < self.rows; i++) {
            left_diag.push(this.grid[i][i]);
            right_diag.push(this.grid[i][this.cols - i - 1]);
        }
        return [left_diag, right_diag];
    }; 

    this.is_complete = function() {
        if (this.owner != undefined)
            return true
        else if ((this.rows == 0) && (this.cols == 0))
            return false //No inner boards to check
        // Assume all inner boards are complete, seeking contradiction.
        var result = true
        var all_coords = [];
        for (var r = 0; r < this.rows; r++)
            for (var c = 0; c < this.cols; c++)
                all_coords.push([r, c]);
        for (var coord of all_coords)
            if (!self.grid[coord[0]][coord[1]].is_complete())
                return false;
        return result;
    };

    this.is_valid_move = function(coords) {
        var board = this;
        for (var c of coords)
            board = board.grid[c[1]][c[0]];
        return !board.is_complete();
    };

    this.perform_move = function(player, coords) {
        /*
        Arguments are:
        player - single-character represtation of a player e.g. 'O', 'X',
            or use None to perform a dry-run to check if the move is valid
        coords - list of coordindate tuples from top layer to bottom
        Iterates through coords returning False if selected cell has an owner,
        otherwise iterates a layer deeper. If coords is empty, the owner of
        the board is set to player (even if not at layer 0).
        */
        var coords = coords.slice()
        if (this.owner != undefined)
            return false;
        if (!coords.length) { // should also check rows==0?
            this.owner = player;
            return true;
        } else {
            //console.log(coords);
            var c = coords[0];
            var is_valid = this.grid[c[1]][c[0]].perform_move(player, coords.slice(1));
            //console.log(this);
            this.owner = this.check_winner(); //Only needs to be called if inner
                                              //board becomes completed
            return is_valid
        }
    };

    this.check_winner = function() {
        /*
        Return the owner of the board after checking for completion. A (square)
        board of size n is defined as being completed if there is a single
        player who owns a line of n cells, which can be vertical, horizontal,
        or diagonal through the centre cell.
        */
        if (this.owner != undefined)
            return this.owner;
        var rows = this.get_rows();
        for (var i = 0; i < rows.length; i++) {
            if (rows[i].filter(c => (c.owner == rows[i][0].owner) && (c.owner != undefined)).length == this.cols)
                return r[i][0].owner;
        }
        var cols = this.get_cols();
        //console.log(cols);
        for (var i = 0; i < cols.length; i++) {
            if (cols[i].filter(c => (c.owner == cols[i][0].owner) && (c.owner != undefined)).length == this.rows)
                return cols[i][0].owner;
        }
        var diags = this.get_diags();
        for (var i = 0; i < diags.length; i++) {
            if (diags[i].filter(c => (c.owner == diags[i][0].owner) && (c.owner != undefined)).length == this.rows)
                return diags[i][0].owner;
        }
    };
}

function create_board(size=3, depth=1) {
    // Returns a board which has dimensions size x size x depth.
    if (depth == 0)
        return new Board([]);
    var grid = [];
    for (var i = 0; i < size; i++) {
        var row = [];
        for (var j = 0; j < size; j++)
            row.push(create_board(size, depth=depth-1));
        grid.push(row);
    }
    return new Board(grid);
}

function parse_move(user_input) {
    if (user_input == "FORFEIT")
        return "FORFEIT";
    // Transform to list of 2 strings which were separated by comma or spaces.
    user_input = user_input.replace(/[\ \(\[\)\]]/g, "").replace(",", " ").replace(/ +/g, " ").split(' ');
    try { // Catch the case input can't be converted to int
        move = user_input.map(x => +x);
    } catch(err) {
        //console.log(err);
        return;
    }
    // Check two numbers were entered (case of more than 2 already caught) and
    // that they are within the required range.
    if ((move.length == 2) && (move[0] >= 0) && (move[0] < size) && (move[1] >= 0) && (move[1] < size))
        return move;
}

function create_board(size=3, depth=1) {
    // Returns a board which has dimensions size x size x depth.
    if (depth == 0)
        return new Board([]);
    var grid = [];
    for (var i = 0; i < size; i++) {
        var row = [];
        for (var j = 0; j < size; j++)
            row.push(create_board(size, depth-1));
        grid.push(row)
    }
    return new Board(grid)
}
