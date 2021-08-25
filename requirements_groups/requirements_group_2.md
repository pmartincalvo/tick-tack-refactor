# Requirement group 2

## Intro

The second requirement group adds a few small features to the first group. Remember:
you must use the code you built for requirements group 1.


## Specific requirements

- Before the match starts, the user can pick which player will have the first move.
- After the final move, if it's a winning one, the board is printed showing only the winning marks.
  That means that if the board is in the following state.
  
```
-------------
| X | O | X |
-------------
| X | 5 | O |
-------------
| 7 | 8 | 9 |
-------------
```
And the player with the mark X places it on cell 7, the final printed board looks like:
```
-------------
| X |   |   |
-------------
| X |   |   |
-------------
| X |   |   |
-------------
```
If a stalemate is reached, the board is printed with all the marks on it, just like in 
requirements group 1.
- Once the match finishes, the CLI asks the user if they would like to start over,
  instead of simply finishing execution.


## Acceptance criteria

The resulting code should provide an experience as follows:
1. Before starting the match, the CLI asks which player should start, and the user can 
give some input to make a choice.
2. The match is played exactly as it was specified in requirements group 1.
3. After someone wins or a stalemate is reached, the final board is printed. If someone
has won, only the winning marks appear on the board.
4. The CLI asks the user if he wants to play another match. The user says yes, and the flow repeats.
5. The flow repeats until the user indicates it doesn't want to play another match.
