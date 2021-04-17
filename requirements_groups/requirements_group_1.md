# Requirement group 1

## Intro

The first requirement group is a simple implementation of a CLI tick-tack-toe.
No fancy stuff.


## Specific requirements

- A script named `main.py` is the entrypoint to the code. Starting it starts
a new game from scratch. No external data or parameters are needed.
- The script runs a 1vs1 game of 3x3 tick-tack-toe.
- Player 1 is always the starting one, and uses the "X" mark. Player 2 uses the
  "O" mark.
- Each player takes a turn to place their mark, and they can select where to 
place their mark by indicating the cell with a number. The numbering goes as follows:
  
```
-------------
| 1 | 2 | 3 |
-------------
| 4 | 5 | 6 |
-------------
| 7 | 8 | 9 |
-------------
```
- After each movement, the board is printed to screen, showing all the marks 
that have been placed already.
- If one of the players wins by placing 3 marks in a line, a message is printed
announcing the winner and the program exits.
- If a stalemate is reached, a message is printed announcing it and the program 
exits.
  
Besides that, please keep in mind all the common, well-known rules of 
tic-tac-toe (one mark per turn, one turn for each player, only one mark can be
set in a cell, etc.). If in doubt, [check here](http://web.cecs.pdx.edu/~bart/cs541-fall2001/homework/tictactoe-rules.html).


## Acceptance criteria

The resulting code should provide an experience as follows:
1. After running `main.py`, an empty board appears on the screen. Some text 
should also indicate whose player turn is it. Since player 1 always starts,
it should show player 1 at first.
2. An input space allows player 1 to pick in which cell he would like to place
his mark.
3. The board appears again, now showing the board with player's 1 mark. Now 
it's player's 2 turn.
4. The pattern keeps on going until the game ends with either the victory of 
one of the players or a stalemate.
5. Execution finishes.