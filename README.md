# tic-tac-tic-tac-toe-toe

An n-dimensional m-layer noughts and crosses game

Here is an example of a 3x3x2 board played on the command line:

![Early stages of a 3x3x2 game](http://i.imgur.com/u8kf3Ep.png)

![The first 2 subboards have been won](http://i.imgur.com/HT8bqxZ.png)

![The end of a 3x3x2 game](http://i.imgur.com/QRBhSzR.png)


## Running the code

### CLI game (Python)

The Python CLI implementation depends on Python 3.6+ and no external dependencies.

It can be run with: `python3 run.py`


### CLI game (JavaScript)

1. Copy the entire board.js file into a javascript interpreter (e.g. the [chrome console](https://developers.google.com/web/tools/chrome-devtools/console/)).
2. Create a board
  `let board = create_board();`
3. Draw the board to see current status
  `board.draw_board()`
4. Perform a move
   `board.perform_move(player, coords)`
 
The arguments for the perform_move function are:  
        -  player - single-character represtation of a player e.g. 'O', 'X', or use undefined to perform a dry-run to check if the move is valid  
        -  coords - list of coordindate tuples from top layer to bottom  
        
It iterates through coords returning False if selected cell has an owner, otherwise iterates a layer deeper. If coords is empty, the owner of the board is set to player (even if not at layer 0).  


## Running the tests

There are currently some very basic 'tests' for the Python CLI implementation, which is really just an example of exercising the main APIs!

Run with: `python3 test.py`
